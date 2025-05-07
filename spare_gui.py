import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Database Setup
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('university.db')
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Students table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            full_name TEXT NOT NULL,
            roll_number TEXT UNIQUE,
            department TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        
        # Teachers table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            full_name TEXT NOT NULL,
            department TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')
        
        # Courses table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            credits INTEGER,
            department TEXT
        )
        ''')
        
        # Enrollments table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            teacher_id INTEGER NOT NULL,
            semester TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id),
            FOREIGN KEY (teacher_id) REFERENCES teachers(id)
        )
        ''')
        
        # Grades table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment_id INTEGER NOT NULL,
            grade TEXT,
            remarks TEXT,
            FOREIGN KEY (enrollment_id) REFERENCES enrollments(id)
        )
        ''')
        
        # Attendance table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            enrollment_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (enrollment_id) REFERENCES enrollments(id)
        )
        ''')
        
        self.conn.commit()
    
    def execute_query(self, query, params=(), fetch=False):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        self.conn.commit()
        return None
    
    def add_sample_data(self):
        # Add admin user if not exists
        if not self.execute_query("SELECT * FROM users WHERE username=?", ("admin",), fetch=True):
            self.execute_query(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ("admin", "admin123", "admin")
            )
        
        # Add some sample students, teachers, and courses
        # (Implementation omitted for brevity)
        pass

# Authentication Service
class AuthService:
    def __init__(self, db):
        self.db = db
    
    def login(self, username, password):
        user = self.db.execute_query(
            "SELECT id, username, role FROM users WHERE username=? AND password=?",
            (username, password),
            fetch=True
        )
        return user[0] if user else None
    
    def register_student(self, username, password, full_name, roll_number, department):
        try:
            # First create user
            self.db.execute_query(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, "student")
            )
            user_id = self.db.execute_query("SELECT last_insert_rowid()", fetch=True)[0][0]
            
            # Then create student
            self.db.execute_query(
                "INSERT INTO students (user_id, full_name, roll_number, department) VALUES (?, ?, ?, ?)",
                (user_id, full_name, roll_number, department)
            )
            return True
        except sqlite3.IntegrityError:
            return False

