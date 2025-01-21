import sqlite3 
import requests
import tkinter as tk
from tkinter import messagebox, ttk
import time

# Initialize the database
def initialize_database():
    connection = sqlite3.connect("college_feedback.db")
    cursor = connection.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT CHECK(role IN ('student', 'admin'))
    )
    """)

    # Create feedback table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        environment TEXT,
        infrastructure TEXT,
        faculty TEXT,
        hostel TEXT,
        library TEXT,
        playground TEXT,
        fest TEXT
    )
    """)

    # Insert default admin
    cursor.execute("""
    INSERT OR IGNORE INTO users (username, password, role)
    VALUES (?, ?, ?)
    """, ("admin", "admin123", "admin"))

    connection.commit()
    connection.close()

# Function to handle database connection with retry for locked database
def execute_db_query(query, params=()):
    retry_count = 5
    while retry_count > 0:
        try:
            connection = sqlite3.connect("college_feedback.db")
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            connection.close()
            return cursor
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e):
                retry_count -= 1
                time.sleep(0.5)  # Wait before retrying
            else:
                raise
    raise Exception("Database is locked. Please try again later.")

# Main App Class
class CollegeFeedbackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("College Feedback System")
        self.root.geometry("600x400")
        self.root.configure(bg="aqua")
        self.create_account_page()

    # Create account page
    def create_account_page(self):
        self.clear_window()

        title = tk.Label(self.root, text="Create Account", font=("Arial", 20), bg="aqua")
        title.pack(pady=20)

        tk.Label(self.root, text="Username:", bg="aqua").pack(pady=5)
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password:", bg="aqua").pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        tk.Label(self.root, text="Role (student/admin):", bg="aqua").pack(pady=5)
        role_var = tk.StringVar(value="student")
        role_menu = ttk.Combobox(self.root, textvariable=role_var, values=["student", "admin"], state="readonly")
        role_menu.pack()

        def create_account():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            role = role_var.get().lower()

            if not username or not password:
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                execute_db_query("""
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
                """, (username, password, role))
                messagebox.showinfo("Success", "Account created successfully! Redirecting to login.")
                self.login_page()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists.")

        tk.Button(self.root, text="Create Account", command=create_account).pack(pady=20)
        tk.Button(self.root, text="Go to Login", command=self.login_page).pack()

    # Login page
    def login_page(self):
        self.clear_window()

        title = tk.Label(self.root, text="Login", font=("Arial", 20), bg="aqua")
        title.pack(pady=20)

        tk.Label(self.root, text="Username:", bg="aqua").pack(pady=5)
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password:", bg="aqua").pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            connection = sqlite3.connect("college_feedback.db")
            cursor = connection.cursor()
            cursor.execute("""
            SELECT role FROM users WHERE username = ? AND password = ?
            """, (username, password))
            user = cursor.fetchone()
            connection.close()

            if user:
                role = user[0]
                messagebox.showinfo("Success", f"Welcome, {role}!")
                if role == "student":
                    self.feedback_page(username)
                elif role == "admin":
                    self.admin_page()
            else:
                messagebox.showerror("Error", "Invalid credentials.")

        tk.Button(self.root, text="Login", command=login).pack(pady=20)
        tk.Button(self.root, text="Create Account", command=self.create_account_page).pack()

    # Feedback page for students
    def feedback_page(self, username):
        self.clear_window()

        title = tk.Label(self.root, text="Submit Feedback", font=("Arial", 20), bg="aqua")
        title.pack(pady=20)

        fields = ["Environment", "Infrastructure", "Faculty", "Hostel", "Library", "Playground", "Fest"]
        entries = {}

        for field in fields:
            tk.Label(self.root, text=f"{field}:", bg="aqua").pack(pady=5)
            entry = tk.Entry(self.root)
            entry.pack()
            entries[field.lower()] = entry

        def submit_feedback():
            feedback_data = {field: entry.get().strip() for field, entry in entries.items()}
            if any(not value for value in feedback_data.values()):
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                execute_db_query("""
                INSERT INTO feedback (username, environment, infrastructure, faculty, hostel, library, playground, fest)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (username, *feedback_data.values()))
                messagebox.showinfo("Success", "Feedback submitted successfully!")
                self.main_menu()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        tk.Button(self.root, text="Submit Feedback", command=submit_feedback).pack(pady=20)

    # Admin page to view feedback
    def admin_page(self):
        self.clear_window()

        title = tk.Label(self.root, text="Admin Dashboard", font=("Arial", 20), bg="aqua")
        title.pack(pady=20)

        feedback_list = tk.Listbox(self.root, width=80, height=20)
        feedback_list.pack(pady=20)

        connection = sqlite3.connect("college_feedback.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM feedback")
        feedbacks = cursor.fetchall()
        connection.close()

        for feedback in feedbacks:
            feedback_list.insert(tk.END, feedback)

        def clear_data():
            result = messagebox.askyesno("Confirm", "Are you sure you want to delete all feedback data?")
            if result:
                execute_db_query("DELETE FROM feedback")
                feedback_list.delete(0, tk.END)
                messagebox.showinfo("Success", "All feedback data has been cleared.")

        tk.Button(self.root, text="Clear Data", command=clear_data).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.login_page).pack()

    # Quotes page
    def quotes_page(self):
        self.clear_window()

        title = tk.Label(self.root, text="Inspirational Quotes", font=("Arial", 20), bg="aqua")
        title.pack(pady=20)

        quote_label = tk.Label(self.root, text="", wraplength=500, justify="center", bg="aqua")
        quote_label.pack(pady=20)

        def fetch_quote():
            try:
                response = requests.get("https://zenquotes.io/api/random")
                if response.status_code == 200:
                    data = response.json()
                    quote_label.config(text=f'"{data[0]["q"]}"\n\n- {data[0]["a"]}')
                else:
                    quote_label.config(text="Failed to fetch quote.")
            except Exception as e:
                quote_label.config(text=f"Error: {e}")

        fetch_quote()
        tk.Button(self.root, text="New Quote", command=fetch_quote).pack(pady=20)
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack()

    # Main menu
    def main_menu(self):
        self.clear_window()

        title = tk.Label(self.root, text="Main Menu", font=("Arial", 20), bg="aqua")
        title.pack(pady=20)

        tk.Button(self.root, text="Submit Feedback", command=lambda: self.feedback_page("student"), width=20).pack(pady=10)
        tk.Button(self.root, text="Inspirational Quotes", command=self.quotes_page, width=20).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.login_page, width=20).pack(pady=10)

    # Clear window
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    initialize_database()
    root = tk.Tk()
    app = CollegeFeedbackApp(root)
    root.mainloop()
