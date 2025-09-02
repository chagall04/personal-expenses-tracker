# models.py
# This file contains the data model classes.

class Expense:
    def __init__(self, date, category, amount, description, method):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description
        self.method = method

    def to_dict(self):
        # Convert the expense into a dictionary for JSON storage.
        return {
            'date': self.date,
            'category': self.category,
            'amount': self.amount,
            'description': self.description,
            'method': self.method
        }

class ExpenseDecorator:
    def __init__(self, expense):
        self.expense = expense

    def get_priority(self):
        # Return a priority tag based on the expense amount.
        if self.expense.amount > 300:
            return "❗High"
        elif self.expense.amount > 100:
            return "⚠️Medium"
        return "✅Low"
