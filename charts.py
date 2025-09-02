# charts.py
# This file defines the ChartDialog class, which displays the charts using matplotlib.

from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime


class ChartDialog(QDialog):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.setWindowTitle("Spending Analysis")
        self.setGeometry(200, 200, 800, 600)
        self.setStyleSheet("background-color: #ffffff;")  # Simple background styling.

        # Create dropdowns for month and year.
        self.month_combo = QComboBox()
        self.month_combo.addItems(["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        self.year_combo = QComboBox()
        self.year_combo.addItems([str(y) for y in range(2020, 2031)])
        update_btn = QPushButton("Update Charts")
        update_btn.clicked.connect(self.update_charts)
        update_btn.setStyleSheet("padding: 5px; background-color: #4CAF50; color: white;")

        # Setup the matplotlib figure and canvas.
        self.figure = Figure(figsize=(8, 6), facecolor="#f9f9f9")
        self.canvas = FigureCanvas(self.figure)

        # Layout for the controls.
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("Month:"))
        control_layout.addWidget(self.month_combo)
        control_layout.addWidget(QLabel("Year:"))
        control_layout.addWidget(self.year_combo)
        control_layout.addWidget(update_btn)

        # Main layout.
        layout = QVBoxLayout()
        layout.addLayout(control_layout)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Default selections to current month and year.
        now = datetime.now()
        self.month_combo.setCurrentIndex(now.month - 1)
        self.year_combo.setCurrentText(str(now.year))
        self.update_charts()

    def update_charts(self):
        # Clear the previous charts.
        self.figure.clear()
        month = self.month_combo.currentIndex() + 1
        year = int(self.year_combo.currentText())
        categories, daily = self.manager.get_monthly_data(month, year)

        # Left subplot: Pie chart for spending by category.
        ax1 = self.figure.add_subplot(121)
        if categories:
            wedges, texts, autotexts = ax1.pie(
                categories.values(),
                labels=categories.keys(),
                autopct='%1.1f%%',
                startangle=140,
                shadow=True
            )
            for text in texts + autotexts:
                text.set_fontsize(9)
            ax1.set_title("Spending by Category", fontsize=11)
        else:
            ax1.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=12)

        # Right subplot: Line chart for daily spending.
        ax2 = self.figure.add_subplot(122)
        if daily:
            days = sorted(daily.keys())
            amounts = [daily[d] for d in days]
            ax2.plot(days, amounts, marker='o', linestyle='-', color='b', linewidth=2)
            ax2.set_xlabel("Day of Month", fontsize=10)
            ax2.set_ylabel("Amount Spent (€)", fontsize=10)
            ax2.set_title("Daily Spending", fontsize=11)
            ax2.grid(True, linestyle='--', alpha=0.7)
        else:
            ax2.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=12)

        self.canvas.draw()
