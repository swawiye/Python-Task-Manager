import sqlite3 #for tha database
from datetime import datetime
import csv

Database = "tasks.db"


class Task:
    def __init__(self, id=None, title="", description="", due_date=None, completed=False):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed

    @staticmethod
    def initialize_db():
        with sqlite3.connect(Database) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT,
                    completed INTEGER DEFAULT 0
                )
            ''')
            conn.commit()

    def save(self):
        with sqlite3.connect(Database) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO tasks (title, description, due_date, completed)
                VALUES (?, ?, ?, ?)
            ''', (self.title, self.description, self.due_date, int(self.completed)))
            conn.commit()

    @staticmethod
    def get_all():
        with sqlite3.connect(Database) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM tasks ORDER BY completed, due_date')
            rows = c.fetchall()
            return [Task(*row) for row in rows]

    @staticmethod
    def mark_complete(task_id):
        with sqlite3.connect(Database) as conn:
            c = conn.cursor()
            c.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
            conn.commit()

    @staticmethod
    def delete(task_id):
        with sqlite3.connect(Database) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()

    @staticmethod
    def export_to_csv(filename="tasks_export.csv"):
        tasks = Task.get_all()
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Title", "Description", "Due Date", "Completed"])
            for t in tasks:
                writer.writerow([t.id, t.title, t.description, t.due_date, "Yes" if t.completed else "No"])

    def __str__(self):
        return f"{self.id:<3} | {self.title:<20} | {self.description:<30} | {self.due_date:<10} | {'✔' if self.completed else '✘'}"


# -------- CLI Functions --------
def print_tasks(tasks):
    print("\nID  | Title                | Description                   | Due Date  | Completed")
    print("-" * 80)
    for task in tasks:
        print(task)
    print()


def add_task():
    title = input("Enter title: ")
    description = input("Enter description: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    task = Task(title=title, description=description, due_date=due_date)
    task.save()
    print("Task added!")


def view_tasks():
    tasks = Task.get_all()
    print_tasks(tasks)


def mark_complete():
    task_id = int(input("Enter task ID to mark as complete: "))
    Task.mark_complete(task_id)
    print("Task marked as complete!")


def delete_task():
    task_id = int(input("Enter task ID to delete: "))
    Task.delete(task_id)
    print("Task deleted!")


def export_tasks():
    Task.export_to_csv()
    print("Tasks exported to tasks_export.csv")


# -------- Main Program --------
def main():
    Task.initialize_db()

    while True:
        print("\n===== Task Manager =====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Complete")
        print("4. Delete Task")
        print("5. Export to CSV")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            mark_complete()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            export_tasks()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
