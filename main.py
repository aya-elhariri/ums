# mohmmed:
from datetime import date
from abc import ABC, abstractmethod
import sqlite3
from multipledispatch import dispatch



class User(ABC):
    def __init__(self, user_id, name, role, email, password):
        try:
            if not isinstance(user_id, (int, str)):
                    raise TypeError("user_id must be an integer")
            if not isinstance(name, str) or not name:
                raise ValueError("name must be a non-empty string")
            if not isinstance(role, str) or not role:
                raise ValueError("role must be a non-empty string")
            if not isinstance(email, str) or '@' not in email:
                raise ValueError("email must be a valid email address")
            if not isinstance(password, str) or len(password) < 6:
                raise ValueError("password must be a string with at least 6 characters")
            self.user_id = user_id
            self.name = name
            self.role = role
            self.email = email
            self.__password = password
            self.logged_in = False
        except (TypeError, ValueError) as e:
            print(f"can't initialize User: {e}")

    def login(self):
        try:
            email = input("Enter your email: ")
            password = input("Enter your password: ")

            while not email or not password:
                print("Email and password cannot be empty.")
                email = input("Enter your email: ")
                password = input("Enter your password: ")

            while email != self.email or password != self.__password:
                print("Invalid email or password.")
                email = input("Enter your email: ")
                password = input("Enter your password: ")

            if self.logged_in:
                print("You are already logged in.")
            else:
                self.logged_in = True
                print("Logged in successfully.")

        except Exception as e:
            print(f"Something went wrong: {e}")

    def logout(self):
        if self.logged_in:
            self.logged_in = False
            print("loged out sucessfully")
        else:
            print("you are already logged out")

    @abstractmethod
    def view_dashboard(self):
        pass

    @abstractmethod
    def get_info(self):
        pass

class UserProxy(User):
    def __init__(self, real_user):
        self._real_user = real_user

    def login(self):
        if not self._real_user.logged_in:
            self._real_user.login()
        else:
            print("User is already logged in")

    def logout(self):
        if self._real_user.logged_in:
            self._real_user.logout()
        else:
            print("User is already logged out")

    def view_dashboard(self):
        if self._real_user.logged_in:
            self._real_user.view_dashboard()
        else:
            print("Please login first to view dashboard")

    def get_info(self):
        if self._real_user.logged_in:
            self._real_user.get_info()
        else:
            print("Please login first to view info")

class student(User):
    In_Use_IDs = set()
    def __init__(self, student_name, student_id, major, email, password):
        super().__init__(student_id, student_name,'student', email=email, password=password)

        if not isinstance(student_name, str) or not student_name:
            raise ValueError("name must be a string and cannot be empty space!")

        if not isinstance(email, str) or not email:
            raise ValueError("email must be a string and cannot be empty space!")

        if '@' not in email or '.' not in email:
            raise ValueError("email must follow this format -->  'user@example.com'")

        if not isinstance(student_id, int) or not (100000 <= student_id <= 999999):
            raise ValueError("ID must be an integer and must be 6 digits long")

        if student_id in student.In_Use_IDs:
            raise ValueError("ID is already in use. please enter a different ID")
        student.In_Use_IDs.add(student_id)

        self.student_name = student_name
        self.student_id = student_id
        self.major = major
        self.email = email
        self.courses_enrolled = []
        self.__grades = {}

    def is_eligible(self, course_obj):
        if course_obj.department == self.major:
            return True
        else:
            return False

    def set_grades(self, course, new_grade):
        self.__grades[course] = new_grade

    def enroll_course(self, course_obj):
        if not course_obj:
            raise ValueError("You may have accidentally entered an empty space")
        if course_obj in self.courses_enrolled:
            print(f"{self.student_name} is already enrolled in {course_obj.course_name}")
            return

        if self.is_eligible(course_obj):
            self.courses_enrolled.append(course_obj)
            print(f"{self.student_name} has enrolled in {course_obj.course_name}")
        else:
            print(f" no such course as {course_obj.course_name}")

    def drop_course(self, course_obj):
        if not course_obj:
            raise ValueError("You may have accidentally entered an empty space")

        if course_obj in self.courses_enrolled:
            self.courses_enrolled.remove(course_obj)
            print(f"{self.student_name} has dropped {course_obj.course_name}")
        else:
            print(f"{self.student_name} is not currently enrolled in this course")

    def view_grades(self):
        if not self.__grades:
            print("No grades available.")
            return
            
        print("\nSTUDENT GRADES")
        print("--------------")
        for course, grade in self.__grades.items():
            if hasattr(course, 'course_name'):
                course_name = course.course_name
            else:
                course_name = str(course)
            print(f"Course: {course_name}, Grade: {grade}")
            print()

    def get_info(self):
        print("STUDENT INFO")
        print(f"Student's name : {self.student_name} , Student's id : {self.student_id} , student's major : {self.major}")
        print(f"student's email : {self.email}")
        for course in self.courses_enrolled:
            print(f"course : {course.course_name}")
        print("")

    def view_dashboard(self):
        self.get_info()

