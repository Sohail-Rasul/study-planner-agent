import datetime
import os
from typing import Any
from google.adk import Agent
from skills.calendar import CalendarSkill
from skills.memory import MemorySkill
from skills.study import StudySkill
from mcp.mcp_client import MCPClient

class StudyPlannerAgent(Agent):
    """
    Main Planner Agent responsible for understanding user goals, planning study schedules,
    selecting appropriate skills, calling MCP tools, and returning structured responses.
    This is implemented as a Google ADK Agent.
    """
    name: str = "StudyPlannerAgent"
    description: str = "Main Planner Agent responsible for study planning and scheduling"
    calendar_skill: Any = None
    memory_skill: Any = None
    study_skill: Any = None
    mcp_client: Any = None

    def __init__(self, history_filepath="study_history.json", **kwargs):
        kwargs.setdefault("name", "StudyPlannerAgent")
        kwargs.setdefault("description", "Main Planner Agent responsible for study planning and scheduling")
        super().__init__(**kwargs)
        self.calendar_skill = CalendarSkill()
        self.memory_skill = MemorySkill(filepath=history_filepath)
        self.study_skill = StudySkill()
        self.mcp_client = MCPClient()

    def generate_plan(self, subjects: list, exam_dates: dict, hours_available: float) -> dict:
        """
        Generates a realistic study plan based on subjects, exam dates, and available daily hours.
        """
        # Input validation
        if not subjects:
            raise ValueError("Subjects list cannot be empty")
        for sub in subjects:
            if not isinstance(sub, str) or not sub.strip():
                raise ValueError("Subject names must be non-empty strings")
                
        if not isinstance(exam_dates, dict):
            raise ValueError("Exam dates must be a dictionary")
            
        current_date = datetime.date(2026, 7, 2)  # Reference date as per rules/system
        
        parsed_exams = {}
        for sub in subjects:
            if sub not in exam_dates:
                # If exam date is not provided, default to 7 days from now
                exam_date_obj = current_date + datetime.timedelta(days=7)
                parsed_exams[sub] = exam_date_obj
            else:
                date_str = exam_dates[sub]
                try:
                    exam_date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                except ValueError:
                    raise ValueError(f"Exam date for {sub} must be in YYYY-MM-DD format")
                
                if exam_date_obj < current_date:
                    raise ValueError(f"Exam date for {sub} ({date_str}) must be in the future (on or after {current_date})")
                parsed_exams[sub] = exam_date_obj

        if not isinstance(hours_available, (int, float)) or hours_available <= 0 or hours_available > 24:
            raise ValueError("Available study hours must be a positive number between 0 and 24")

        # Let's schedule from current_date up to the day before the last exam (max 14 days)
        last_exam_date = max(parsed_exams.values())
        total_days = (last_exam_date - current_date).days
        planning_horizon = min(max(total_days, 1), 14)
        
        schedule = []
        for d in range(planning_horizon):
            day_date = current_date + datetime.timedelta(days=d)
            
            # Active subjects are those whose exam date is strictly after this day
            active_subjects = [
                sub for sub, exam_dt in parsed_exams.items()
                if exam_dt > day_date
            ]
            
            if not active_subjects:
                continue
                
            # Sort active subjects by exam date proximity (nearest first) - task prioritization
            active_subjects.sort(key=lambda s: parsed_exams[s])
            
            # Allocate slots using CalendarSkill
            slots = self.calendar_skill.allocate_slots(active_subjects, hours_available)
            
            schedule.append({
                "date": day_date.strftime("%Y-%m-%d"),
                "day_of_week": day_date.strftime("%A"),
                "slots": slots
            })
            
        # Generate recommendations using MCP client information or rule-based fallback
        recommendations = []
        # Query developer knowledge for productivity tip
        mcp_res = self.mcp_client.call_tool(
            "google-developer-knowledge", 
            "answer_query", 
            {"query": "study planner productivity tips"}
        )
        if "answer_text" in mcp_res:
            recommendations.append(mcp_res["answer_text"])
            
        # Subject-specific prioritization tips
        sorted_subjects = sorted(parsed_exams.keys(), key=lambda s: parsed_exams[s])
        nearest_sub = sorted_subjects[0]
        days_left = (parsed_exams[nearest_sub] - current_date).days
        recommendations.append(f"Focus heavily on {nearest_sub} as the exam is in {days_left} days.")
        
        # General guidelines
        recommendations.append("Take 5-minute Pomodoro breaks to keep retention high.")
        recommendations.append("Review history to see how closely you stuck to the previous schedules.")
        
        return {
            "success": True,
            "subjects": subjects,
            "exam_dates": {k: v.strftime("%Y-%m-%d") for k, v in parsed_exams.items()},
            "hours_available_per_day": hours_available,
            "schedule": schedule,
            "recommendations": recommendations
        }

    def update_plan(self, completed_tasks: list) -> dict:
        """
        Updates the study plan based on completed study tasks.
        """
        if not isinstance(completed_tasks, list):
            raise ValueError("Completed tasks must be a list")
            
        for task in completed_tasks:
            # Save completed tasks to memory
            self.memory_skill.save_session(task)
            
        history = self.memory_skill.get_history()
        
        # Calculate summary stats
        total_completed_mins = sum(t.get("duration_minutes", 0) for t in history)
        subject_counts = {}
        for t in history:
            sub = t.get("subject", "Unknown")
            subject_counts[sub] = subject_counts.get(sub, 0) + t.get("duration_minutes", 0)
            
        return {
            "success": True,
            "message": f"Successfully registered {len(completed_tasks)} completed sessions.",
            "total_completed_minutes": total_completed_mins,
            "breakdown_by_subject": subject_counts,
            "history": history
        }


