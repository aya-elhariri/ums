
import sqlite3

# Connect to the database (creates if it doesn't exist)
conn = sqlite3.connect('Uni_system.db')
cursor = conn.cursor()

def setup_database():
    """Create the tables we need"""
    # Students table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        major TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    ''')
    
    # Courses table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT NOT NULL
    )
    ''')
    
    # Enrollment table (links students to courses)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS enrollment (
        student_id INTEGER,
        course_id INTEGER,
        PRIMARY KEY (student_id, course_id),
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    )
    ''')
    
    conn.commit()

def add_student(student_id, name, major, email):
    """Add a new student"""
    try:
        cursor.execute('''
        INSERT INTO students (id, name, major, email)
        VALUES (?, ?, ?, ?)
        ''', (student_id, name, major, email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def add_course(course_name, department):
    """Add a new course"""
    cursor.execute('''
    INSERT INTO courses (name, department)
    VALUES (?, ?)
    ''', (course_name, department))
    conn.commit()
    return cursor.lastrowid  # Returns the auto-generated course ID

def enroll_student(student_id, course_id):
    """Enroll a student in a course"""
    try:
        cursor.execute('''
        INSERT INTO enrollment (student_id, course_id)
        VALUES (?, ?)
        ''', (student_id, course_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def get_student_info(student_id):
    """Get all info about a student"""
    # Get basic info
    cursor.execute('SELECT id, name, major, email FROM students WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    
    if not student:
        return None
    
    # Get enrolled courses
    cursor.execute('''
    SELECT c.name 
    FROM courses c
    JOIN enrollment e ON c.id = e.course_id
    WHERE e.student_id = ?
    ''', (student_id,))
    courses = [row[0] for row in cursor.fetchall()]
    
    return {
        'id': student[0],
        'name': student[1],
        'major': student[2],
        'email': student[3],
        'courses': courses
    }

# Initialize the database when this file is imported
setup_database()



# Connect to the same database as students
conn = sqlite3.connect('Uni_system.db')
cursor = conn.cursor()

def setup_professor_tables():
    """Create tables needed for professors"""
    # Professors table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS professors (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        department TEXT NOT NULL
    )
    ''')
    
    # Courses taught by professors
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS professor_courses (
        professor_id TEXT,
        course_id INTEGER,
        PRIMARY KEY (professor_id, course_id),
        FOREIGN KEY (professor_id) REFERENCES professors(id),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    )
    ''')
    
    conn.commit()

def add_professor(professor_id, name, email, department):
    """Add a new professor to the database"""
    try:
        cursor.execute('''
        INSERT INTO professors (id, name, email, department)
        VALUES (?, ?, ?, ?)
        ''', (professor_id, name, email, department))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def assign_course_to_professor(professor_id, course_id):
    """Assign a course to be taught by a professor"""
    try:
        cursor.execute('''
        INSERT INTO professor_courses (professor_id, course_id)
        VALUES (?, ?)
        ''', (professor_id, course_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def get_professor_info(professor_id):
    """Get all info about a professor"""
    # Get basic info
    cursor.execute('SELECT id, name, email, department FROM professors WHERE id = ?', (professor_id,))
    professor = cursor.fetchone()
    
    if not professor:
        return None
    
    # Get courses taught
    cursor.execute('''
    SELECT c.name 
    FROM courses c
    JOIN professor_courses pc ON c.id = pc.course_id
    WHERE pc.professor_id = ?
    ''', (professor_id,))
    courses = [row[0] for row in cursor.fetchall()]
    
    return {
        'id': professor[0],
        'name': professor[1],
        'email': professor[2],
        'department': professor[3],
        'courses': courses
    }

# Initialize professor tables when this file is imported
setup_professor_tables()