class Admin(User):
    def __init__(self, admin_id, name, role, contact_info):
        try:
            if not all([admin_id, name, role, contact_info]):
                raise ValueError("All admin fields (ID, name, role, contact_info) must be provided.")
            if not isinstance(admin_id, str):
                raise TypeError("Admin ID must be a string.")
            if not isinstance(name, str):
                raise TypeError("Name must be a string.")
            if not isinstance(role, str):
                raise TypeError("Role must be a string.")
            if not isinstance(contact_info, (str, dict)):
                raise TypeError("Contact info must be a string or a dictionary.")

            self.__admin_id = admin_id
            self.name = name
            self.role = role
            self.contact_info = contact_info

        except(ValueError, TypeError) as e:
            print(f"Error creating Admin: {e}")

    def add_student(self, student_name, student_id, major, email):
        if not all([student_name, student_id, major, email]):
            print("ERROR: All student fields must be provided.")
            return
        if student_id in student.In_Use_IDs:
            print("STUDENT Already Exists!")
        else:
            try:
                new_student = student(student_name, student_id, major, email)
                student.In_Use_IDs.add(new_student.student_id)
                print(f"Student {new_student.name} added successfully.")
            except Exception as e:
                print(f"ERROR: Failed to create student. Reason: {e}")

    def remove_student(self, student_id):
        if not student_id:
            print("ERROR: Student ID is required.")
            return

        try:
            if student_id not in student.In_Use_IDs:
                print("Student Does Not Exist!")
                return
            student.In_Use_IDs.remove(student_id)
        except Exception as e:
            print(f"Something went wrong: {e}")

    def assign_professor(self, course, professor):
        if not course or not professor:
            print("ERROR: Course and Professor must be provided.")
            return
        try:
            if not hasattr(professor, 'courses_taught') or not isinstance(professor.courses_taught, list):
                raise AttributeError("Professor object is missing 'courses_taught' list.")

            if hasattr(course, 'professor') and course.professor:
                print(f"ERROR: Course {course.course_id} already has a professor assigned: {course.professor.name}")
                return

            if course in professor.courses_taught:
                print(f"Professor {professor.name} already teaches this course.")
                return

            professor.courses_taught.append(course)
            course.professor = professor
            print(f"prof. {professor.name} is assigned to course: {course.course_id}")

        except Exception as e:
            print(f"Something went wrong: {e}")

    def manage_course(self, operation, course, department):
        if operation.lower() == "add":
            if course not in department.courses_offered:
                department.courses_offered.append(course)
                print(f"course {course} added sucessfuly to department of {department}")
            else:
                print("CAN NOT BE ADDED. course already exists")
        if operation.lower() == "remove":
            if course in department.courses_offered:
                department.courses_offered.remove(course)
                print(f"course {course} removed sucessfuly from department of {department}")
            else:
                print("ERROR course doesn't exists")

    def view_dashboard(self):
        self.get_info()

    def get_info(self):
        print ({
            "admin_id": self.__admin_id,
            "name": self.name,
            "role": self.role,
            "contact_info": self.contact_info,
        })

