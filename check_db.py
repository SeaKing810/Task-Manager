import sqlite3

conn = sqlite3.connect('tasks.db')
c = conn.cursor()
c.execute("SELECT * FROM tasks")
tasks = c.fetchall()
for task in tasks:
    print(f"Task ID: {task[0]}, Title: {task[1]}, Due Date: {task[6]}")
conn.close()