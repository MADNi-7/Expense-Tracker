"""
Expense Tracker
A simple command-line expense tracker that stores expenses in a JSON file.
Features: add, view, filter by category/month, summary, delete, export to CSV.
"""

import json
import csv
import os
from datetime import datetime

DATA_FILE = "expenses.json"


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses):
    print("\n--- Add New Expense ---")
    date_input = input("Date (YYYY-MM-DD, blank = today): ").strip()
    if not date_input:
        date = datetime.now().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            date = date_input
        except ValueError:
            print("Invalid date format. Using today.")
            date = datetime.now().strftime("%Y-%m-%d")

    try:
        amount = float(input("Amount: ").strip())
    except ValueError:
        print("Invalid amount. Expense not added.")
        return

    category = input("Category (food/transport/books/rent/other): ").strip().lower() or "other"
    description = input("Description: ").strip()

    expense = {
        "id": (max((e["id"] for e in expenses), default=0) + 1),
        "date": date,
        "amount": amount,
        "category": category,
        "description": description,
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Added expense #{expense['id']}: Rs. {amount} on {category}")


def view_expenses(expenses, items=None):
    items = items if items is not None else expenses
    if not items:
        print("\nNo expenses to show.")
        return
    print("\n" + "-" * 70)
    print(f"{'ID':<4}{'Date':<12}{'Category':<14}{'Amount':>10}  Description")
    print("-" * 70)
    for e in items:
        print(f"{e['id']:<4}{e['date']:<12}{e['category']:<14}{e['amount']:>10.2f}  {e['description']}")
    print("-" * 70)
    print(f"Total: Rs. {sum(e['amount'] for e in items):.2f}  ({len(items)} entries)")


def filter_expenses(expenses):
    print("\n--- Filter Expenses ---")
    print("1. By category")
    print("2. By month (YYYY-MM)")
    choice = input("Choose: ").strip()
    if choice == "1":
        cat = input("Category: ").strip().lower()
        view_expenses(expenses, [e for e in expenses if e["category"] == cat])
    elif choice == "2":
        month = input("Month (YYYY-MM): ").strip()
        view_expenses(expenses, [e for e in expenses if e["date"].startswith(month)])
    else:
        print("Invalid choice.")


def summary(expenses):
    if not expenses:
        print("\nNo expenses yet.")
        return
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    grand = sum(totals.values())
    print("\n--- Summary by Category ---")
    print(f"{'Category':<15}{'Amount':>12}{'Percent':>10}")
    print("-" * 37)
    for cat, amt in sorted(totals.items(), key=lambda x: -x[1]):
        pct = (amt / grand) * 100 if grand else 0
        print(f"{cat:<15}{amt:>12.2f}{pct:>9.1f}%")
    print("-" * 37)
    print(f"{'TOTAL':<15}{grand:>12.2f}")


def delete_expense(expenses):
    try:
        eid = int(input("\nEnter ID to delete: ").strip())
    except ValueError:
        print("Invalid ID.")
        return
    for i, e in enumerate(expenses):
        if e["id"] == eid:
            removed = expenses.pop(i)
            save_expenses(expenses)
            print(f"Deleted expense #{eid} ({removed['description']}).")
            return
    print(f"No expense with ID {eid}.")


def export_csv(expenses):
    if not expenses:
        print("Nothing to export.")
        return
    filename = "expenses_export.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "date", "category", "amount", "description"])
        writer.writeheader()
        writer.writerows(expenses)
    print(f"Exported {len(expenses)} expenses to {filename}")


def menu():
    expenses = load_expenses()
    actions = {
        "1": ("Add expense", lambda: add_expense(expenses)),
        "2": ("View all expenses", lambda: view_expenses(expenses)),
        "3": ("Filter expenses", lambda: filter_expenses(expenses)),
        "4": ("Summary by category", lambda: summary(expenses)),
        "5": ("Delete expense", lambda: delete_expense(expenses)),
        "6": ("Export to CSV", lambda: export_csv(expenses)),
        "7": ("Exit", None),
    }
    while True:
        print("\n========== EXPENSE TRACKER ==========")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        choice = input("Choose an option: ").strip()
        if choice == "7":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action[1]()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()