class Exam:
    def __init__(self, exam_id, course, duration, student_results, exam_date=None):
        if not exam_id:
            raise ValueError("Exam ID cannot be empty")
        if not course:
            raise ValueError("Course cannot be empty")
        if duration <= 0:
            raise ValueError("Duration must be positive")

        self.exam_id = exam_id
        self.course = course
        self.exam_date = exam_date
        self.duration = duration
        self.__student_results = {}

    def schedule_exam(self, year, month, day):
        while True:
            try:
                self.exam_date = date(year, month, day)
                break
            except ValueError:
                print("Invalid date. please enter a valid date")

    def record_result(self, score, student_name):
        self.__student_results[student_name] = score
        print(f"{student_name}' results have been saved as {score}")

    def set_student_results(self, student, result):
        self.__student_results[student] = result

    def display_student_results(self):
        print("")
        print("*EXAM RESULTS*")
        print(f"result for exam {self.exam_id} in course {self.course} : ")
        for student, score in self.__student_results.items():
            print(f"student : {student}'s score is {score}")
        print("")

    def view_exam_info(self):
        print(" ")
        print("EXAM INFO")
        print(f"exam ID : {self.exam_id} , course : {self.course}")
        if self.exam_date:
            print(f"{self.exam_id} is scheduled for {self.exam_date.strftime('%y-%m-%d')}" )
        else:
            print("exam has no scheduled date yet")
        print("*")

class Classroom:
    def __init__(self, classroom_id, location, capacity):
        try:
            if not isinstance(classroom_id, str) or not classroom_id:
                raise ValueError("Classroom ID must be a non-empty string")

            if not isinstance(location, str) or not location:
                raise ValueError("Location must be a non-empty string")

            capacity = int(capacity)
            if capacity <= 0:
                raise ValueError("Capacity must be a positive integer")

            self.classroom_id = classroom_id.strip()
            self.location = location.strip()
            self.capacity = capacity
            self.schedule = {}

        except ValueError as e:
            print(f"Error creating Classroom: {e}")

    def allocate_class(self, course_name, time_slot, num_students):
        try:
            if not isinstance(course_name, str) or not course_name:
                raise ValueError("Course name must be a non-empty string")

            if not isinstance(time_slot, str) or not time_slot:
                raise ValueError("Time slot must be a non-empty string")

            if not isinstance(num_students, int) or num_students <= 0:
                raise ValueError("Number of students must be a positive integer")

            if not self.check_availability(time_slot):
                raise ValueError(f"Classroom {self.classroom_id} is already booked at {time_slot}")

            if num_students > self.capacity:
                raise ValueError(
                    f"Classroom capacity exceeded (Capacity: {self.capacity}, "
                    f"Requested: {num_students})"
                )

            self.schedule[time_slot] = course_name
            print(f"Classroom {self.classroom_id} allocated for {course_name} at {time_slot}.")

        except ValueError as e:
            print(f"Allocation failed: {e}")

    def check_availability(self, time_slot):
        try:
            if not isinstance(time_slot, str) or not time_slot:
                raise ValueError("Time slot must be a non-empty string")

            return time_slot not in self.schedule

        except ValueError as e:
            print(f"Availability check failed: {e}")

    def get_classroom_info(self):
        return (
            f"Classroom ID: {self.classroom_id}, "
            f"Location: {self.location}, "
            f"Capacity: {self.capacity}"
        )

    def __str__(self):
        return self.get_classroom_info()

