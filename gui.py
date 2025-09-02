# gui.py
# This file defines the main GUI for the Expense Tracker application.

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QPushButton, QLineEdit, QLabel, QComboBox,
                             QMessageBox)
from datetime import datetime
from manager import ExpenseManager
from models import Expense, ExpenseDecorator
from charts import ChartDialog


class ExpenseGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.manager = ExpenseManager()
        self.initUI()
        self.load_table()

    def initUI(self):
        self.setWindowTitle("Expense Tracker")
        self.setGeometry(100, 100, 800, 500)

        # Create input fields.
        self.date_field = QLineEdit(datetime.now().strftime("%Y-%m-%d"))
        self.category_field = QComboBox()
        self.category_field.addItems([
            "Food", "Transport", "Utilities", "Entertainment",
            "Health", "Education", "Shopping", "Others"
        ])
        self.amount_field = QLineEdit()
        self.desc_field = QLineEdit()
        self.method_field = QComboBox()
        self.method_field.addItems(["Cash", "Card", "Online"])

        # Create buttons for actions.
        add_btn = QPushButton("Add Expense")
        add_btn.clicked.connect(self.add_expense)
        del_btn = QPushButton("Delete")
        del_btn.clicked.connect(self.delete_expense)
        summary_btn = QPushButton("Show Summary")
        summary_btn.clicked.connect(self.show_summary)
        export_btn = QPushButton("Export CSV")
        export_btn.clicked.connect(self.manager.export_csv)
        viz_btn = QPushButton("View Charts")
        viz_btn.clicked.connect(self.show_charts)

        # Apply simple styling to buttons.
        for btn in [add_btn, del_btn, summary_btn, export_btn, viz_btn]:
            btn.setStyleSheet("padding: 5px; background-color: #4CAF50; color: white;")

        # Dropdown for filtering by category.
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            "All", "Food", "Transport", "Utilities", "Entertainment",
            "Health", "Education", "Shopping", "Others"
        ])
        self.filter_combo.currentTextChanged.connect(self.load_table)

        # Table to display expense records.
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Date", "Category", "Amount", "Description", "Method"])

        # Layout for the input area.
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Date (YYYY-MM-DD):"))
        input_layout.addWidget(self.date_field)
        input_layout.addWidget(QLabel("Category:"))
        input_layout.addWidget(self.category_field)
        input_layout.addWidget(QLabel("Amount:"))
        input_layout.addWidget(self.amount_field)
        input_layout.addWidget(QLabel("Description:"))
        input_layout.addWidget(self.desc_field)
        input_layout.addWidget(QLabel("Payment Method:"))
        input_layout.addWidget(self.method_field)
        input_layout.addWidget(add_btn)
        input_layout.addWidget(del_btn)
        input_layout.addWidget(QLabel("Filter Category:"))
        input_layout.addWidget(self.filter_combo)
        input_layout.addWidget(summary_btn)
        input_layout.addWidget(export_btn)
        input_layout.addWidget(viz_btn)

        # Main layout combines the input area and the table.
        main_layout = QHBoxLayout()
        main_layout.addLayout(input_layout, 1)
        main_layout.addWidget(self.table, 2)

        container = QWidget()
        container.setLayout(main_layout)
        container.setStyleSheet("background-color: #f9f9f9;")
        self.setCentralWidget(container)

    def load_table(self):
        # Load expenses into the table based on the selected filter.
        filtered = [
            e for e in self.manager.expenses
            if self.filter_combo.currentText() == "All"
               or e.category == self.filter_combo.currentText()
        ]
        self.table.setRowCount(len(filtered))
        for row, expense in enumerate(filtered):
            decorated = ExpenseDecorator(expense)
            self.table.setItem(row, 0, QTableWidgetItem(expense.date))
            self.table.setItem(row, 1, QTableWidgetItem(expense.category))
            self.table.setItem(row, 2, QTableWidgetItem(f"€{expense.amount:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{expense.description}\n{decorated.get_priority()}"))
            self.table.setItem(row, 4, QTableWidgetItem(expense.method))

    def validate_date(self, date_text):
        # Check if the date is in the correct format.
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def add_expense(self):
        # Add a new expense after validating input.
        if not self.validate_date(self.date_field.text()):
            QMessageBox.warning(self, "Error", "Invalid date format!")
            return
        try:
            new_expense = Expense(
                self.date_field.text(),
                self.category_field.currentText(),
                float(self.amount_field.text()),
                self.desc_field.text(),
                self.method_field.currentText()
            )
            self.manager.expenses.append(new_expense)
            self.manager.save_data()
            self.load_table()
            self.amount_field.clear()
            self.desc_field.clear()
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid amount entered")

    def delete_expense(self):
        # Delete the selected expense.
        selected = self.table.currentRow()
        if selected >= 0:
            del self.manager.expenses[selected]
            self.manager.save_data()
            self.load_table()

    def show_summary(self):
        # Show a summary of spending statistics.
        summary = self.manager.get_summary()
        msg = (f"Total Spent: €{summary['total']:.2f}\n"
               f"Average Expense: €{summary['average']:.2f}\n"
               f"Most Common Category: {summary['common_category']}")
        QMessageBox.information(self, "Summary", msg)

    def show_charts(self):
        # Open the chart dialog.
        dialog = ChartDialog(self.manager)
        dialog.exec_()


if __name__ == "__main__":
    app = QApplication([])
    window = ExpenseGUI()
    window.show()
    app.exec()
