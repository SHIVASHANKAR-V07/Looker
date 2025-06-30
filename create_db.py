import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('Shiva', '12345'))

conn.commit()
conn.close()

print("Database and default user created.")
