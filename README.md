# Media Library Loan Management

A small Python prototype demonstrating:
- Singleton `LibraryManager` for shared loan state.
- Command pattern using `LoanCommand.execute()` and `undo()`.
- Prevention of a second active loan for the same item.
- Overdue reminder generation.
- Unit tests using Python's `unittest` module.

Run the demo: `python library.py`

Run tests: `python -m unittest -v`
