import sqlite3
import bcrypt

def init_db():
    conn = sqlite3.connect("career.db")
    c = conn.cursor()
    
    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # Goals table
    c.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            goal TEXT NOT NULL,
            timeline TEXT,
            roadmap TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    # Progress table
    c.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()

def signup_user(name, email, password):
    conn = sqlite3.connect("career.db")
    c = conn.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                  (name, email, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = sqlite3.connect("career.db")
    c = conn.cursor()
    c.execute("SELECT id, name, password FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode(), user[2]):
        return {"id": user[0], "name": user[1]}
    return None

def save_goal(user_id, goal, timeline, roadmap):
    conn = sqlite3.connect("career.db")
    c = conn.cursor()
    c.execute("DELETE FROM goals WHERE user_id = ?", (user_id,))
    c.execute("INSERT INTO goals (user_id, goal, timeline, roadmap) VALUES (?, ?, ?, ?)",
              (user_id, goal, timeline, roadmap))
    conn.commit()
    conn.close()

def get_goal(user_id):
    conn = sqlite3.connect("career.db")
    c = conn.cursor()
    c.execute("SELECT goal, timeline, roadmap FROM goals WHERE user_id = ?", (user_id,))
    goal = c.fetchone()
    conn.close()
    return goal

def save_task(user_id, task):
    conn = sqlite3.connect("career.db")
    c = conn.cursor()
    c.execute("INSERT INTO progress (user_id, task) VALUES (?, ?)", (user_id, task))
    conn.commit()
    conn.close()

def get_tasks(user_id):
    conn = sqlite3.connect("career.db")
    c = conn.cursor()
    c.execute("SELECT id, task, completed FROM progress WHERE user_id = ?", (user_id,))
    tasks = c.fetchall()
    conn.close()
    return tasks

def update_task(task_id, completed):
    conn = sqlite3.connect("career.db")
    c = conn.cursor()
    c.execute("UPDATE progress SET completed = ? WHERE id = ?", (completed, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect("career.db")
    c = conn.cursor()
    c.execute("DELETE FROM progress WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()