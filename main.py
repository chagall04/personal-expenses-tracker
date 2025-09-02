# main.py
# Entry point for the Expense Tracker application.

from gui import ExpenseGUI
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    window = ExpenseGUI()
    window.show()
    app.exec()
