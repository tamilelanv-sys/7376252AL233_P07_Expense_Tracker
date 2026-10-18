# Name: TAMILELAN V
# Register Number: 7376252AL233
# Project: P07 Expense Tracker
# Day 1 milestone: validation, text-file storage, add/list/edit/delete expenses.

EXPENSE_FILE = "expenses.txt"
LIMIT_FILE = "limits.txt"
CATEGORIES = ["Food", "Travel", "Books", "Fees", "Other"]


def is_digits(value):
    if value == "":
        return False
    for character in value:
        if character < "0" or character > "9":
            return False
    return True


def parse_date(value):
    """Return (year, month, day) for a valid DD-MM-YYYY date, otherwise None."""
    parts = value.split("-")
    if len(parts) != 3:
        return None

    day_text, month_text, year_text = parts
    if len(day_text) != 2 or len(month_text) != 2 or len(year_text) != 4:
        return None
    if not is_digits(day_text) or not is_digits(month_text) or not is_digits(year_text):
        return None

    day = int(day_text)
    month = int(month_text)
    year = int(year_text)

    if year < 1 or month < 1 or month > 12:
        return None

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    leap_year = (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)
    if leap_year:
        days_in_month[1] = 29

    if day < 1 or day > days_in_month[month - 1]:
        return None
    return (year, month, day)


def read_date(prompt):
    while True:
        value = input(prompt).strip()
        if parse_date(value) is not None:
            return value
        print("Invalid date. Use a real date in DD-MM-YYYY format.")


def parse_amount_to_paise(value):
    """Parse a positive amount with up to two decimal places into integer paise."""
    value = value.strip()
    if value == "" or value.startswith("-") or value.startswith("+"):
        return None
    if value.count(".") > 1:
        return None

    parts = value.split(".")
    if len(parts) > 2 or parts[0] == "" or not is_digits(parts[0]):
        return None

    rupees = int(parts[0])
    paise = 0
    if len(parts) == 2:
        decimal_part = parts[1]
        if decimal_part == "" or not is_digits(decimal_part) or len(decimal_part) > 2:
            return None
        if len(decimal_part) == 1:
            decimal_part += "0"
        paise = int(decimal_part)

    total = rupees * 100 + paise
    if total <= 0:
        return None
    return total


def read_amount(prompt):
    while True:
        value = input(prompt).strip()
        amount = parse_amount_to_paise(value)
        if amount is not None:
            return amount
        print("Invalid amount. Enter a positive amount, such as 120 or 120.50.")


def format_money(paise):
    rupees = paise // 100
    remaining_paise = paise % 100
    if remaining_paise < 10:
        return "Rs. " + str(rupees) + ".0" + str(remaining_paise)
    return "Rs. " + str(rupees) + "." + str(remaining_paise)


def read_category():
    while True:
        print("Categories: Food, Travel, Books, Fees, Other")
        value = input("Category: ").strip().title()
        if value in CATEGORIES:
            return value
        print("Invalid category. Choose one of the listed categories.")


def read_note():
    while True:
        note = input("Short note: ").strip()
        if note == "":
            print("Note cannot be empty.")
        elif "|" in note or "\n" in note or "\r" in note:
            print("The note cannot contain the pipe character or a newline.")
        else:
            return note


def load_expenses():
    expenses = []
    try:
        file = open(EXPENSE_FILE, "r")
        lines = file.readlines()
        file.close()
    except FileNotFoundError:
        return expenses

    line_number = 0
    for line in lines:
        line_number += 1
        line = line.rstrip("\n\r")
        if line == "":
            continue
        fields = line.split("|")
        if len(fields) != 5:
            print("Warning: skipped malformed record on line " + str(line_number) + ".")
            continue

        expense_id, date, category, amount_text, note = fields
        amount = parse_amount_to_paise(amount_text)
        if (expense_id == "" or parse_date(date) is None or
                category not in CATEGORIES or amount is None or
                note == "" or "|" in note):
            print("Warning: skipped invalid record on line " + str(line_number) + ".")
            continue

        expenses.append({
            "id": expense_id,
            "date": date,
            "category": category,
            "amount": amount,
            "note": note
        })
    return expenses


