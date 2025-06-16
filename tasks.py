import sqlite3
import csv

database = "Tasks.db"

# Define a Task class to encapsulate all task-related behavior
class Task:
    def __init__(self, id=None, title="", description="", due_date=None, completed=False):
        # Initialize a task object
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed

    @staticmethod # A static method is a method which is bound to the class and not the object of the class. It can’t access or modify class state.
    def initialize_db():
        # Create the tasks table if it doesn't exist
        with sqlite3.connect(database) as conn: # connect to SQLite and create a database file
            c = conn.cursor() # Create a cursor object
            c.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT,
                    completed INTEGER DEFAULT 0  -- 0 for incomplete, 1 for complete
                )
            ''')
            conn.commit()

    @staticmethod
    def seed_initial_data():
        # Insert sample data only if the table is empty
        with sqlite3.connect(database) as conn:
            c = conn.cursor()
            c.execute('SELECT COUNT(*) FROM tasks')
            if c.fetchone()[0] == 0: #fetchone() - retrieve only the first row from the table, and iterate through it
                tasks_data = [
                    ("Making dinner", "Roast potatoes and grilled salmon", "2025-06-15", 1),
                    ("Doing laundry", "White clothes", "2025-06-15", 0)
                ]
                c.executemany('''
                    INSERT INTO tasks (title, description, due_date, completed)
                    VALUES (?, ?, ?, ?)
                ''', tasks_data)
                conn.commit()

    def save(self):
        # Save the current task to the database
        with sqlite3.connect(database) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO tasks (title, description, due_date, completed)
                VALUES (?, ?, ?, ?)
            ''', (self.title, self.description, self.due_date, int(self.completed)))
            conn.commit()

    @staticmethod
    def get_all():
        # Retrieve all tasks from the database, sorted by completion and due date
        with sqlite3.connect(database) as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM tasks') # ORDER BY completed, due_date
            rows = c.fetchall()
            return [Task(*row) for row in rows]  # Return list of Task objects

    @staticmethod
    def mark_complete(task_id):
        # Mark a task as complete (set completed to 1)
        with sqlite3.connect(database) as conn:
            c = conn.cursor()
            c.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
            conn.commit()

    @staticmethod
    def delete(task_id):
        # Delete a task by its ID
        with sqlite3.connect(database) as conn:
            c = conn.cursor()
            c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            conn.commit()

    @staticmethod
    def export_to_csv(filename="tasks_export.csv"):
        # Export all tasks to a CSV file
        tasks = Task.get_all()
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Title", "Description", "Due Date", "Completed"])
            for t in tasks:
                writer.writerow([t.id, t.title, t.description, t.due_date, "Yes" if t.completed else "No"])

    def __str__(self):
        # Nicely format task display for the CLI
        return f"{self.id:<3} | {self.title:<20} | {self.description:<30} | {self.due_date:<10} | {'✅' if self.completed else '❌'}"

# CLI Functions 
def print_tasks(tasks):
    # Print a list of tasks in tabular format
    print("\nID  | Title                | Description                   | Due Date  | Completed")
    print("-" * 80)
    for task in tasks:
        print(task)
    print()

def add_task():
    # Prompt user for task details and add it to the database
    title = input("Enter title: ")
    description = input("Enter description: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    task = Task(title=title, description=description, due_date=due_date)
    task.save()
    print("Task added!")

def view_tasks():
    # Retrieve and display all tasks
    tasks = Task.get_all()
    print_tasks(tasks)

def mark_complete():
    # Prompt for a task ID and mark it as completed
    task_id = int(input("Enter task ID to mark as complete: "))
    Task.mark_complete(task_id)
    print("Task marked as complete!")

def delete_task():
    # Prompt for a task ID and delete it
    task_id = int(input("Enter task ID to delete: "))
    Task.delete(task_id)
    print("Task deleted!")

def export_tasks():
    # Export tasks to a CSV file
    Task.export_to_csv()
    print("Tasks exported to tasks_export.csv")

