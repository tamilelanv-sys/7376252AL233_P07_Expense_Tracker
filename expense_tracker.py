# Name: TAMILELAN V
# Register Number: 7376252AL233
# Project: P07 - Expense Tracker

DATA_FILE = "expenses.txt"
LIMIT_FILE = "limits.txt"
CATEGORIES = ["Food", "Travel", "Books", "Fees", "Other"]


def read_text(prompt, max_length=100, allow_empty=False):
    while True:
        value = input(prompt).strip()
        if allow_empty and value == "":
            return value
        if not value:
            print("Input cannot be empty.")
        elif "|" in value:
            print("The | character is reserved as a file separator.")
        elif len(value) > max_length:
            print("Maximum length:", max_length)
        else:
            return value


def read_int(prompt, low=None, high=None):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            number = int(value)
            if low is not None and number < low:
                print("Minimum value:", low)
            elif high is not None and number > high:
                print("Maximum value:", high)
            else:
                return number
        else:
            print("Enter a whole number.")


def parse_amount(value):
    if not value or "|" in value or value.count(".") > 1:
        return None
    parts = value.split(".")
    whole = parts[0]
    decimal = parts[1] if len(parts) == 2 else ""
    if not whole.isdigit():
        return None
    if decimal and (not decimal.isdigit() or len(decimal) > 2):
        return None
    amount = int(whole) * 100 + (int((decimal + "00")[:2]) if decimal else 0)
    return amount if amount > 0 else None


def read_amount(prompt):
    while True:
        value = input(prompt).strip()
        amount = parse_amount(value)
        if amount is not None:
            return amount
        print("Enter a positive amount, e.g. 250 or 250.50.")


def money(amount):
    return "Rs. " + str(amount // 100) + "." + ("0" if amount % 100 < 10 else "") + str(amount % 100)


def leap_year(year):
    return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)


