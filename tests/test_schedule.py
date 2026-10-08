import unittest

from bot import schedule


class TestSchedule(unittest.TestCase):

    def test_weekdays_exist(self):
        """Проверка наличия учебных дней."""
        expected_days = [
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
            "Суббота",
        ]

        for day in expected_days:
            self.assertIn(day, schedule)

    def test_monday_schedule(self):
        """Проверка расписания понедельника."""
        self.assertEqual(len(schedule["Понедельник"]), 2)

    def test_tuesday_schedule(self):
        """Проверка расписания вторника."""
        self.assertEqual(len(schedule["Вторник"]), 5)

    def test_saturday_schedule(self):
        """Проверка русского языка в субботу."""
        subjects = [subject for time, subject in schedule["Суббота"]]

        self.assertIn("Русский язык (устная речь)", subjects)


if __name__ == "__main__":
    unittest.main()