P07 EXPENSE TRACKER — DAY 1 MILESTONE

Student name: TAMILELAN V
Register number: 7376252AL233
Project: P07 Expense Tracker

DAY 1 FEATURES IMPLEMENTED
- Core Python terminal menu.
- Expense data stored in expenses.txt using pipe-separated records.
- Automatic sequential expense IDs (E001, E002, ...).
- Date validation for DD-MM-YYYY, including leap-year checks.
- Positive amount validation with two decimal places.
- Category validation: Food, Travel, Books, Fees, Other.
- Load and save expenses using text files.
- Add an expense.
- List expenses between two dates.
- Edit an expense by ID.
- Delete an expense by ID with confirmation.
- Handles missing expenses.txt by starting with an empty collection.
- No imports, third-party packages, database, or datetime module.

NOT YET IMPLEMENTED IN DAY 1
- Monthly total and category-wise monthly report.
- Category percentage calculations.
- ASCII category chart.
- Highest single expense report.
- Set and enforce category spending limits.
These are planned for the next development stage.

RUNNING THE PROGRAM
1. Open a terminal in this folder.
2. Run: python3 expense_tracker.py
3. Follow the numbered menu.

DATA FORMAT
Each expense record is one line:
ID|DD-MM-YYYY|Category|Amount|Note

The pipe character is reserved as the field separator and is not allowed in notes.