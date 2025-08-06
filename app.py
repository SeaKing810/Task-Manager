import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import date
from database import init_db, add_user, get_user_by_username, add_task, get_all_tasks, get_task, update_task, delete_task

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Replace with a secure key in production
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        user = get_user_by_username(user[1])
        if user:
            return User(user[0], user[1])
    return None

def get_user_by_id(user_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # In production, hash passwords
        try:
            add_user(username, password)
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and user[2] == password:  # In production, compare hashed passwords
            login_user(User(user[0], user[1]))
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()  # Clear session data
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    tasks = get_all_tasks(current_user.id)
    today = date.today().strftime("%Y-%m-%d")
    return render_template('index.html', tasks=tasks, query='', today=today)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        category = request.form['category']
        due_date_input = request.form.get('due_date', '')
        if due_date_input and due_date_input.strip():
            due_date = due_date_input.strip()
        else:
            due_date = None
        print(f"Adding task - Title: {title}, Description: {description}, Status: {status}, Category: {category}, Due Date Input: {due_date_input}, Due Date: {due_date}, User ID: {current_user.id}")
        add_task(title, description, status, current_user.id, due_date, category)  # Swapped category and due_date
        flash('Task added successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    task = get_task(task_id, current_user.id)
    if not task:
        flash('Task not found.', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        category = request.form['category']
        due_date_input = request.form.get('due_date', '')
        if due_date_input and due_date_input.strip():
            due_date = due_date_input.strip()
        else:
            due_date = None
        print(f"Editing task {task_id} - Title: {title}, Description: {description}, Status: {status}, Category: {category}, Due Date Input: {due_date_input}, Due Date: {due_date}, User ID: {current_user.id}")
        update_task(task_id, title, description, status, current_user.id, due_date, category)  # Swapped category and due_date
        flash('Task updated successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)

@app.route('/delete/<int:task_id>')
@login_required
def delete(task_id):
    task = get_task(task_id, current_user.id)
    if task:
        delete_task(task_id, current_user.id)
        flash('Task deleted successfully.', 'success')
    else:
        flash('Task not found.', 'danger')
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        query = request.form['query']
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE user_id = ? AND (title LIKE ? OR description LIKE ?)",
                  (current_user.id, f'%{query}%', f'%{query}%'))
        tasks = c.fetchall()
        conn.close()
        return render_template('index.html', tasks=tasks, query=query, today=date.today().strftime("%Y-%m-%d"))
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)