# Main Application
class UniversityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("University Management System")
        self.root.geometry("1200x700")
        
        self.db = Database()
        self.auth = AuthService(self.db)
        self.current_user = None
        
        self.show_login_screen()
    
    def show_login_screen(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding="30")
        frame.pack(expand=True)
        
        ttk.Label(frame, text="University Login", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(frame, text="Username:").grid(row=1, column=0, sticky='e', pady=5)
        self.username_entry = ttk.Entry(frame)
        self.username_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame, text="Password:").grid(row=2, column=0, sticky='e', pady=5)
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)
        
        ttk.Button(frame, text="Login", command=self.handle_login).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Only show register button for demo purposes
        ttk.Button(frame, text="Register Student", command=self.show_register_screen).grid(row=4, column=0, columnspan=2)
    
    def show_register_screen(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding="30")
        frame.pack(expand=True)
        
        ttk.Label(frame, text="Student Registration", font=('Arial', 16)).grid(row=0, column=0, columnspan=2, pady=20)
        
        fields = [
            ("Username:", "username_entry"),
            ("Password:", "password_entry"),
            ("Full Name:", "full_name_entry"),
            ("Roll Number:", "roll_number_entry"),
            ("Department:", "department_entry")
        ]
        
        for i, (label_text, var_name) in enumerate(fields, start=1):
            ttk.Label(frame, text=label_text).grid(row=i, column=0, sticky='e', pady=5)
            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, pady=5)
            setattr(self, var_name, entry)
        
        ttk.Button(frame, text="Register", command=self.handle_register).grid(row=len(fields)+1, column=0, pady=20)
        ttk.Button(frame, text="Back to Login", command=self.show_login_screen).grid(row=len(fields)+1, column=1, pady=20)
    
    def handle_register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        full_name = self.full_name_entry.get()
        roll_number = self.roll_number_entry.get()
        department = self.department_entry.get()
        
        if not all([username, password, full_name, roll_number, department]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        if self.auth.register_student(username, password, full_name, roll_number, department):
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login_screen()
        else:
            messagebox.showerror("Error", "Username or roll number already exists")
    
    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        user = self.auth.login(username, password)
        if user:
            self.current_user = {
                'id': user[0],
                'username': user[1],
                'role': user[2]
            }
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def show_dashboard(self):
        self.clear_window()
        
        if self.current_user['role'] == 'admin':
            self.show_admin_dashboard()
        elif self.current_user['role'] == 'teacher':
            self.show_teacher_dashboard()
        else:
            self.show_student_dashboard()
    
    def show_admin_dashboard(self):
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(
            header_frame, 
            text=f"Admin Dashboard - Welcome {self.current_user['username']}",
            font=('Arial', 14)
        ).pack(side='left')
        
        ttk.Button(
            header_frame, 
            text="Logout", 
            command=self.show_login_screen
        ).pack(side='right')
        
        # Stats frame
        stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding=10)
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # Get stats from database
        student_count = self.db.execute_query(
            "SELECT COUNT(*) FROM students", fetch=True
        )[0][0]
        
        teacher_count = self.db.execute_query(
            "SELECT COUNT(*) FROM teachers", fetch=True
        )[0][0]
        
        course_count = self.db.execute_query(
            "SELECT COUNT(*) FROM courses", fetch=True
        )[0][0]
        
        # Display stats
        stats = [
            ("Total Students", student_count),
            ("Total Teachers", teacher_count),
            ("Total Courses", course_count)
        ]
        
        for i, (label, value) in enumerate(stats):
            ttk.Label(stats_frame, text=label).grid(row=0, column=i*2, padx=5)
            ttk.Label(stats_frame, text=str(value), font=('Arial', 14, 'bold')).grid(row=0, column=i*2+1, padx=5)
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Students tab
        students_tab = ttk.Frame(notebook)
        notebook.add(students_tab, text="Manage Students")
        
        # Treeview for students
        columns = ("ID", "Full Name", "Roll Number", "Department")
        self.students_tree = ttk.Treeview(
            students_tab, columns=columns, show='headings'
        )
        
        for col in columns:
            self.students_tree.heading(col, text=col)
            self.students_tree.column(col, width=150)
        
        self.students_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Buttons for student management
        btn_frame = ttk.Frame(students_tab)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Add Student", 
            command=self.show_add_student_dialog
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Edit Student", 
            command=self.show_edit_student_dialog
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Delete Student", 
            command=self.delete_student
        ).pack(side='left', padx=5)
        
        # Load students data
        self.load_students_data()
        
        # Teachers tab (similar to students tab)
        teachers_tab = ttk.Frame(notebook)
        notebook.add(teachers_tab, text="Manage Teachers")
        
        # Courses tab (similar to students tab)
        courses_tab = ttk.Frame(notebook)
        notebook.add(courses_tab, text="Manage Courses")
        
        # Reports tab
        reports_tab = ttk.Frame(notebook)
        notebook.add(reports_tab, text="Reports")
    
    def show_student_dashboard(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        # Get student info
        student = self.db.execute_query(
            "SELECT full_name, roll_number, department FROM students WHERE user_id=?",
            (self.current_user['id'],),
            fetch=True
        )[0]
        
        ttk.Label(
            header_frame, 
            text=f"Student Dashboard - {student[0]} ({student[1]}) - {student[2]}",
            font=('Arial', 14)
        ).pack(side='left')
        
        ttk.Button(
            header_frame, 
            text="Logout", 
            command=self.show_login_screen
        ).pack(side='right')
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Courses tab
        courses_tab = ttk.Frame(notebook)
        notebook.add(courses_tab, text="My Courses")
        
        # Attendance tab
        attendance_tab = ttk.Frame(notebook)
        notebook.add(attendance_tab, text="Attendance")
        
        # Grades tab
        grades_tab = ttk.Frame(notebook)
        notebook.add(grades_tab, text="Grades")
    
    def show_teacher_dashboard(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', padx=20, pady=10)
        
        # Get teacher info
        teacher = self.db.execute_query(
            "SELECT full_name, department FROM teachers WHERE user_id=?",
            (self.current_user['id'],),
            fetch=True
        )[0]
        
        ttk.Label(
            header_frame, 
            text=f"Teacher Dashboard - {teacher[0]} - {teacher[1]}",
            font=('Arial', 14)
        ).pack(side='left')
        
        ttk.Button(
            header_frame, 
            text="Logout", 
            command=self.show_login_screen
        ).pack(side='right')
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Classes tab
        classes_tab = ttk.Frame(notebook)
        notebook.add(classes_tab, text="My Classes")
        
        # Students tab
        students_tab = ttk.Frame(notebook)
        notebook.add(students_tab, text="Students")
        
        # Grade entry tab
        grades_tab = ttk.Frame(notebook)
        notebook.add(grades_tab, text="Grade Entry")
    
    def load_students_data(self):
        # Clear existing data
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        
        # Fetch students from database
        students = self.db.execute_query(
            "SELECT id, full_name, roll_number, department FROM students",
            fetch=True
        )
        
        # Add to treeview
        for student in students:
            self.students_tree.insert('', 'end', values=student)
    
    def show_add_student_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("400x300")
        
        fields = [
            ("Username:", "username"),
            ("Password:", "password"),
            ("Full Name:", "full_name"),
            ("Roll Number:", "roll_number"),
            ("Department:", "department")
        ]
        
        entries = {}
        for i, (label, name) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            entry = ttk.Entry(dialog)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky='w')
            entries[name] = entry
        
        def save_student():
            data = {name: entry.get() for name, entry in entries.items()}
            
            if not all(data.values()):
                messagebox.showerror("Error", "All fields are required")
                return
            
            try:
                # First create user
                self.db.execute_query(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (data['username'], data['password'], 'student')
                )
                user_id = self.db.execute_query("SELECT last_insert_rowid()", fetch=True)[0][0]
                
                # Then create student
                self.db.execute_query(
                    "INSERT INTO students (user_id, full_name, roll_number, department) VALUES (?, ?, ?, ?)",
                    (user_id, data['full_name'], data['roll_number'], data['department'])
                )
                
                messagebox.showinfo("Success", "Student added successfully")
                self.load_students_data()
                dialog.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username or roll number already exists")
        
        ttk.Button(dialog, text="Save", command=save_student).grid(row=len(fields), column=0, columnspan=2, pady=10)
    
    def show_edit_student_dialog(self):
        selected = self.students_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to edit")
            return
        
        student_id = self.students_tree.item(selected[0])['values'][0]
        
        # Fetch student data
        student = self.db.execute_query(
            '''SELECT u.username, s.full_name, s.roll_number, s.department 
            FROM students s JOIN users u ON s.user_id = u.id 
            WHERE s.id=?''',
            (student_id,),
            fetch=True
        )[0]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Student")
        dialog.geometry("400x300")
        
        fields = [
            ("Username:", "username", student[0]),
            ("Password:", "password", ""),
            ("Full Name:", "full_name", student[1]),
            ("Roll Number:", "roll_number", student[2]),
            ("Department:", "department", student[3])
        ]
        
        entries = {}
        for i, (label, name, value) in enumerate(fields):
            ttk.Label(dialog, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            entry = ttk.Entry(dialog)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky='w')
            entries[name] = entry
        
        def update_student():
            data = {name: entry.get() for name, entry in entries.items()}
            
            if not all(data.values()):
                messagebox.showerror("Error", "All fields are required")
                return
            
            try:
                # Update user
                if data['password']:
                    self.db.execute_query(
                        "UPDATE users SET username=?, password=? WHERE id=(SELECT user_id FROM students WHERE id=?)",
                        (data['username'], data['password'], student_id)
                    )
                else:
                    self.db.execute_query(
                        "UPDATE users SET username=? WHERE id=(SELECT user_id FROM students WHERE id=?)",
                        (data['username'], student_id)
                    )
                
                # Update student
                self.db.execute_query(
                    "UPDATE students SET full_name=?, roll_number=?, department=? WHERE id=?",
                    (data['full_name'], data['roll_number'], data['department'], student_id)
                )
                
                messagebox.showinfo("Success", "Student updated successfully")
                self.load_students_data()
                dialog.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username or roll number already exists")
        
        ttk.Button(dialog, text="Update", command=update_student).grid(row=len(fields), column=0, columnspan=2, pady=10)
    
    def delete_student(self):
        selected = self.students_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to delete")
            return
        
        student_id = self.students_tree.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this student?"):
            # First get user_id to delete from users table
            user_id = self.db.execute_query(
                "SELECT user_id FROM students WHERE id=?",
                (student_id,),
                fetch=True
            )[0][0]
            
            # Delete student
            self.db.execute_query("DELETE FROM students WHERE id=?", (student_id,))
            
            # Delete user
            self.db.execute_query("DELETE FROM users WHERE id=?", (user_id,))
            
            messagebox.showinfo("Success", "Student deleted successfully")
            self.load_students_data()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversityApp(root)
    root.mainloop()
