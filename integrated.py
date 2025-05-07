import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod

# Database Setup
def setup_database():
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                      user_id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      role TEXT NOT NULL,
                      email TEXT UNIQUE NOT NULL,
                      password TEXT NOT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Students (
                      student_id INTEGER PRIMARY KEY,
                      name TEXT NOT NULL,
                      major TEXT NOT NULL,
                      email TEXT UNIQUE NOT NULL,
                      FOREIGN KEY (student_id) REFERENCES Users(user_id))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Professors (
                      professor_id TEXT PRIMARY KEY,
                      name TEXT NOT NULL,
                      department TEXT NOT NULL,
                      email TEXT UNIQUE NOT NULL,
                      FOREIGN KEY (professor_id) REFERENCES Users(user_id))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Admins (
                      admin_id TEXT PRIMARY KEY,
                      name TEXT NOT NULL,
                      role TEXT NOT NULL,
                      contact_info TEXT,
                      FOREIGN KEY (admin_id) REFERENCES Users(user_id))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Courses (
                      course_id TEXT PRIMARY KEY,
                      course_name TEXT NOT NULL,
                      department TEXT NOT NULL,
                      credits INTEGER,
                      professor_id TEXT,
                      FOREIGN KEY (professor_id) REFERENCES Professors(professor_id))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Enrollments (
                      enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                      student_id INTEGER,
                      course_id TEXT,
                      grade REAL,
                      FOREIGN KEY (student_id) REFERENCES Students(student_id),
                      FOREIGN KEY (course_id) REFERENCES Courses(course_id),
                      UNIQUE(student_id, course_id))''')
    
    conn.commit()
    conn.close()

setup_database()

# GUI Application
class UniversityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("University Management System")
        self.root.geometry("1000x700")
        
        self.current_user = None
        self.create_login_frame()
    
    def create_login_frame(self):
        self.clear_frame()
        
        frame = Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)
        
        Label(frame, text="Login", font=('Arial', 20)).grid(row=0, column=0, columnspan=2, pady=20)
        
        Label(frame, text="Email:").grid(row=1, column=0, sticky='e', pady=5)
        self.email_entry = Entry(frame, width=30)
        self.email_entry.grid(row=1, column=1, pady=5)
        
        Label(frame, text="Password:").grid(row=2, column=0, sticky='e', pady=5)
        self.password_entry = Entry(frame, width=30, show='*')
        self.password_entry.grid(row=2, column=1, pady=5)
        
        Button(frame, text="Login", command=self.handle_login).grid(row=3, column=0, columnspan=2, pady=20)
        
        # Add registration button for demo purposes
        Button(frame, text="Register New User", command=self.create_registration_frame).grid(row=4, column=0, columnspan=2, pady=10)
    
    def create_registration_frame(self):
        self.clear_frame()
        
        frame = Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True)
        
        Label(frame, text="Register New User", font=('Arial', 20)).grid(row=0, column=0, columnspan=2, pady=20)
        
        # Role selection
        Label(frame, text="Role:").grid(row=1, column=0, sticky='e', pady=5)
        self.role_var = StringVar(value="student")
        OptionMenu(frame, self.role_var, "student", "professor", "admin").grid(row=1, column=1, sticky='w', pady=5)
        
        # Common fields
        Label(frame, text="Name:").grid(row=2, column=0, sticky='e', pady=5)
        self.reg_name_entry = Entry(frame, width=30)
        self.reg_name_entry.grid(row=2, column=1, pady=5)
        
        Label(frame, text="Email:").grid(row=3, column=0, sticky='e', pady=5)
        self.reg_email_entry = Entry(frame, width=30)
        self.reg_email_entry.grid(row=3, column=1, pady=5)
        
        Label(frame, text="Password:").grid(row=4, column=0, sticky='e', pady=5)
        self.reg_password_entry = Entry(frame, width=30, show='*')
        self.reg_password_entry.grid(row=4, column=1, pady=5)
        
        # Role-specific fields
        self.role_fields_frame = Frame(frame)
        self.role_fields_frame.grid(row=5, column=0, columnspan=2, pady=10)
        self.update_role_fields()
        
        self.role_var.trace('w', lambda *args: self.update_role_fields())
        
        Button(frame, text="Register", command=self.handle_registration).grid(row=6, column=0, pady=20, padx=5)
        Button(frame, text="Back to Login", command=self.create_login_frame).grid(row=6, column=1, pady=20, padx=5)
    
    def update_role_fields(self):
        for widget in self.role_fields_frame.winfo_children():
            widget.destroy()
        
        role = self.role_var.get()
        
        if role == "student":
            Label(self.role_fields_frame, text="Student ID (6 digits):").grid(row=0, column=0, sticky='e', pady=5)
            self.student_id_entry = Entry(self.role_fields_frame, width=30)
            self.student_id_entry.grid(row=0, column=1, pady=5)
            
            Label(self.role_fields_frame, text="Major:").grid(row=1, column=0, sticky='e', pady=5)
            self.major_entry = Entry(self.role_fields_frame, width=30)
            self.major_entry.grid(row=1, column=1, pady=5)
        
        elif role == "professor":
            Label(self.role_fields_frame, text="Professor ID:").grid(row=0, column=0, sticky='e', pady=5)
            self.prof_id_entry = Entry(self.role_fields_frame, width=30)
            self.prof_id_entry.grid(row=0, column=1, pady=5)
            
            Label(self.role_fields_frame, text="Department:").grid(row=1, column=0, sticky='e', pady=5)
            self.department_entry = Entry(self.role_fields_frame, width=30)
            self.department_entry.grid(row=1, column=1, pady=5)
        
        elif role == "admin":
            Label(self.role_fields_frame, text="Admin ID:").grid(row=0, column=0, sticky='e', pady=5)
            self.admin_id_entry = Entry(self.role_fields_frame, width=30)
            self.admin_id_entry.grid(row=0, column=1, pady=5)
            
            Label(self.role_fields_frame, text="Contact Info:").grid(row=1, column=0, sticky='e', pady=5)
            self.contact_info_entry = Entry(self.role_fields_frame, width=30)
            self.contact_info_entry.grid(row=1, column=1, pady=5)
    
    def handle_registration(self):
        role = self.role_var.get()
        name = self.reg_name_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            # Check if email already exists
            cursor.execute("SELECT email FROM Users WHERE email=?", (email,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Email already exists")
                return
            
            if role == "student":
                student_id = int(self.student_id_entry.get())
                major = self.major_entry.get()
                
                if not (100000 <= student_id <= 999999):
                    raise ValueError("Student ID must be 6 digits")
                
                # Insert into Users table
                cursor.execute("INSERT INTO Users (user_id, name, role, email, password) VALUES (?, ?, ?, ?, ?)",
                              (student_id, name, role, email, password))
                
                # Insert into Students table
                cursor.execute("INSERT INTO Students (student_id, name, major, email) VALUES (?, ?, ?, ?)",
                              (student_id, name, major, email))
                
                messagebox.showinfo("Success", "Student registered successfully")
            
            elif role == "professor":
                prof_id = self.prof_id_entry.get()
                department = self.department_entry.get()
                
                # Insert into Users table
                cursor.execute("INSERT INTO Users (user_id, name, role, email, password) VALUES (?, ?, ?, ?, ?)",
                              (prof_id, name, role, email, password))
                
                # Insert into Professors table
                cursor.execute("INSERT INTO Professors (professor_id, name, department, email) VALUES (?, ?, ?, ?)",
                              (prof_id, name, department, email))
                
                messagebox.showinfo("Success", "Professor registered successfully")
            
            elif role == "admin":
                admin_id = self.admin_id_entry.get()
                contact_info = self.contact_info_entry.get()
                
                # Insert into Users table
                cursor.execute("INSERT INTO Users (user_id, name, role, email, password) VALUES (?, ?, ?, ?, ?)",
                              (admin_id, name, role, email, password))
                
                # Insert into Admins table
                cursor.execute("INSERT INTO Admins (admin_id, name, role, contact_info) VALUES (?, ?, ?, ?)",
                              (admin_id, name, role, contact_info))
                
                messagebox.showinfo("Success", "Admin registered successfully")
            
            conn.commit()
            conn.close()
            self.create_login_frame()
        
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
    
    def handle_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM Users WHERE email=? AND password=?", (email, password))
            user = cursor.fetchone()
            
            if user:
                user_id, name, role, email, _ = user
                
                if role == "student":
                    cursor.execute("SELECT * FROM Students WHERE student_id=?", (user_id,))
                    student_data = cursor.fetchone()
                    self.current_user = StudentGUI(user_id, name, email, student_data[2])
                
                elif role == "professor":
                    cursor.execute("SELECT * FROM Professors WHERE professor_id=?", (user_id,))
                    prof_data = cursor.fetchone()
                    self.current_user = ProfessorGUI(user_id, name, email, prof_data[2])
                
                elif role == "admin":
                    cursor.execute("SELECT * FROM Admins WHERE admin_id=?", (user_id,))
                    admin_data = cursor.fetchone()
                    self.current_user = AdminGUI(user_id, name, email, admin_data[3])
                
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Invalid email or password")
            
            conn.close()
        
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")
    
    def show_dashboard(self):
        self.clear_frame()
        
        # Create main container
        main_frame = Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True)
        
        # Header
        header_frame = Frame(main_frame, bg='lightgray', padx=10, pady=10)
        header_frame.pack(fill=X)
        
        Label(header_frame, text=f"Welcome, {self.current_user.name} ({self.current_user.role.capitalize()})", 
              font=('Arial', 14), bg='lightgray').pack(side=LEFT)
        
        Button(header_frame, text="Logout", command=self.logout).pack(side=RIGHT)
        
        # Navigation and content
        content_frame = Frame(main_frame)
        content_frame.pack(fill=BOTH, expand=True)
        
        # Navigation sidebar
        nav_frame = Frame(content_frame, width=200, bg='lightblue', padx=10, pady=10)
        nav_frame.pack(side=LEFT, fill=Y)
        
        # Add navigation buttons based on user role
        if self.current_user.role == "student":
            Button(nav_frame, text="View Courses", command=self.current_user.view_courses).pack(fill=X, pady=5)
            Button(nav_frame, text="View Grades", command=self.current_user.view_grades).pack(fill=X, pady=5)
        
        elif self.current_user.role == "professor":
            Button(nav_frame, text="View Courses", command=self.current_user.view_courses).pack(fill=X, pady=5)
            Button(nav_frame, text="Assign Grades", command=self.current_user.assign_grades).pack(fill=X, pady=5)
        
        elif self.current_user.role == "admin":
            Button(nav_frame, text="Manage Students", command=self.current_user.manage_students).pack(fill=X, pady=5)
            Button(nav_frame, text="Manage Professors", command=self.current_user.manage_professors).pack(fill=X, pady=5)
            Button(nav_frame, text="Manage Courses", command=self.current_user.manage_courses).pack(fill=X, pady=5)
        
        # Content area
        self.content_area = Frame(content_frame, padx=20, pady=20)
        self.content_area.pack(side=RIGHT, fill=BOTH, expand=True)
        
        # Show default dashboard view
        self.current_user.view_dashboard(self.content_area)
    
    def logout(self):
        self.current_user = None
        self.create_login_frame()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# GUI Classes for each user type
class StudentGUI:
    def __init__(self, user_id, name, email, major):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.major = major
        self.role = "student"
    
    def view_dashboard(self, parent_frame):
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        Label(parent_frame, text="Student Dashboard", font=('Arial', 16)).pack(pady=10)
        
        # Student info
        info_frame = LabelFrame(parent_frame, text="Student Information", padx=10, pady=10)
        info_frame.pack(fill=X, pady=10)
        
        Label(info_frame, text=f"Name: {self.name}").pack(anchor='w')
        Label(info_frame, text=f"Student ID: {self.user_id}").pack(anchor='w')
        Label(info_frame, text=f"Email: {self.email}").pack(anchor='w')
        Label(info_frame, text=f"Major: {self.major}").pack(anchor='w')
    
    def view_courses(self):
        for widget in self.parent.content_area.winfo_children():
            widget.destroy()
        
        Label(self.parent.content_area, text="Enrolled Courses", font=('Arial', 16)).pack(pady=10)
        
        # Fetch courses from database
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            cursor.execute('''SELECT c.course_id, c.course_name, c.department, c.credits, p.name 
                             FROM Enrollments e
                             JOIN Courses c ON e.course_id = c.course_id
                             LEFT JOIN Professors p ON c.professor_id = p.professor_id
                             WHERE e.student_id = ?''', (self.user_id,))
            courses = cursor.fetchall()
            
            if courses:
                tree = ttk.Treeview(self.parent.content_area, columns=('ID', 'Name', 'Department', 'Credits', 'Professor'), show='headings')
                tree.heading('ID', text='Course ID')
                tree.heading('Name', text='Course Name')
                tree.heading('Department', text='Department')
                tree.heading('Credits', text='Credits')
                tree.heading('Professor', text='Professor')
                
                for course in courses:
                    tree.insert('', 'end', values=course)
                
                tree.pack(fill=BOTH, expand=True)
            else:
                Label(self.parent.content_area, text="No courses enrolled").pack()
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch courses: {str(e)}")
    
    def view_grades(self):
        for widget in self.parent.content_area.winfo_children():
            widget.destroy()
        
        Label(self.parent.content_area, text="Grades", font=('Arial', 16)).pack(pady=10)
        
        # Fetch grades from database
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            cursor.execute('''SELECT c.course_id, c.course_name, e.grade 
                             FROM Enrollments e
                             JOIN Courses c ON e.course_id = c.course_id
                             WHERE e.student_id = ? AND e.grade IS NOT NULL''', (self.user_id,))
            grades = cursor.fetchall()
            
            if grades:
                tree = ttk.Treeview(self.parent.content_area, columns=('ID', 'Name', 'Grade'), show='headings')
                tree.heading('ID', text='Course ID')
                tree.heading('Name', text='Course Name')
                tree.heading('Grade', text='Grade')
                
                for grade in grades:
                    tree.insert('', 'end', values=grade)
                
                tree.pack(fill=BOTH, expand=True)
            else:
                Label(self.parent.content_area, text="No grades available").pack()
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch grades: {str(e)}")

class ProfessorGUI:
    def __init__(self, user_id, name, email, department):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.department = department
        self.role = "professor"
    
    def view_dashboard(self, parent_frame):
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        Label(parent_frame, text="Professor Dashboard", font=('Arial', 16)).pack(pady=10)
        
        # Professor info
        info_frame = LabelFrame(parent_frame, text="Professor Information", padx=10, pady=10)
        info_frame.pack(fill=X, pady=10)
        
        Label(info_frame, text=f"Name: {self.name}").pack(anchor='w')
        Label(info_frame, text=f"Professor ID: {self.user_id}").pack(anchor='w')
        Label(info_frame, text=f"Email: {self.email}").pack(anchor='w')
        Label(info_frame, text=f"Department: {self.department}").pack(anchor='w')
    
    def view_courses(self):
        for widget in self.parent.content_area.winfo_children():
            widget.destroy()
        
        Label(self.parent.content_area, text="Courses Taught", font=('Arial', 16)).pack(pady=10)
        
        # Fetch courses from database
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            cursor.execute('''SELECT course_id, course_name, department, credits 
                             FROM Courses 
                             WHERE professor_id = ?''', (self.user_id,))
            courses = cursor.fetchall()
            
            if courses:
                tree = ttk.Treeview(self.parent.content_area, columns=('ID', 'Name', 'Department', 'Credits'), show='headings')
                tree.heading('ID', text='Course ID')
                tree.heading('Name', text='Course Name')
                tree.heading('Department', text='Department')
                tree.heading('Credits', text='Credits')
                
                for course in courses:
                    tree.insert('', 'end', values=course)
                
                tree.pack(fill=BOTH, expand=True)
            else:
                Label(self.parent.content_area, text="No courses assigned").pack()
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch courses: {str(e)}")
    
    def assign_grades(self):
        for widget in self.parent.content_area.winfo_children():
            widget.destroy()
        
        Label(self.parent.content_area, text="Assign Grades", font=('Arial', 16)).pack(pady=10)
        
        # Course selection
        course_frame = Frame(self.parent.content_area)
        course_frame.pack(fill=X, pady=10)
        
        Label(course_frame, text="Select Course:").pack(side=LEFT, padx=5)
        self.course_var = StringVar()
        
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            cursor.execute('''SELECT course_id, course_name 
                             FROM Courses 
                             WHERE professor_id = ?''', (self.user_id,))
            courses = cursor.fetchall()
            
            if not courses:
                Label(self.parent.content_area, text="No courses assigned to you").pack()
                return
            
            course_options = [f"{course[0]} - {course[1]}" for course in courses]
            OptionMenu(course_frame, self.course_var, *course_options).pack(side=LEFT, padx=5)
            
            Button(course_frame, text="Load Students", command=self.load_students_for_grading).pack(side=LEFT, padx=10)
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch courses: {str(e)}")
    
    def load_students_for_grading(self):
        if not self.course_var.get():
            messagebox.showerror("Error", "Please select a course first")
            return
        
        course_id = self.course_var.get().split(" - ")[0]
        
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            # Get students enrolled in the course
            cursor.execute('''SELECT s.student_id, s.name, e.grade 
                             FROM Enrollments e
                             JOIN Students s ON e.student_id = s.student_id
                             WHERE e.course_id = ?''', (course_id,))
            students = cursor.fetchall()
            
            if not students:
                Label(self.parent.content_area, text="No students enrolled in this course").pack()
                return
            
            # Create grading table
            self.grading_table = ttk.Treeview(self.parent.content_area, columns=('ID', 'Name', 'Grade'), show='headings')
            self.grading_table.heading('ID', text='Student ID')
            self.grading_table.heading('Name', text='Student Name')
            self.grading_table.heading('Grade', text='Grade')
            
            for student in students:
                self.grading_table.insert('', 'end', values=student)
            
            self.grading_table.pack(fill=BOTH, expand=True)
            
            # Add grade entry and update button
            grade_frame = Frame(self.parent.content_area)
            grade_frame.pack(fill=X, pady=10)
            
            Label(grade_frame, text="Grade:").pack(side=LEFT, padx=5)
            self.grade_entry = Entry(grade_frame)
            self.grade_entry.pack(side=LEFT, padx=5)
            
            Button(grade_frame, text="Update Grade", command=lambda: self.update_grade(course_id)).pack(side=LEFT, padx=10)
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load students: {str(e)}")
    
    def update_grade(self, course_id):
        selected_item = self.grading_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student first")
            return
        
        try:
            grade = float(self.grade_entry.get())
            if not (0 <= grade <= 100):
                raise ValueError("Grade must be between 0 and 100")
            
            student_id = self.grading_table.item(selected_item)['values'][0]
            
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            cursor.execute('''UPDATE Enrollments 
                             SET grade = ?
                             WHERE student_id = ? AND course_id = ?''', 
                          (grade, student_id, course_id))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Grade updated successfully")
            self.load_students_for_grading()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid grade: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update grade: {str(e)}")

class AdminGUI:
    def __init__(self, user_id, name, email, contact_info):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.contact_info = contact_info
        self.role = "admin"
    
    def view_dashboard(self, parent_frame):
        for widget in parent_frame.winfo_children():
            widget.destroy()
        
        Label(parent_frame, text="Admin Dashboard", font=('Arial', 16)).pack(pady=10)
        
        # Admin info
        info_frame = LabelFrame(parent_frame, text="Admin Information", padx=10, pady=10)
        info_frame.pack(fill=X, pady=10)
        
        Label(info_frame, text=f"Name: {self.name}").pack(anchor='w')
        Label(info_frame, text=f"Admin ID: {self.user_id}").pack(anchor='w')
        Label(info_frame, text=f"Email: {self.email}").pack(anchor='w')
        Label(info_frame, text=f"Contact Info: {self.contact_info}").pack(anchor='w')
    
    def manage_students(self):
        for widget in self.parent.content_area.winfo_children():
            widget.destroy()
        
        Label(self.parent.content_area, text="Manage Students", font=('Arial', 16)).pack(pady=10)
        
        # Add student button
        Button(self.parent.content_area, text="Add New Student", command=self.add_student_dialog).pack(pady=10)
        
        # Student list
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            cursor.execute('''SELECT student_id, name, major, email FROM Students''')
            students = cursor.fetchall()
            
            if students:
                tree = ttk.Treeview(self.parent.content_area, columns=('ID', 'Name', 'Major', 'Email'), show='headings')
                tree.heading('ID', text='Student ID')
                tree.heading('Name', text='Name')
                tree.heading('Major', text='Major')
                tree.heading('Email', text='Email')
                
                for student in students:
                    tree.insert('', 'end', values=student)
                
                tree.pack(fill=BOTH, expand=True)
                
                # Add delete button
                Button(self.parent.content_area, text="Delete Selected", 
                      command=lambda: self.delete_student(tree)).pack(pady=10)
            else:
                Label(self.parent.content_area, text="No students found").pack()
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch students: {str(e)}")
    
    def add_student_dialog(self):
        dialog = Toplevel(self.parent.root)
        dialog.title("Add New Student")
        dialog.geometry("400x300")
        
        Label(dialog, text="Add New Student", font=('Arial', 14)).pack(pady=10)
        
        # Form fields
        form_frame = Frame(dialog, padx=10, pady=10)
        form_frame.pack()
        
        Label(form_frame, text="Student ID (6 digits):").grid(row=0, column=0, sticky='e', pady=5)
        student_id_entry = Entry(form_frame)
        student_id_entry.grid(row=0, column=1, pady=5)
        
        Label(form_frame, text="Name:").grid(row=1, column=0, sticky='e', pady=5)
        name_entry = Entry(form_frame)
        name_entry.grid(row=1, column=1, pady=5)
        
        Label(form_frame, text="Major:").grid(row=2, column=0, sticky='e', pady=5)
        major_entry = Entry(form_frame)
        major_entry.grid(row=2, column=1, pady=5)
        
        Label(form_frame, text="Email:").grid(row=3, column=0, sticky='e', pady=5)
        email_entry = Entry(form_frame)
        email_entry.grid(row=3, column=1, pady=5)
        
        Label(form_frame, text="Password:").grid(row=4, column=0, sticky='e', pady=5)
        password_entry = Entry(form_frame, show='*')
        password_entry.grid(row=4, column=1, pady=5)
        
        # Submit button
        Button(dialog, text="Add Student", 
              command=lambda: self.add_student(
                  student_id_entry.get(),
                  name_entry.get(),
                  major_entry.get(),
                  email_entry.get(),
                  password_entry.get(),
                  dialog
              )).pack(pady=10)
    
    def add_student(self, student_id, name, major, email, password, dialog):
        try:
            student_id = int(student_id)
            if not (100000 <= student_id <= 999999):
                raise ValueError("Student ID must be 6 digits")
            
            if not all([name, major, email, password]):
                raise ValueError("All fields are required")
            
            if len(password) < 6:
                raise ValueError("Password must be at least 6 characters")
            
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            # Check if student ID or email already exists
            cursor.execute("SELECT student_id FROM Students WHERE student_id=?", (student_id,))
            if cursor.fetchone():
                raise ValueError("Student ID already exists")
            
            cursor.execute("SELECT email FROM Students WHERE email=?", (email,))
            if cursor.fetchone():
                raise ValueError("Email already exists")
            
            # Add to Users table
            cursor.execute("INSERT INTO Users (user_id, name, role, email, password) VALUES (?, ?, 'student', ?, ?)",
                          (student_id, name, email, password))
            
            # Add to Students table
            cursor.execute("INSERT INTO Students (student_id, name, major, email) VALUES (?, ?, ?, ?)",
                          (student_id, name, major, email))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Student added successfully")
            dialog.destroy()
            self.manage_students()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")
    
    def delete_student(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student first")
            return
        
        student_id = tree.item(selected_item)['values'][0]
        
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            # Delete from Enrollments first (foreign key constraint)
            cursor.execute("DELETE FROM Enrollments WHERE student_id=?", (student_id,))
            
            # Delete from Students
            cursor.execute("DELETE FROM Students WHERE student_id=?", (student_id,))
            
            # Delete from Users
            cursor.execute("DELETE FROM Users WHERE user_id=?", (student_id,))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Student deleted successfully")
            self.manage_students()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
    
    def manage_professors(self):
        for widget in self.parent.content_area.winfo_children():
            widget.destroy()
        
        Label(self.parent.content_area, text="Manage Professors", font=('Arial', 16)).pack(pady=10)
        
        # Add professor button
        Button(self.parent.content_area, text="Add New Professor", command=self.add_professor_dialog).pack(pady=10)
        
        # Professor list
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            cursor.execute('''SELECT professor_id, name, department, email FROM Professors''')
            professors = cursor.fetchall()
            
            if professors:
                tree = ttk.Treeview(self.parent.content_area, columns=('ID', 'Name', 'Department', 'Email'), show='headings')
                tree.heading('ID', text='Professor ID')
                tree.heading('Name', text='Name')
                tree.heading('Department', text='Department')
                tree.heading('Email', text='Email')
                
                for professor in professors:
                    tree.insert('', 'end', values=professor)
                
                tree.pack(fill=BOTH, expand=True)
                
                # Add delete button
                Button(self.parent.content_area, text="Delete Selected", 
                      command=lambda: self.delete_professor(tree)).pack(pady=10)
            else:
                Label(self.parent.content_area, text="No professors found").pack()
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch professors: {str(e)}")
    
    def add_professor_dialog(self):
        dialog = Toplevel(self.parent.root)
        dialog.title("Add New Professor")
        dialog.geometry("400x300")
        
        Label(dialog, text="Add New Professor", font=('Arial', 14)).pack(pady=10)
        
        # Form fields
        form_frame = Frame(dialog, padx=10, pady=10)
        form_frame.pack()
        
        Label(form_frame, text="Professor ID:").grid(row=0, column=0, sticky='e', pady=5)
        prof_id_entry = Entry(form_frame)
        prof_id_entry.grid(row=0, column=1, pady=5)
        
        Label(form_frame, text="Name:").grid(row=1, column=0, sticky='e', pady=5)
        name_entry = Entry(form_frame)
        name_entry.grid(row=1, column=1, pady=5)
        
        Label(form_frame, text="Department:").grid(row=2, column=0, sticky='e', pady=5)
        dept_entry = Entry(form_frame)
        dept_entry.grid(row=2, column=1, pady=5)
        
        Label(form_frame, text="Email:").grid(row=3, column=0, sticky='e', pady=5)
        email_entry = Entry(form_frame)
        email_entry.grid(row=3, column=1, pady=5)
        
        Label(form_frame, text="Password:").grid(row=4, column=0, sticky='e', pady=5)
        password_entry = Entry(form_frame, show='*')
        password_entry.grid(row=4, column=1, pady=5)
        
        # Submit button
        Button(dialog, text="Add Professor", 
              command=lambda: self.add_professor(
                  prof_id_entry.get(),
                  name_entry.get(),
                  dept_entry.get(),
                  email_entry.get(),
                  password_entry.get(),
                  dialog
              )).pack(pady=10)
    
    def add_professor(self, prof_id, name, department, email, password, dialog):
        try:
            if not all([prof_id, name, department, email, password]):
                raise ValueError("All fields are required")
            
            if len(password) < 6:
                raise ValueError("Password must be at least 6 characters")
            
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            # Check if professor ID or email already exists
            cursor.execute("SELECT professor_id FROM Professors WHERE professor_id=?", (prof_id,))
            if cursor.fetchone():
                raise ValueError("Professor ID already exists")
            
            cursor.execute("SELECT email FROM Professors WHERE email=?", (email,))
            if cursor.fetchone():
                raise ValueError("Email already exists")
            
            # Add to Users table
            cursor.execute("INSERT INTO Users (user_id, name, role, email, password) VALUES (?, ?, 'professor', ?, ?)",
                          (prof_id, name, email, password))
            
            # Add to Professors table
            cursor.execute("INSERT INTO Professors (professor_id, name, department, email) VALUES (?, ?, ?, ?)",
                          (prof_id, name, department, email))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Professor added successfully")
            dialog.destroy()
            self.manage_professors()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add professor: {str(e)}")
    
    def delete_professor(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a professor first")
            return
        
        prof_id = tree.item(selected_item)['values'][0]
        
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            # First, unassign this professor from any courses
            cursor.execute("UPDATE Courses SET professor_id = NULL WHERE professor_id=?", (prof_id,))
            
            # Delete from Professors
            cursor.execute("DELETE FROM Professors WHERE professor_id=?", (prof_id,))
            
            # Delete from Users
            cursor.execute("DELETE FROM Users WHERE user_id=?", (prof_id,))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Professor deleted successfully")
            self.manage_professors()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete professor: {str(e)}")
    
    def manage_courses(self):
        for widget in self.parent.content_area.winfo_children():
            widget.destroy()
        
        Label(self.parent.content_area, text="Manage Courses", font=('Arial', 16)).pack(pady=10)
        
        # Add course button
        Button(self.parent.content_area, text="Add New Course", command=self.add_course_dialog).pack(pady=10)
        
        # Course list
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            cursor.execute('''SELECT c.course_id, c.course_name, c.department, c.credits, p.name 
                             FROM Courses c
                             LEFT JOIN Professors p ON c.professor_id = p.professor_id''')
            courses = cursor.fetchall()
            
            if courses:
                tree = ttk.Treeview(self.parent.content_area, columns=('ID', 'Name', 'Department', 'Credits', 'Professor'), show='headings')
                tree.heading('ID', text='Course ID')
                tree.heading('Name', text='Course Name')
                tree.heading('Department', text='Department')
                tree.heading('Credits', text='Credits')
                tree.heading('Professor', text='Professor')
                
                for course in courses:
                    tree.insert('', 'end', values=course)
                
                tree.pack(fill=BOTH, expand=True)
                
                # Add delete and assign professor buttons
                button_frame = Frame(self.parent.content_area)
                button_frame.pack(pady=10)
                
                Button(button_frame, text="Delete Selected", 
                      command=lambda: self.delete_course(tree)).pack(side=LEFT, padx=5)
                
                Button(button_frame, text="Assign Professor", 
                      command=lambda: self.assign_professor_dialog(tree)).pack(side=LEFT, padx=5)
            else:
                Label(self.parent.content_area, text="No courses found").pack()
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch courses: {str(e)}")
    
    def add_course_dialog(self):
        dialog = Toplevel(self.parent.root)
        dialog.title("Add New Course")
        dialog.geometry("400x300")
        
        Label(dialog, text="Add New Course", font=('Arial', 14)).pack(pady=10)
        
        # Form fields
        form_frame = Frame(dialog, padx=10, pady=10)
        form_frame.pack()
        
        Label(form_frame, text="Course ID:").grid(row=0, column=0, sticky='e', pady=5)
        course_id_entry = Entry(form_frame)
        course_id_entry.grid(row=0, column=1, pady=5)
        
        Label(form_frame, text="Course Name:").grid(row=1, column=0, sticky='e', pady=5)
        name_entry = Entry(form_frame)
        name_entry.grid(row=1, column=1, pady=5)
        
        Label(form_frame, text="Department:").grid(row=2, column=0, sticky='e', pady=5)
        dept_entry = Entry(form_frame)
        dept_entry.grid(row=2, column=1, pady=5)
        
        Label(form_frame, text="Credits:").grid(row=3, column=0, sticky='e', pady=5)
        credits_entry = Entry(form_frame)
        credits_entry.grid(row=3, column=1, pady=5)
        
        # Submit button
        Button(dialog, text="Add Course", 
              command=lambda: self.add_course(
                  course_id_entry.get(),
                  name_entry.get(),
                  dept_entry.get(),
                  credits_entry.get(),
                  dialog
              )).pack(pady=10)
    
    def add_course(self, course_id, name, department, credits, dialog):
        try:
            if not all([course_id, name, department]):
                raise ValueError("Course ID, Name, and Department are required")
            
            credits = int(credits) if credits else None
            
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            # Check if course ID already exists
            cursor.execute("SELECT course_id FROM Courses WHERE course_id=?", (course_id,))
            if cursor.fetchone():
                raise ValueError("Course ID already exists")
            
            # Add to Courses table
            cursor.execute("INSERT INTO Courses (course_id, course_name, department, credits) VALUES (?, ?, ?, ?)",
                          (course_id, name, department, credits))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Course added successfully")
            dialog.destroy()
            self.manage_courses()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add course: {str(e)}")
    
    def delete_course(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a course first")
            return
        
        course_id = tree.item(selected_item)['values'][0]
        
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            # Delete from Enrollments first (foreign key constraint)
            cursor.execute("DELETE FROM Enrollments WHERE course_id=?", (course_id,))
            
            # Delete from Courses
            cursor.execute("DELETE FROM Courses WHERE course_id=?", (course_id,))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Course deleted successfully")
            self.manage_courses()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete course: {str(e)}")
    
    def assign_professor_dialog(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a course first")
            return
        
        course_id = tree.item(selected_item)['values'][0]
        
        dialog = Toplevel(self.parent.root)
        dialog.title("Assign Professor")
        dialog.geometry("400x200")
        
        Label(dialog, text=f"Assign Professor to Course {course_id}", font=('Arial', 14)).pack(pady=10)
        
        # Professor selection
        prof_frame = Frame(dialog, padx=10, pady=10)
        prof_frame.pack()
        
        Label(prof_frame, text="Select Professor:").grid(row=0, column=0, sticky='e', pady=5)
        self.prof_var = StringVar()
        
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            cursor.execute('''SELECT professor_id, name FROM Professors''')
            professors = cursor.fetchall()
            
            if not professors:
                Label(prof_frame, text="No professors available").grid(row=0, column=1)
                return
            
            prof_options = [f"{prof[0]} - {prof[1]}" for prof in professors]
            OptionMenu(prof_frame, self.prof_var, *prof_options).grid(row=0, column=1)
            
            Button(dialog, text="Assign", 
                  command=lambda: self.assign_professor(course_id, dialog)).pack(pady=10)
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch professors: {str(e)}")
    
    def assign_professor(self, course_id, dialog):
        if not self.prof_var.get():
            messagebox.showerror("Error", "Please select a professor first")
            return
        
        prof_id = self.prof_var.get().split(" - ")[0]
        
        try:
            conn = sqlite3.connect('university.db')
            cursor = conn.cursor()
            
            # Assign professor to course
            cursor.execute("UPDATE Courses SET professor_id = ? WHERE course_id = ?", 
                          (prof_id, course_id))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Professor assigned successfully")
            dialog.destroy()
            self.manage_courses()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to assign professor: {str(e)}")

# Main application
if __name__ == "__main__":
    root = Tk()
    app = UniversityApp(root)
    
    # Set parent reference for GUI classes
    StudentGUI.parent = app
    ProfessorGUI.parent = app
    AdminGUI.parent = app
    
    root.mainloop()
