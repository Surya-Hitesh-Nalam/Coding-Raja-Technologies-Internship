import sqlite3
from datetime import datetime

class BudgetTracker:
    def __init__(self, username):
        self.username = username
        self.conn = sqlite3.connect(f'{username}_budget_tracker.db')
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                category TEXT,
                                budget_limit REAL
                            )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                budget_id INTEGER,
                                type TEXT,
                                amount REAL,
                                category TEXT,
                                tags TEXT,
                                date DATE
                            )''')
        self.conn.commit()

    def create_budget(self, name, category, limit):
        try:
            self.cursor.execute('''INSERT INTO budgets (name, category, budget_limit) VALUES (?, ?, ?)''', (name, category, limit))
            self.conn.commit()
            print("Budget created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating budget: {e}")

    def add_transaction(self, budget_id, trans_type, amount, category, tags=None, date=None):
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        try:
            self.cursor.execute('''INSERT INTO transactions (budget_id, type, amount, category, tags, date)
                                VALUES (?, ?, ?, ?, ?, ?)''', (budget_id, trans_type, amount, category, tags, date))
            self.conn.commit()
            print("Transaction added successfully.")
        except sqlite3.Error as e:
            print(f"Error adding transaction: {e}")

    def calculate_remaining_budget(self, budget_id):
        try:
            self.cursor.execute('''SELECT budget_limit FROM budgets WHERE id=?''', (budget_id,))
            budget_limit = self.cursor.fetchone()[0]
            self.cursor.execute('''SELECT SUM(amount) FROM transactions WHERE budget_id=? AND type='expense' ''', (budget_id,))
            expenses = self.cursor.fetchone()[0] or 0
            remaining_budget = budget_limit - expenses
            print(f"Remaining Budget for Budget ID {budget_id}: {remaining_budget}")
        except sqlite3.Error as e:
            print(f"Error calculating remaining budget: {e}")

    def expense_analysis(self, budget_id):
        try:
            self.cursor.execute('''SELECT category, SUM(amount) FROM transactions WHERE budget_id=? AND type='expense' GROUP BY category''', (budget_id,))
            expenses_by_category = self.cursor.fetchall()
            print("Expense Analysis:")
            for category, total_amount in expenses_by_category:
                print(f"{category}: {total_amount}")
        except sqlite3.Error as e:
            print(f"Error performing expense analysis: {e}")

    def generate_report(self, budget_id, start_date, end_date):
        try:
            self.cursor.execute('''SELECT * FROM transactions WHERE budget_id=? AND date BETWEEN ? AND ?''', (budget_id, start_date, end_date))
            rows = self.cursor.fetchall()
            print("Report Generated Successfully:")
            for row in rows:
                print(row)
        except sqlite3.Error as e:
            print(f"Error generating report: {e}")

    def close(self):
        self.conn.close()

def main():
    print("Welcome to Budget Tracker!")

    # User Authentication
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    # Perform authentication here...

    # Create a Budget Tracker instance for the authenticated user
    budget_tracker = BudgetTracker(username)

    while True:
        print("\n== Budget Tracker Menu ==")
        print("1. Create Budget")
        print("2. Add Transaction")
        print("3. Calculate Remaining Budget")
        print("4. Expense Analysis")
        print("5. Generate Report")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter budget name: ")
            category = input("Enter budget category: ")
            limit = float(input("Enter budget limit: "))
            budget_tracker.create_budget(name, category, limit)
        elif choice == "2":
            budget_id = int(input("Enter budget ID: "))
            trans_type = input("Enter transaction type (expense/income): ")
            amount = float(input("Enter transaction amount: "))
            category = input("Enter transaction category: ")
            tags = input("Enter transaction tags (comma-separated): ").split(',') if input("Do you want to add tags? (y/n): ").lower() == 'y' else None
            budget_tracker.add_transaction(budget_id, trans_type, amount, category, tags)
        elif choice == "3":
            budget_id = int(input("Enter budget ID: "))
            budget_tracker.calculate_remaining_budget(budget_id)
        elif choice == "4":
            budget_id = int(input("Enter budget ID: "))
            budget_tracker.expense_analysis(budget_id)
        elif choice == "5":
            budget_id = int(input("Enter budget ID: "))
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            budget_tracker.generate_report(budget_id, start_date, end_date)
        elif choice == "6":
            budget_tracker.close()
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
