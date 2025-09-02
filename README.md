# Personal Expense Tracker

Description

This project is a desktop application designed to help users efficiently manage their day-to-day spending. It allows users to add, edit, and delete expense records, which are saved permanently to a file. Upon launching, the application loads all saved data into a user-friendly graphical interface for easy management.

Key Features

Manage Expenses: Add, edit, and delete individual expense records, each with a date, category, amount, description, and payment method.

Data Persistence: All expense data is permanently stored in a local file, ensuring your records are saved between sessions.

Data Analysis: Filter expenses by category and view summary statistics, including total spent, average expense, and the most common expense category.

Data Visualization: Generate graphical charts for specific months, including a pie chart breaking down expenses by category and a line chart showing daily spending trends.

Export Functionality: Export all expense data to a CSV file for easy sharing or use in other applications like Excel or Google Sheets.

Technologies Used

    Python 3

    PyQt5 (for the graphical user interface)

    Matplotlib (for data visualization and charts)

## How to Run

1.  **Prerequisites**
    * Make sure you have Python 3 installed on your system.

2.  **Clone the Repository**
    ```sh
    git clone [https://github.com/chagall04/personal-expense-tracker.git](https://github.com/chagall04/personal-expense-tracker.git)
    ```

3.  **Navigate to the Project Directory**
    ```sh
    cd personal-expense-tracker
    ```

4.  **Install Dependencies**
    * It is recommended to create a virtual environment first.
    * Install the required libraries using the `requirements.txt` file:
    ```sh
    pip install -r requirements.txt
    ```

5.  **Run the Application**
    ```sh
    python main.py
    ```