def save_expenses(expenses):
    file = open(EXPENSE_FILE, "w")
    for expense in expenses:
        line = (
            expense["id"] + "|" + expense["date"] + "|" +
            expense["category"] + "|" +
            str(expense["amount"] // 100) + "." +
            ("0" if expense["amount"] % 100 < 10 else "") +
            str(expense["amount"] % 100) + "|" + expense["note"] + "\n"
        )
        file.write(line)
    file.close()


def generate_id(expenses):
    largest_number = 0
    for expense in expenses:
        expense_id = expense["id"]
        if len(expense_id) > 1 and expense_id[0] == "E" and is_digits(expense_id[1:]):
            number = int(expense_id[1:])
            if number > largest_number:
                largest_number = number
    return "E" + str(largest_number + 1).zfill(3)


def find_expense_index(expenses, expense_id):
    index = 0
    while index < len(expenses):
        if expenses[index]["id"].lower() == expense_id.lower():
            return index
        index += 1
    return -1


def display_expense(expense):
    print(
        expense["id"] + " | " + expense["date"] + " | " +
        expense["category"] + " | " + format_money(expense["amount"]) +
        " | " + expense["note"]
    )


def add_expense(expenses):
    print("\n--- Add Expense ---")
    date = read_date("Date (DD-MM-YYYY): ")
    category = read_category()
    amount = read_amount("Amount in rupees: ")
    note = read_note()

    expense = {
        "id": generate_id(expenses),
        "date": date,
        "category": category,
        "amount": amount,
        "note": note
    }
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense saved:")
    display_expense(expense)


def list_expenses_between_dates(expenses):
    print("\n--- List Expenses by Date Range ---")
    start_date = read_date("Start date (DD-MM-YYYY): ")
    end_date = read_date("End date (DD-MM-YYYY): ")
    if parse_date(start_date) > parse_date(end_date):
        print("Start date cannot be later than end date.")
        return

    start_key = parse_date(start_date)
    end_key = parse_date(end_date)
    matches = []
    for expense in expenses:
        date_key = parse_date(expense["date"])
        if start_key <= date_key <= end_key:
            matches.append(expense)

    if len(matches) == 0:
        print("No expenses found in that date range.")
        return

    print("\nID | Date | Category | Amount | Note")
    print("-" * 72)
    for expense in matches:
        display_expense(expense)
    print("Records found: " + str(len(matches)))


def edit_expense(expenses):
    print("\n--- Edit Expense ---")
    expense_id = input("Enter expense ID to edit: ").strip()
    index = find_expense_index(expenses, expense_id)
    if index == -1:
        print("Expense ID not found.")
        return

    current = expenses[index]
    print("Current record:")
    display_expense(current)
    print("Enter the new values below.")
    new_date = read_date("New date (DD-MM-YYYY): ")
    new_category = read_category()
    new_amount = read_amount("New amount in rupees: ")
    new_note = read_note()

    expenses[index] = {
        "id": current["id"],
        "date": new_date,
        "category": new_category,
        "amount": new_amount,
        "note": new_note
    }
    save_expenses(expenses)
    print("Expense updated:")
    display_expense(expenses[index])


def delete_expense(expenses):
    print("\n--- Delete Expense ---")
    expense_id = input("Enter expense ID to delete: ").strip()
    index = find_expense_index(expenses, expense_id)
    if index == -1:
        print("Expense ID not found.")
        return

    print("Selected record:")
    display_expense(expenses[index])
    confirmation = input("Type YES to confirm deletion: ").strip()
    if confirmation != "YES":
        print("Deletion cancelled.")
        return

    del expenses[index]
    save_expenses(expenses)
    print("Expense deleted and file updated.")


def show_menu():
    print("\n====================================")
    print("         EXPENSE TRACKER")
    print("====================================")
    print("1. Add expense")
    print("2. List expenses by date range")
    print("3. Edit expense")
    print("4. Delete expense")
    print("5. Exit")
    print("====================================")


def main():
    expenses = load_expenses()
    print("Expense Tracker — Day 1 build")
    print("Loaded " + str(len(expenses)) + " valid expense record(s).")

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            list_expenses_between_dates(expenses)
        elif choice == "3":
            edit_expense(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            save_expenses(expenses)
            print("Data saved. Goodbye.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
