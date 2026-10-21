P07 - EXPENSE TRACKER | COMPLETE TWO-DAY VERSION
=================================================

Name: TAMILELAN V
Register number: 7376252AL233
Project number: P07

RUN
---
Open a terminal in this folder and run:
    python3 expense_tracker.py

RULES AND IMPLEMENTATION
------------------------
- Python 3; no imports or third-party packages.
- No database; data is stored in pipe-delimited .txt files.
- No eval() or exec().
- Dates are manually validated in DD-MM-YYYY format, including leap years.
- Amounts are stored as integer paise to avoid floating-point errors.
- Do not type the | character in notes because it separates file fields.
- Data files are created automatically if missing.

FEATURES
--------
1. Add expenses with automatic IDs.
2. Validate date, category, note, and positive amount.
3. List all expenses and calculate the overall total.
4. Monthly spending total.
5. Monthly category breakdown with amount, percentage, and # bar
   (approximately one # per Rs. 5; non-zero categories get at least one #).
6. Highest single expense with date and category.
7. Save monthly spending limits by category and warn when reached/exceeded.
8. Edit an expense by ID.
9. Delete an expense by ID after confirmation.
10. List expenses within an inclusive date range.
11. Persist expenses and limits across program runs.

FILES
-----
expense_tracker.py : application
expenses.txt        : 10 sample records
limits.txt          : sample category limits
README.txt          : documentation
sample_run.txt      : illustrative sample terminal session

DATA FORMAT
-----------
expenses.txt: ID|DD-MM-YYYY|Category|AmountInPaise|ShortNote
limits.txt:   Category|MonthlyLimitInPaise
