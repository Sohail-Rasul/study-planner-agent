from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional
import datetime
from agents.planner import StudyPlannerAgent
from skills.memory import MemorySkill

app = FastAPI(title="Smart Study Planner API")
agent = StudyPlannerAgent()

class GeneratePlanRequest(BaseModel):
    subjects: List[str] = Field(..., description="List of subjects to study")
    exam_dates: Dict[str, str] = Field(..., description="Exam dates mapped to subjects as YYYY-MM-DD")
    hours_available: float = Field(..., description="Hours available to study per day", gt=0, le=24)

    @field_validator('subjects')
    @classmethod
    def validate_subjects(cls, v):
        if not v:
            raise ValueError("Subjects list cannot be empty")
        cleaned = [s.strip() for s in v if isinstance(s, str) and s.strip()]
        if not cleaned:
            raise ValueError("Subjects list must contain at least one valid subject name")
        return cleaned

    @field_validator('exam_dates')
    @classmethod
    def validate_exam_dates(cls, v):
        current_date = datetime.date(2026, 7, 2)
        for subject, date_str in v.items():
            try:
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError(f"Exam date for '{subject}' must be in YYYY-MM-DD format")
            if date_obj < current_date:
                raise ValueError(f"Exam date for '{subject}' ({date_str}) must be in the future (on or after {current_date})")
        return v

class UpdatePlanRequest(BaseModel):
    completed_tasks: List[dict] = Field(..., description="List of completed task dictionaries")

class ChatRequest(BaseModel):
    query: str = Field(..., description="Study or productivity question")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the Smart Study Planner API"
    }

@app.post("/plan/generate")
def generate_plan(payload: GeneratePlanRequest):
    try:
        plan = agent.generate_plan(
            subjects=payload.subjects,
            exam_dates=payload.exam_dates,
            hours_available=payload.hours_available
        )
        return plan
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/plan/update")
def update_plan(payload: UpdatePlanRequest):
    try:
        update_result = agent.update_plan(completed_tasks=payload.completed_tasks)
        return update_result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_history():
    memory = MemorySkill()
    return {"history": memory.get_history()}

@app.delete("/history")
def clear_history():
    memory = MemorySkill()
    if memory.clear_history():
        return {"success": True, "message": "Study history cleared successfully"}
    raise HTTPException(status_code=500, detail="Failed to clear study history")

@app.post("/chat")
def chat(payload: ChatRequest):
    query = payload.query.strip().lower()
    
    # Try calling MCP tool or fallback to answering
    mcp_res = agent.mcp_client.call_tool(
        "google-developer-knowledge",
        "answer_query",
        {"query": payload.query}
    )
    
    if "answer_text" in mcp_res:
        return {
            "query": payload.query,
            "answer": mcp_res["answer_text"],
            "references": mcp_res.get("references", [])
        }
        
    return {
        "query": payload.query,
        "answer": "Focus on breaking your study time into 25-minute Pomodoro sessions and space out subject revisions.",
        "references": []
    }