def valid_date(value):
    if len(value) != 10 or value[2] != "-" or value[5] != "-":
        return False
    d, m, y = value[:2], value[3:5], value[6:]
    if not (d.isdigit() and m.isdigit() and y.isdigit()):
        return False
    day, month, year = int(d), int(m), int(y)
    if year < 1 or month < 1 or month > 12:
        return False
    days = [31, 29 if leap_year(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return 1 <= day <= days[month - 1]


def read_date(prompt):
    while True:
        value = input(prompt).strip()
        if valid_date(value):
            return value
        print("Invalid date. Use DD-MM-YYYY, e.g. 07-10-2026.")


def date_key(value):
    return int(value[6:] + value[3:5] + value[:2])


def load_expenses():
    records = []
    try:
        handle = open(DATA_FILE, "r")
        for line in handle:
            fields = line.rstrip("\n").split("|")
            if len(fields) != 5:
                continue
            eid, date, category, amount, note = fields
            if valid_date(date) and category in CATEGORIES and amount.isdigit() and int(amount) > 0:
                records.append({"id": eid, "date": date, "category": category,
                                "amount": int(amount), "note": note})
        handle.close()
    except FileNotFoundError:
        save_expenses(records)
    return records


def save_expenses(records):
    handle = open(DATA_FILE, "w")
    for item in records:
        handle.write(item["id"] + "|" + item["date"] + "|" + item["category"] + "|" +
                     str(item["amount"]) + "|" + item["note"] + "\n")
    handle.close()


def load_limits():
    limits = {}
    try:
        handle = open(LIMIT_FILE, "r")
        for line in handle:
            fields = line.rstrip("\n").split("|")
            if len(fields) == 2 and fields[0] in CATEGORIES and fields[1].isdigit():
                limits[fields[0]] = int(fields[1])
        handle.close()
    except FileNotFoundError:
        save_limits(limits)
    return limits


def save_limits(limits):
    handle = open(LIMIT_FILE, "w")
    for category in CATEGORIES:
        if category in limits:
            handle.write(category + "|" + str(limits[category]) + "\n")
    handle.close()


def next_id(records):
    highest = 0
    for item in records:
        eid = item["id"]
        if eid.startswith("E") and eid[1:].isdigit():
            highest = max(highest, int(eid[1:]))
    return "E" + ("000" + str(highest + 1))[-3:]


def choose_category():
    for index, category in enumerate(CATEGORIES, 1):
        print(str(index) + ". " + category)
    return CATEGORIES[read_int("Choose category: ", 1, len(CATEGORIES)) - 1]


def month_year(date):
    return int(date[3:5]), int(date[6:])


def month_name(month):
    names = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]
    return names[month - 1]


def month_records(records, month, year):
    return [item for item in records if month_year(item["date"]) == (month, year)]


def total_for_category(records, category):
    return sum(item["amount"] for item in records if item["category"] == category)


def warn_limit(records, limits, category, date):
    month, year = month_year(date)
    if category not in limits:
        return
    spent = total_for_category(month_records(records, month, year), category)
    limit = limits[category]
    if spent > limit:
        print("WARNING:", category, "monthly limit exceeded. Spent:", money(spent),
              "| Limit:", money(limit))
    elif spent == limit:
        print("Notice:", category, "monthly limit reached.")


def print_record(item):
    print("{:<6} {:<12} {:<10} {:>12}  {}".format(
        item["id"], item["date"], item["category"], money(item["amount"]), item["note"]))


def add_expense(records, limits):
    print("\n--- Add Expense ---")
    date = read_date("Date (DD-MM-YYYY): ")
    category = choose_category()
    amount = read_amount("Amount (Rs.): ")
    note = read_text("Short note: ", 100)
    item = {"id": next_id(records), "date": date, "category": category,
            "amount": amount, "note": note}
    records.append(item)
    save_expenses(records)
    print("Saved. Expense ID:", item["id"])
    warn_limit(records, limits, category, date)


def list_expenses(records):
    print("\n--- All Expenses ---")
    if not records:
        print("No expenses recorded.")
        return
    print("{:<6} {:<12} {:<10} {:>12}  {}".format("ID", "Date", "Category", "Amount", "Note"))
    for item in sorted(records, key=lambda row: date_key(row["date"])):
        print_record(item)
    print("Records:", len(records), "| Total:", money(sum(x["amount"] for x in records)))


def monthly_total(records):
    print("\n--- Monthly Total ---")
    month = read_int("Month (1-12): ", 1, 12)
    year = read_int("Year: ", 1, 9999)
    selected = month_records(records, month, year)
    print(month_name(month), year, "| Expenses:", len(selected),
          "| Total:", money(sum(x["amount"] for x in selected)))


def category_report(records):
    print("\n--- Category Breakdown ---")
    month = read_int("Month (1-12): ", 1, 12)
    year = read_int("Year: ", 1, 9999)
    selected = month_records(records, month, year)
    total = sum(x["amount"] for x in selected)
    print(month_name(month), year, "spending:", money(total))
    if total == 0:
        print("No expenses found.")
        return
    for category in CATEGORIES:
        amount = total_for_category(selected, category)
        percentage = amount * 100.0 / total
        bars = amount * 20 // total          # one '#' for every 5%
        print("{:<8} {:>14} {:>6.1f}%  {}".format(
            category, money(amount), percentage, "#" * bars))


def highest_expense(records):
    print("\n--- Highest Single Expense ---")
    if not records:
        print("No expenses recorded.")
        return
    item = max(records, key=lambda row: row["amount"])
    print("ID:", item["id"], "| Date:", item["date"], "| Category:", item["category"])
    print("Amount:", money(item["amount"]), "| Note:", item["note"])


def set_limit(records, limits):
    print("\n--- Set Monthly Category Limit ---")
    category = choose_category()
    limits[category] = read_amount("Monthly limit (Rs.): ")
    save_limits(limits)
    month = read_int("Check month (1-12): ", 1, 12)
    year = read_int("Check year: ", 1, 9999)
    spent = total_for_category(month_records(records, month, year), category)
    limit = limits[category]
    print("Limit:", money(limit), "| Spent:", money(spent))
    if spent > limit:
        print("WARNING: Over limit by", money(spent - limit))
    else:
        print("Remaining:", money(limit - spent))


def find_record(records, eid):
    for item in records:
        if item["id"].upper() == eid.upper():
            return item
    return None


def edit_expense(records, limits):
    print("\n--- Edit Expense ---")
    item = find_record(records, read_text("Expense ID: ", 20))
    if item is None:
        print("Expense ID not found.")
        return
    print_record(item)
    value = input("New date [Enter to keep {}]: ".format(item["date"])).strip()
    if value:
        if valid_date(value):
            item["date"] = value
        else:
            print("Invalid date; old date retained.")
    print("Current category:", item["category"])
    if input("Change category? (y/n): ").strip().lower() == "y":
        item["category"] = choose_category()
    value = input("New amount in Rs. [Enter to keep]: ").strip()
    if value:
        amount = parse_amount(value)
        if amount is None:
            print("Invalid amount; old amount retained.")
        else:
            item["amount"] = amount
    value = input("New note [Enter to keep]: ").strip()
    if value:
        if "|" not in value and len(value) <= 100:
            item["note"] = value
        else:
            print("Invalid note; old note retained.")
    save_expenses(records)
    print("Expense updated.")
    warn_limit(records, limits, item["category"], item["date"])


def delete_expense(records):
    print("\n--- Delete Expense ---")
    eid = read_text("Expense ID: ", 20)
    item = find_record(records, eid)
    if item is None:
        print("Expense ID not found.")
        return
    print_record(item)
    if input("Confirm delete? (y/n): ").strip().lower() == "y":
        records.remove(item)
        save_expenses(records)
        print("Expense deleted.")
    else:
        print("Deletion cancelled.")


def date_range_report(records):
    print("\n--- Expenses Between Dates ---")
    start = read_date("Start date (DD-MM-YYYY): ")
    end = read_date("End date (DD-MM-YYYY): ")
    if date_key(start) > date_key(end):
        print("Start date must be on or before end date.")
        return
    selected = [item for item in records
                if date_key(start) <= date_key(item["date"]) <= date_key(end)]
    selected.sort(key=lambda row: date_key(row["date"]))
    if not selected:
        print("No expenses found in this range.")
        return
    for item in selected:
        print_record(item)
    print("Count:", len(selected), "| Total:", money(sum(x["amount"] for x in selected)))


def show_limits(limits):
    print("\n--- Monthly Category Limits ---")
    found = False
    for category in CATEGORIES:
        if category in limits:
            print(category + ":", money(limits[category]))
            found = True
    if not found:
        print("No limits set.")


def show_menu():
    print("\n========== P07 EXPENSE TRACKER ==========")
    print("1. Add expense")
    print("2. List all expenses")
    print("3. Monthly total")
    print("4. Category-wise monthly breakdown")
    print("5. Highest single expense")
    print("6. Set category spending limit")
    print("7. Edit expense by ID")
    print("8. Delete expense by ID")
    print("9. List expenses between two dates")
    print("10. Show saved limits")
    print("0. Save and exit")


def main():
    records = load_expenses()
    limits = load_limits()
    print("Loaded", len(records), "expense record(s).")
    while True:
        show_menu()
        choice = read_int("Choose an option: ", 0, 10)
        if choice == 1:
            add_expense(records, limits)
        elif choice == 2:
            list_expenses(records)
        elif choice == 3:
            monthly_total(records)
        elif choice == 4:
            category_report(records)
        elif choice == 5:
            highest_expense(records)
        elif choice == 6:
            set_limit(records, limits)
        elif choice == 7:
            edit_expense(records, limits)
        elif choice == 8:
            delete_expense(records)
        elif choice == 9:
            date_range_report(records)
        elif choice == 10:
            show_limits(limits)
        else:
            save_expenses(records)
            save_limits(limits)
            print("Data saved. Goodbye.")
            break
        input("\nPress Enter to return to the menu...")


if __name__ == "__main__":
    main()
