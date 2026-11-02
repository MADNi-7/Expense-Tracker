# Expense Tracker

A simple Python expense tracker — college mini-project.

## Features
- Add expenses (date, amount, category, description)
- View all expenses in a formatted table
- Filter by category or month
- Summary by category with percentages
- Delete an expense by ID
- Export to CSV
- Data persists in `expenses.json`

## How to run
```
python expense_tracker.py
```

Requires Python 3.6+. Uses only the standard library (`json`, `csv`, `datetime`, `os`).

## Sample session
```
========== EXPENSE TRACKER ==========
1. Add expense
2. View all expenses
3. Filter expenses
4. Summary by category
5. Delete expense
6. Export to CSV
7. Exit
Choose an option: 1

--- Add New Expense ---
Date (YYYY-MM-DD, blank = today):
Amount: 250
Category (food/transport/books/rent/other): food
Description: Lunch at mess
Added expense #1: Rs. 250.0 on food
```

## Files
- `expense_tracker.py` — main program
- `expenses.json` — created automatically to store data
- `expenses_export.csv` — created when you export
