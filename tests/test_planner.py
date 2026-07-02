import unittest
import os
import datetime
from agents.planner import StudyPlannerAgent
from skills.study import StudySkill
from skills.calendar import CalendarSkill
from skills.memory import MemorySkill

class TestStudyPlanner(unittest.TestCase):
    def setUp(self):
        # Use a temporary test file for memory
        self.test_history_file = "test_study_history.json"
        self.agent = StudyPlannerAgent(history_filepath=self.test_history_file)

    def tearDown(self):
        if os.path.exists(self.test_history_file):
            try:
                os.remove(self.test_history_file)
            except OSError:
                pass

    def test_generate_plan_valid(self):
        subjects = ["Math", "History"]
        # Dates in future relative to 2026-07-02
        exam_dates = {"Math": "2026-07-05", "History": "2026-07-06"}
        res = self.agent.generate_plan(subjects, exam_dates, 2.0)
        
        self.assertTrue(res["success"])
        self.assertEqual(res["subjects"], subjects)
        self.assertIn("schedule", res)
        self.assertGreater(len(res["schedule"]), 0)
        
        # Verify Pomodoro format
        day1 = res["schedule"][0]
        self.assertIn("slots", day1)
        self.assertGreater(len(day1["slots"]), 0)
        self.assertEqual(day1["slots"][0]["subject"], "Math")

    def test_generate_plan_validation_errors(self):
        # Empty subjects list should raise ValueError
        with self.assertRaises(ValueError):
            self.agent.generate_plan([], {}, 2.0)

        # Invalid exam date format should raise ValueError
        with self.assertRaises(ValueError):
            self.agent.generate_plan(["Math"], {"Math": "July 5th"}, 2.0)

        # Past exam date should raise ValueError (relative to 2026-07-02)
        with self.assertRaises(ValueError):
            self.agent.generate_plan(["Math"], {"Math": "2026-06-01"}, 2.0)

        # Invalid hours should raise ValueError
        with self.assertRaises(ValueError):
            self.agent.generate_plan(["Math"], {"Math": "2026-07-15"}, -1.0)
        with self.assertRaises(ValueError):
            self.agent.generate_plan(["Math"], {"Math": "2026-07-15"}, 25.0)

    def test_study_skill_pomodoro(self):
        skill = StudySkill()
        # 1 hour should split into 2 study/break pairs
        blocks = skill.breakdown_to_pomodoro(1.0)
        self.assertEqual(len(blocks), 4)
        self.assertEqual(blocks[0]["type"], "study")
        self.assertEqual(blocks[0]["duration_minutes"], 25)
        self.assertEqual(blocks[1]["type"], "break")
        self.assertEqual(blocks[1]["duration_minutes"], 5)

    def test_calendar_skill_allocation(self):
        skill = CalendarSkill()
        slots = skill.allocate_slots(["Math"], 1.0)
        # Should allocate 1 hour for Math, splitting to Pomodoro slots
        self.assertEqual(len(slots), 4)
        self.assertEqual(slots[0]["subject"], "Math")
        self.assertEqual(slots[0]["type"], "study")

    def test_memory_skill(self):
        mem = MemorySkill(filepath=self.test_history_file)
        # Clear/initialize
        mem.clear_history()
        self.assertEqual(len(mem.get_history()), 0)
        
        # Save a session
        session = {"subject": "Math", "duration_minutes": 25}
        mem.save_session(session)
        
        history = mem.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["subject"], "Math")

if __name__ == '__main__':
    unittest.main()

