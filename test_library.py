import unittest
from datetime import date
from library import LibraryManager, LoanCommand


class LibraryTests(unittest.TestCase):
    def setUp(self):
        self.manager = LibraryManager()
        self.manager.reset()

    def test_two_lookups_share_same_state(self):
        second_lookup = LibraryManager()
        command = LoanCommand("book-1", "Ravi", date(2026, 11, 25), self.manager)
        command.execute()
        self.assertIs(self.manager, second_lookup)
        self.assertEqual(second_lookup.items["book-1"], "loaned")

    def test_second_loan_for_same_item_is_rejected(self):
        first = LoanCommand("camera-1", "Ravi", date(2026, 11, 25), self.manager)
        second = LoanCommand("camera-1", "Maya", date(2026, 11, 26), self.manager)
        first.execute()
        with self.assertRaises(ValueError):
            second.execute()

    def test_undo_restores_availability(self):
        command = LoanCommand("tripod-1", "Aishu", date(2026, 11, 25), self.manager)
        command.execute()
        command.undo()
        self.assertTrue(self.manager.is_available("tripod-1"))
        self.assertNotIn("tripod-1", self.manager.loans)

    def test_overdue_reminder(self):
        command = LoanCommand("book-1", "Ravi", date(2026, 11, 10), self.manager)
        command.execute()
        reminders = self.manager.overdue_reminders(date(2026, 11, 18))
        self.assertEqual(len(reminders), 1)
        self.assertIn("book-1", reminders[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
