import sqlite3

connection = sqlite3.connect('Tasks.db') # connect to SQLite and create a database file

# Create a cursor object
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT NOT NULL, 
        description TEXT, 
        due_date TEXT, 
        completed TEXT
    )  
''')

# Inserting data
tasks_data = [
    ('Making dinner', 'Roast potatoes and grilled salmon', 15/6/2025, 'YES'),
    ('Doing laundry', 'White clothes', 15/6/2025, 'NO')
]

cursor.executemany('''
    INSERT INTO tasks (title, description, due_date, completed)
    VALUES(?, ?, ?, ?)
''', tasks_data)

# Read data
print("\n--- Tasks ---")
cursor.execute('SELECT * FROM tasks')
for row in cursor.fetchall():
    print(row)

# Updating data
cursor.execute('''
    UPDATE tasks SET title = ? WHERE id = ?                 
''', ('Washing clothes', 4))

# Deleting data
cursor.execute("DELETE FROM tasks WHERE completed = NO")

# Saving changes and Close the connection to the database (only once )
connection.commit()
connection.close() 