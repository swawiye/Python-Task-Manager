import sqlite3

connection = sqlite3.connect('Tasks.db') # connect to SQLite and create a database file

# Create a cursor object
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT, 
        description TEXT, 
        due_date DATE, 
        completed TEXT
    )  
''')