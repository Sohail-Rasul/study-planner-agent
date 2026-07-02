import datetime

class CalendarSkill:
    """
    Skill for calendar scheduling, slot validation, and conflict checking.
    """
    def __init__(self):
        pass

    def allocate_slots(self, tasks: list, available_hours: float) -> list:
        """
        Allocate time slots for study tasks on a single day.
        `tasks` is a list of subject names (strings).
        """
        if not tasks or available_hours <= 0:
            return []
            
        # Distribute available hours equally among active subjects for the day
        hours_per_subject = available_hours / len(tasks)
        
        allocated = []
        # Start scheduling at 09:00 AM by default
        current_time = datetime.datetime(2026, 7, 2, 9, 0)  # Reference date-time
        
        from skills.study import StudySkill
        study_skill = StudySkill()
        
        for subject in tasks:
            pomodoros = study_skill.breakdown_to_pomodoro(hours_per_subject)
            
            for block in pomodoros:
                duration = block["duration_minutes"]
                end_time = current_time + datetime.timedelta(minutes=duration)
                
                allocated.append({
                    "subject": subject,
                    "type": block["type"],
                    "duration_minutes": duration,
                    "start_time": current_time.strftime("%H:%M"),
                    "end_time": end_time.strftime("%H:%M")
                })
                current_time = end_time
                
        return allocated

