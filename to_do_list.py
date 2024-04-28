import sqlite3
import os
from datetime import datetime

class Task:
    def __init__(self, title, description, priority, due_date=None, completed=False):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

class ToDoList:
    def __init__(self, db_file, user_id):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.user_id = user_id
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            title TEXT,
                            description TEXT,
                            priority TEXT,
                            due_date DATE,
                            completed INTEGER
                        )''')
        self.conn.commit()

    def add_task(self, task):
        try:
            self.cursor.execute('''INSERT INTO tasks (user_id, title, description, priority, due_date, completed)
                                VALUES (?, ?, ?, ?, ?, ?)''', (self.user_id, task.title, task.description, task.priority, task.due_date, 0))
            self.conn.commit()
            print("Task added successfully.")
        except sqlite3.Error as e:
            print(f"Error adding task: {e}")

    def remove_task(self, task_id):
        try:
            self.cursor.execute('''DELETE FROM tasks WHERE id=? AND user_id=?''', (task_id, self.user_id))
            self.conn.commit()
            print("Task removed successfully.")
        except sqlite3.Error as e:
            print(f"Error removing task: {e}")

    def mark_task_completed(self, task_id):
        try:
            self.cursor.execute('''UPDATE tasks SET completed=1 WHERE id=? AND user_id=?''', (task_id, self.user_id))
            self.conn.commit()
            print("Task marked as completed successfully.")
        except sqlite3.Error as e:
            print(f"Error marking task as completed: {e}")

    def get_tasks(self):
        try:
            self.cursor.execute('''SELECT * FROM tasks WHERE user_id=?''', (self.user_id,))
            rows = self.cursor.fetchall()
            tasks = []
            for row in rows:
                task = Task(row[2], row[3], row[4], row[5], row[6])
                tasks.append(task)
            return tasks
        except sqlite3.Error as e:
            print(f"Error fetching tasks: {e}")
            return []

    def close(self):
        self.conn.close()

def main():
    db_file = "tasks.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create users table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        password TEXT
                    )''')
    conn.commit()

    while True:
        print("\n== To-Do List Menu ==")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")

            try:
                cursor.execute('''SELECT id FROM users WHERE username=? AND password=?''', (username, password))
                user = cursor.fetchone()
                if user:
                    user_id = user[0]
                    todo_list = ToDoList(db_file, user_id)
                    while True:
                        print("\n== To-Do List Menu ==")
                        print("1. Add Task")
                        print("2. Remove Task")
                        print("3. Mark Task as Completed")
                        print("4. Display Tasks")
                        print("5. Save and Exit")
                        choice = input("Enter your choice: ")

                        if choice == "1":
                            title = input("Enter task title: ")
                            description = input("Enter task description: ")
                            priority = input("Enter task priority (High/Medium/Low): ")
                            due_date = input("Enter due date (YYYY-MM-DD) or leave empty: ")
                            if due_date:
                                due_date = datetime.strptime(due_date, '%Y-%m-%d')
                            task = Task(title, description, priority, due_date)
                            todo_list.add_task(task)
                        elif choice == "2":
                            tasks = todo_list.get_tasks()
                            for i, task in enumerate(tasks, start=1):
                                print(f"{i}. {task.title}")
                            task_index = int(input("Enter the index of the task to remove: "))
                            todo_list.remove_task(task_index)
                        elif choice == "3":
                            tasks = todo_list.get_tasks()
                            for i, task in enumerate(tasks, start=1):
                                print(f"{i}. {task.title}")
                            task_index = int(input("Enter the index of the task to mark as completed: "))
                            todo_list.mark_task_completed(task_index)
                        elif choice == "4":
                            tasks = todo_list.get_tasks()
                            for i, task in enumerate(tasks, start=1):
                                print(f"{i}. {task.title} - Priority: {task.priority} - Due Date: {task.due_date} - Completed: {task.completed}")
                        elif choice == "5":
                            todo_list.close()
                            print("Tasks saved successfully. Exiting...")
                            exit()
                        else:
                            print("Invalid choice. Please try again.")
                else:
                    print("Invalid username or password.")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        elif choice == "2":
            username = input("Enter new username: ")
            password = input("Enter new password: ")

            try:
                cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', (username, password))
                conn.commit()
                print("User registered successfully.")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()

if __name__ == "__main__":
    main()

