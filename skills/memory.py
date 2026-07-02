import json
import os

class MemorySkill:
    """
    Skill for remembering previous study sessions and retaining student progress context.
    """
    def __init__(self, filepath="study_history.json"):
        # Store in current directory or project root
        self.filepath = filepath

    def save_session(self, session_data: dict) -> bool:
        """
        Save study session details.
        """
        try:
            history = self.get_history()
            history.append(session_data)
            with open(self.filepath, "w") as f:
                json.dump(history, f, indent=4)
            return True
        except Exception:
            return False

    def get_history(self) -> list:
        """
        Get past study history.
        """
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def clear_history(self) -> bool:
        """
        Clear past study history.
        """
        if os.path.exists(self.filepath):
            try:
                os.remove(self.filepath)
                return True
            except Exception:
                return False
        return True