class Library:
    def __init__(self, library_id):
        try:
            if not isinstance(library_id, str) or not library_id:
                raise ValueError("Library ID must be a non-empty string")

            self.library_id = library_id.strip()
            self.books = {}
            self.students_registered = set()
            self.borrowed_books = {}

        except ValueError as e:
            print(f"Error creating Library: {str(e)}")
            raise

    def add_book(self, book_id, book_name):
        try:
            if not isinstance(book_id, str) or not book_id.strip():
                raise ValueError("Book ID must be a non-empty string")

            if not isinstance(book_name, str) or not book_name.strip():
                raise ValueError("Book name must be a non-empty string")

            if book_id in self.books:
                raise ValueError(f"Book with ID {book_id} already exists")

            self.books[book_id] = book_name.strip()
            print(f"Book '{book_name}' added to the library.")

        except ValueError as e:
            print(f"Failed to add book: {str(e)}")

    def register_student(self, student_name):
        try:
            if not isinstance(student_name, str) or not student_name.strip():
                raise ValueError("Student name must be a non-empty string")

            if student_name in self.students_registered:
                raise ValueError(f"Student {student_name} is already registered")

            self.students_registered.add(student_name.strip())
            print(f"Student {student_name} registered with the library.")

        except ValueError as e:
            print(f"Registration failed: {str(e)}")

    def borrow_book(self, student_name, book_id):
        try:
            if not isinstance(student_name, str) or not student_name.strip():
                raise ValueError("Student name must be a non-empty string")

            if not isinstance(book_id, str) or not book_id.strip():
                raise ValueError("Book ID must be a non-empty string")

            student_name = student_name.strip()
            book_id = book_id.strip()

            if student_name not in self.students_registered:
                raise ValueError(f"Student {student_name} is not registered with the library")

            if book_id not in self.books:
                raise ValueError(f"Book with ID {book_id} not found")

            if student_name not in self.borrowed_books:
                self.borrowed_books[student_name] = []

            if book_id in self.borrowed_books[student_name]:
                raise ValueError(f"Student {student_name} has already borrowed this book")

            self.borrowed_books[student_name].append(book_id)
            print(f"Student {student_name} borrowed '{self.books[book_id]}'.")

        except ValueError as e:
            print(f"Borrowing failed: {str(e)}")

    def return_book(self, student_name, book_id):
        try:
            if not isinstance(student_name, str) or not student_name.strip():
                raise ValueError("Student name must be a non-empty string")

            if not isinstance(book_id, str) or not book_id.strip():
                raise ValueError("Book ID must be a non-empty string")

            student_name = student_name.strip()
            book_id = book_id.strip()

            if student_name not in self.students_registered:
                raise ValueError(f"Student {student_name} is not registered with the library")

            if book_id not in self.books:
                raise ValueError(f"Book with ID {book_id} not found")

            if student_name not in self.borrowed_books or book_id not in self.borrowed_books[student_name]:
                raise ValueError(f"Student {student_name} hasn't borrowed this book")

            self.borrowed_books[student_name].remove(book_id)

            if not self.borrowed_books[student_name]:
                del self.borrowed_books[student_name]

            print(f"Student {student_name} returned '{self.books[book_id]}'.")

        except ValueError as e:
            print(f"Return failed: {str(e)}")

    def get_library_info(self):
        return (
            f"Library ID: {self.library_id}, "
            f"Total Books: {len(self.books)}, "
            f"Registered Students: {len(self.students_registered)}"
        )

    def __str__(self):
        return self.get_library_info()


class Department:
    def __init__(self, department_id, name, head_of_department):

        if not department_id:
            raise ValueError("Department ID cannot be empty")
        if not name or not isinstance(name, str):
            raise ValueError("Department name must be a non-empty string")
        if not head_of_department:
            raise ValueError("Head of Department cannot be empty")


        self.department_id = department_id
        self.name = name
        self.head_of_department = head_of_department
        self.courses_offered = []
        self.faculty_members = []

    def get_department_info(self):
        return {
            "Department ID": self.department_id,
            "Name": self.name,
            "Head of Department": self.head_of_department,
            "Courses Offered": self.courses_offered,
            "Faculty Members": self.faculty_members
        }

    def list_courses(self, courses):
        self.courses_offered = courses
        return self.courses_offered
        if not isinstance(courses, list):
            raise TypeError("Courses must be provided as a list")
        if not all(courses):
            raise ValueError("Course list contains invalid entries")

    def list_professors(self, professors):
        self.faculty_members = professors
        return self.faculty_members
        if not isinstance(professors, list):
            raise TypeError("Professors must be provided as a list")

        if not professors:
            raise ValueError("Professors list cannot be empty")




