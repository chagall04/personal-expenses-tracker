# manager.py
# This file handles file operations and data management.

import json
import csv
from datetime import datetime
from models import Expense

class ExpenseManager:
    def __init__(self, filename='expenses.txt'):
        self.filename = filename
        self.expenses = []
        self.load_data()

    def load_data(self):
        # Load expenses from a JSON file; start with an empty list if file doesn't exist.
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.expenses = [Expense(**item) for item in data]
        except FileNotFoundError:
            self.expenses = []

    def save_data(self):
        # Save the list of expenses as JSON.
        with open(self.filename, 'w') as f:
            json.dump([expense.to_dict() for expense in self.expenses], f)

    def get_summary(self):
        # Calculate total spent, average expense, and the most common category.
        if not self.expenses:
            return {'total': 0, 'average': 0, 'common_category': 'N/A'}
        total = sum(e.amount for e in self.expenses)
        average = total / len(self.expenses)
        categories = [e.category for e in self.expenses]
        return {
            'total': total,
            'average': average,
            'common_category': max(set(categories), key=categories.count)
        }

    def export_csv(self):
        # Export expense data to a CSV file.
        with open('expenses.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Category', 'Amount', 'Description', 'Method'])
            for e in self.expenses:
                writer.writerow([e.date, e.category, e.amount, e.description, e.method])

    def get_monthly_data(self, month, year):
        # Filter expenses by month and year.
        monthly_expenses = [e for e in self.expenses
                           if datetime.strptime(e.date, "%Y-%m-%d").month == month
                           and datetime.strptime(e.date, "%Y-%m-%d").year == year]
        # Sum expenses by category.
        categories = {}
        for e in monthly_expenses:
            categories[e.category] = categories.get(e.category, 0) + e.amount
        # Sum expenses by day.
        daily_spending = {}
        for e in monthly_expenses:
            day = datetime.strptime(e.date, "%Y-%m-%d").day
            daily_spending[day] = daily_spending.get(day, 0) + e.amount
        return categories, daily_spending
