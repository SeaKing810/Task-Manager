import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    due_date TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                 )''')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_task(title, description, status, user_id, category="Uncategorized", due_date=None):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO tasks (title, description, status, created_at, user_id, category, due_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (title, description, status, created_at, user_id, category, due_date))
    conn.commit()
    conn.close()

def get_all_tasks(user_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_task(task_id, user_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
    task = c.fetchone()
    conn.close()
    return task

def update_task(task_id, title, description, status, user_id, category, due_date):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET title = ?, description = ?, status = ?, category = ?, due_date = ? WHERE id = ? AND user_id = ?",
              (title, description, status, category, due_date, task_id, user_id))
    conn.commit()
    conn.close()

def delete_task(task_id, user_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
    conn.commit()
    conn.close()