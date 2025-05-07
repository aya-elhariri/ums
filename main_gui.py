import tkinter as tk
from tkinter import ttk, messagebox
import Database
import sqlite3

# Your User class
class User:
    def __init__(self, user_id, name, role, email, password):
        try:
            if not isinstance(user_id, int):
                raise TypeError("user_id must be an integer")
            if not isinstance(name, str) or not name:
                raise ValueError("name must be a non-empty string")
            if not isinstance(role, str) or not role:
                raise ValueError("role must be a non-empty string")
            if not isinstance(email, str) or '@' not in email:
                raise ValueError("email must be a valid email address")
            if not isinstance(password, str) or len(password) < 6:
                raise ValueError("password must be at least 6 characters")

            self.user_id = user_id
            self.name = name
            self.role = role
            self.email = email
            self.__password = password
            self.logged_in = False

        except (TypeError, ValueError) as e:
            print(f"Can't initialize User: {e}")

    
    ## eih da   

    def check_credentials(self, email, password):
        return email == self.email and password == self.__password

    def login(self):
        if not self.logged_in:
            self.logged_in = True
            print("Logged in successfully.")
        else:
            print("Already logged in.")

    def logout(self):
        if self.logged_in:
            self.logged_in = False
            print("Logged out successfully.")
        else:
            print("Already logged out.")

    def view_dashboard(self):
        print(f"Dashboard of {self.name}")
        print(f"User data:\nName: {self.name}\nRole: {self.role}\nID: {self.user_id}\nEmail: {self.email}")


    ## eih da   
    def get_student_data(self):
        return {
            "name": self.name,
            "role": self.role,
            "user_id": str(self.user_id),
            "email": self.email,
            "department": "Computer Science",  # You can make these dynamic
            "year": "2023"                      # You can make these dynamic
        }

class StudentDashboard:
    def __init__(self, root, student_data):
        self.root = root
        self.root.title("Student Dashboard")
        self.root.geometry("600x400")
        self.student_data = student_data
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Label(
            main_frame, 
            text=f"Dashboard of: {self.student_data['name']}",
            font=('Helvetica', 16, 'bold')
        )
        header.pack(pady=(0, 20))
        
        # User info frame
        info_frame = ttk.LabelFrame(main_frame, text="Student Information", padding=15)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create labels for each piece of information
        labels = [
            ("Name:", self.student_data['name']),
            ("Role:", self.student_data['role']),
            ("Student ID:", self.student_data['user_id']),
            ("Email:", self.student_data['email']),
            ("Department:", self.student_data.get('department', 'N/A')),
            ("Year:", self.student_data.get('year', 'N/A'))
        ]
        
        for i, (label_text, value) in enumerate(labels):
            # Label
            label = ttk.Label(info_frame, text=label_text, font=('Helvetica', 11, 'bold'))
            label.grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            
            # Value
            value_label = ttk.Label(info_frame, text=value, font=('Helvetica', 11))
            value_label.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Additional widgets (grades, courses, etc.)
        self.create_additional_widgets(main_frame)
        
        # Close button
        close_btn = ttk.Button(
            main_frame, 
            text="Close", 
            command=self.root.destroy
        )
        close_btn.pack(pady=(20, 0))
    
    def create_additional_widgets(self, parent):
        # Notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Grades tab
        grades_frame = ttk.Frame(notebook)
        self.create_grades_table(grades_frame)
        notebook.add(grades_frame, text="Grades")
        
        # Courses tab
        courses_frame = ttk.Frame(notebook)
        self.create_courses_list(courses_frame)
        notebook.add(courses_frame, text="Courses")
    
    def create_grades_table(self, parent):
        # Sample grade data
        grade_data = [
            ("Mathematics", "A", "90%"),
            ("Physics", "B+", "87%"),
            ("Chemistry", "A-", "92%"),
            ("Biology", "B", "85%"),
            ("History", "A", "95%")
        ]
        
        # Create treeview
        tree = ttk.Treeview(parent, columns=("Subject", "Grade", "Score"), show="headings")
        
        # Define headings
        tree.heading("Subject", text="Subject")
        tree.heading("Grade", text="Grade")
        tree.heading("Score", text="Score")
        
        # Add data
        for subject, grade, score in grade_data:
            tree.insert("", tk.END, values=(subject, grade, score))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        
        # Pack widgets
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_courses_list(self, parent):
        # Sample course data
        courses = [
            "Mathematics - Prof. Smith",
            "Physics - Prof. Johnson",
            "Chemistry - Prof. Williams",
            "Biology - Prof. Brown",
            "History - Prof. Davis",
            "Computer Science - Prof. Miller"
        ]
        
        # Create listbox
        listbox = tk.Listbox(parent, font=('Helvetica', 11), height=10)
        
        # Add courses to listbox
        for course in courses:
            listbox.insert(tk.END, course)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=listbox.yview)
        listbox.configure(yscroll=scrollbar.set)
        
        # Pack widgets
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Tkinter GUI
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("400x300")
        self.root.configure(bg="#2c3e50")
        
        # Create a user instance
        self.user = User(1, "John Doe", "Student", "admin@example.com", "123456")
        
        self.setup_ui()
    
    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Card.TFrame", background="#ecf0f1")
        style.configure("TLabel", background="#ecf0f1", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))

        frame = ttk.Frame(self.root, padding=20, style="Card.TFrame")
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Login", font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))
        ttk.Label(frame, text="Email").pack(anchor="w")
        self.email_entry = ttk.Entry(frame, width=30)
        self.email_entry.pack(pady=5)

        ttk.Label(frame, text="Password").pack(anchor="w")
        self.password_entry = ttk.Entry(frame, width=30, show="*")
        self.password_entry.pack(pady=5)

        ttk.Button(frame, text="Login", command=self.gui_login).pack(pady=20)
    
    def gui_login(self):
        entered_email = self.email_entry.get()
        entered_password = self.password_entry.get()

        if not entered_email or not entered_password:
            messagebox.showwarning("Input Error", "Please enter both email and password.")
            return

        if self.user.check_credentials(entered_email, entered_password):
            self.user.login()
            messagebox.showinfo("Login Success", f"Welcome, {self.user.name}!")
            self.user.view_dashboard()
            self.open_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")
    
    def open_dashboard(self):
        # Close the login window
        self.root.withdraw()
        
        # Create new window for dashboard
        dashboard_window = tk.Toplevel()
        dashboard_window.protocol("WM_DELETE_WINDOW", self.on_dashboard_close)
        
        # Get student data from user
        student_data = self.user.get_student_data()
        
        # Open dashboard
        StudentDashboard(dashboard_window, student_data)
    
    def on_dashboard_close(self):
        # When dashboard closes, log out and show login window again
        self.user.logout()
        self.root.deiconify()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
