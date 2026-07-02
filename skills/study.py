class StudySkill:
    """
    Skill for study session management, Pomodoro scheduling, and breaks.
    """
    def __init__(self):
        pass

    def breakdown_to_pomodoro(self, total_hours: float) -> list:
        """
        Split study hours into Pomodoro blocks (25 mins study, 5 mins break).
        """
        if total_hours <= 0:
            return []
            
        blocks = []
        # A full Pomodoro cycle is 30 minutes (25 min study + 5 min break)
        num_cycles = int(total_hours // 0.5)
        for _ in range(num_cycles):
            blocks.append({"type": "study", "duration_minutes": 25})
            blocks.append({"type": "break", "duration_minutes": 5})
            
        remaining_hours = total_hours % 0.5
        remaining_minutes = int(round(remaining_hours * 60))
        
        if remaining_minutes >= 30:
            blocks.append({"type": "study", "duration_minutes": 25})
            blocks.append({"type": "break", "duration_minutes": 5})
        elif remaining_minutes > 5:
            blocks.append({"type": "study", "duration_minutes": remaining_minutes - 5})
            blocks.append({"type": "break", "duration_minutes": 5})
        elif remaining_minutes > 0:
            blocks.append({"type": "study", "duration_minutes": remaining_minutes})
            
        return blocks