class Schedule:
    def __init__(self, schedule_id, course, professor, time_slot, location):
        self.schedule_id = schedule_id
        self.course = course
        self.professor = professor
        self.time_slot = time_slot
        self.location = location

    @dispatch(str , str , str , str, str, str)
    def assign_schedule(self, schedule_id, course, professor, time_slot, location):

        if not all([schedule_id, course, professor, time_slot, location]):
            raise ValueError("All schedule fields must be provided")
        self._init_(schedule_id, course, professor, time_slot, location)

    @dispatch(str, str, str)
    def assign_schedule(self, schedule_id, course, professor):
        if not all([schedule_id, course, professor]):
            raise ValueError("All schedule fields must be provided")
        self._init_(schedule_id, course, professor)


        

    def update_schedule(self, schedule_id=None, course=None, professor=None, time_slot=None, location=None):
        if schedule_id:
            self.schedule_id = schedule_id
        if course:
            self.course = course
        if professor:
            self.professor = professor
        if time_slot:
            self.time_slot = time_slot
        if location:
            self.location = location
        print("Schedule updated successfully.")

    def view_schedule(self):
        return {
            "Schedule ID": self.schedule_id,
            "Course": self.course,
            "Professor": self.professor,
            "Time Slot": self.time_slot,
            "Location": self.location
        }


# aya:







# habiba:


class Professor (User):
    def __init__(self, name, professor_id, email, department, password):
        super().__init__(professor_id, name, "professor",email, password)

        try:
            if not all(isinstance(val, str) and val.strip() for val in [name, professor_id, email, department]):
                raise ValueError("All professor details must be non-empty strings.")

            self.name = name.strip()
            self.__professor_id = professor_id.strip()
            self.email = email.strip()
            self.department = department.strip()
            self.courses_taught = []
            self.contact_info = []
            self.grades = {}

        except ValueError as e:
            print(f"Error initializing professor: {e}")
            raise

    def assign_grades(self, student_obj, course, grade, max_grade , exam_obj):
        try:
            if not isinstance(student_obj, student) or not student_obj:
                raise ValueError("invalid student object.")

            if not isinstance(course, str) or not course:
                raise ValueError("Course name must be a non-empty string.")

            if not (isinstance(grade, (int, float)) and isinstance(max_grade, (int, float))):
                raise ValueError("Grades must be numeric.")

            if not (0 <= grade <= max_grade):
                raise ValueError("Grade must be within the valid range.")

            if student_obj not in self.grades:
                self.grades[student_obj.student_name] = {}


            self.grades[student_obj.student_name][course] = grade
            student_obj.set_grades(course , grade)
            exam_obj.record_result( grade, student_obj.student_name )
            print(f"student name is: {student_obj.student_name}, course: {course}, the grade assigned: {grade}")



        except ValueError as e:
            print(f"Error assigning grade: {e}")
            raise







    def view_students(self):
        try:
            if not self.grades:
                print("No students have been assigned grades.")
                return

            for student, courses in self.grades.items():
                print(f"Student: {student}")
                for course, grade in courses.items():
                    print(f"  Course: {course}, Grade: {grade}")

        except Exception as e:
            print(f"Error viewing students: {e}")
            raise ValueError from e

    def get_info(self):
        try:
            print(f"Professor name: {self.name}, ID: {self.__professor_id}, Email: {self.email}, Department: {self.department}")
        except Exception as e:
            print(f"Error retrieving professor info: {e}")
            raise ValueError from e
    def view_dashboard(self):
        self.get_info()




class Course:
    def __init__(self, course_name, course_id, department, credits, professor):
        if not all(isinstance(val, str) and val.strip() for val in [course_name, course_id, department, professor]):
            raise ValueError("Course name, ID, department, and professor must be non-empty strings.")

        if not isinstance(credits, int) or credits <= 0:
            raise ValueError("Credits must be a positive integer.")

        self.course_name = course_name.strip()
        self.course_id = course_id.strip()
        self.department = department.strip()
        self.credits = credits
        self.professor = professor.strip()
        self.enrolled_students = []

    def add_students(self, student_name):
        if not isinstance(student_name, str) or not student_name.strip():
            raise ValueError("Student name must be a non-empty string.")

        if student_name in self.enrolled_students:
            raise ValueError(f"{student_name} is already enrolled in this course.")

        self.enrolled_students.append(student_name)

    def remove_course(self, student_name):
        if not isinstance(student_name, str) or not student_name.strip():
            raise ValueError("Student name must be a non-empty string.")

        if student_name not in self.enrolled_students:
            raise ValueError(f"{student_name} is not enrolled in this course.")

        self.enrolled_students.remove(student_name)

    def get_course_info(self):
        try:
            return (
                f"course_name: {self.course_name}, course_id: {self.course_id}, "
                f"department: {self.department}, credits: {self.credits}, course_professor: {self.professor}"
            )
        except Exception:
            raise ValueError("Failed to retrieve course info.")

