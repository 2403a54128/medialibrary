from datetime import date


class LibraryManager:
    """Singleton that stores the shared media-loan state."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.items = {
                "book-1": "available",
                "camera-1": "available",
                "tripod-1": "available",
            }
            cls._instance.loans = {}
        return cls._instance

    def reset(self):
        """Reset state for demonstrations and unit tests."""
        self.items = {
            "book-1": "available",
            "camera-1": "available",
            "tripod-1": "available",
        }
        self.loans = {}

    def is_available(self, item_id):
        return self.items.get(item_id) == "available"

    def overdue_reminders(self, today=None):
        today = today or date.today()
        reminders = []
        for item_id, loan in self.loans.items():
            if loan["due_date"] < today:
                reminders.append(
                    f"Reminder: {item_id} is overdue (due {loan['due_date']})."
                )
        return reminders


class LoanCommand:
    """Command object that supports execute and undo."""
    def __init__(self, item_id, borrower, due_date, manager=None):
        self.manager = manager or LibraryManager()
        self.item_id = item_id
        self.borrower = borrower
        self.due_date = due_date
        self.executed = False

    def execute(self):
        if self.item_id not in self.manager.items:
            raise ValueError("Item does not exist")
        if not self.manager.is_available(self.item_id):
            raise ValueError("Item already has an active loan")

        self.manager.items[self.item_id] = "loaned"
        self.manager.loans[self.item_id] = {
            "borrower": self.borrower,
            "due_date": self.due_date,
        }
        self.executed = True
        return f"{self.item_id} loaned to {self.borrower}"

    def undo(self):
        if not self.executed:
            raise ValueError("Cannot undo a loan that was not executed")
        self.manager.items[self.item_id] = "available"
        self.manager.loans.pop(self.item_id, None)
        self.executed = False
        return f"Loan undone. {self.item_id} is available again."


if __name__ == "__main__":
    manager1 = LibraryManager()
    manager1.reset()
    manager2 = LibraryManager()
    print("Same singleton object:", manager1 is manager2)

    command = LoanCommand("camera-1", "Aishu", date(2026, 11, 20), manager1)
    print(command.execute())
    print("Lookup through manager2:", manager2.items["camera-1"])
    print(command.undo())
    print("Available after undo:", manager1.is_available("camera-1"))