################################################################################################################################



s130 = student("Aya", 123456, "csit", "aya@gmail.com", "121212")
s130.view_grades()
s130.view_dashboard()
#s130.login()
csc111 = Course("prog.", "CSC111", "csit",3, "issa")
s130.enroll_course(csc111)
s130.view_dashboard()
s130.drop_course(csc111)
s130.view_dashboard()
#s130.is_eligible(csc111)
s130.set_grades(csc111 , 24)



#s130.view_grades()
################################################################################################################################
#std = student("mohamed" , 124234 , "Cns" , "user@gmail.com" , 12345)
#std.enroll_course("physics 112")
#std.enroll_course("DLD")
#std.enroll_course("chemistry")
#std.get_info()


ex = Exam(1423 , "Advanced programming" , 1 , 1 , 1 )
# #
ex.schedule_exam(2024,5,26)
ex.record_result("57/60" , "Mohamed")
ex.display_student_results()
ex.view_exam_info()
################################################################################################################################

classroom_101 = Classroom("101", "Building A, Room 101", 50)
classroom_101.allocate_class("Introduction to Programming", "Monday 10:00 AM - 12:00 PM", 40)
print("Classroom availability at Monday 10:00 AM - 12:00 PM:", classroom_101.check_availability("Monday 10:00 AM - 12:00 PM"))
print(classroom_101)
main_library = Library("L001")
main_library.add_book("B001", "Python Programming")
main_library.add_book("B002", "Data Structures and Algorithms")
main_library.register_student("John Doe")
main_library.borrow_book("John Doe", "B001")
main_library.return_book("John Doe", "B001")
print(main_library)
################################################################################################################################


department1 = Department(1, "Computer Science", "Dr. Johnson")
print(department1.get_department_info())
print("Courses Offered:", department1.list_courses(["CS101", "CS102"]))
print("Faculty Members:", department1.list_professors(["Dr. Smith", "Dr. Brown"]))
print(department1.get_department_info())

schedule1 = Schedule(101, "Math 101", "Dr. Smith", "10:00 AM - 11:00 AM", "Room 202")
print(schedule1.view_schedule())
schedule1.update_schedule(time_slot="11:00 AM - 12:00 PM")
print(schedule1.view_schedule())


################################################################################################################################


cou1=Course("advanced","csc1022","programming",4453,"ahmad")
cou1.add_students("jana")
cou1.add_students("ammar")
cou1.add_students("jissi")
cou1.add_students("ghadeeer")
cou1.remove_course("ghadeeer")
#cou1. remove_course("emi")
cou1.get_course_info()

prof1=Professor("dr.john","799776","john@gmail.com","computer science", "234756")
#prof1.assign_grades("Aya","math",78,90,ex)
prof1.assign_grades(s130,"german",88,90,ex)
#prof1.assign_grades("kim","math",56,90,ex)
prof1.view_students()
prof1.get_info()
prof1.view_dashboard()
s130.view_grades()
################################################################################################################################

admn301 = Admin("301","Ahmed", "student Affairs", "admin301@gmail.com")


admn301.get_info()
admn301.view_dashboard()
admn301.add_student("m" , 123456 , "csit" , "asfads@asdas.com")

#user5871 = User(5871, "Mohamed", "Student", "mohamed@example.com", "12345")
#user5871.view_dashboard()
#user5871.login(email="mohamed@example.com", password="12345")
#user5871.view_dashboard()
#user5871.logout()
