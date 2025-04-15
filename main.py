# mohmmed: 
from datetime import date 
class student:
    
    ##remove this from here and handle but in other way
    available_courses = ["Advanced programming" , "fundementals of programming" , "physics 112" , "Math 111" , "DLD"]

    def __init__(self, student_name , student_id , major , email ):
        self.student_name = student_name
        self.student_id = student_id
        self.major = major
        self.email = email
        self.courses_enrolled = []
        self.grades = {}


    def enroll_course(self , course):
        ##handle if the student already enrolled or not
        if course in self.available_courses:
            self.courses_enrolled.append(course)
            print (f"{self.student_name} has enrolled in {course}")

        else:
            print(f" no such course as {course}")


    def drop_course(self , course):
        if course in self.available_courses:

            if course in self.courses_enrolled:
                self.courses_enrolled.remove(course)
                print(f"{self.student_name} has dropped {course}")

            else:
                print(f"{self.student_name} is not currently enrolled in this course")

        else:
            print("this course does not exist")


    def assign_grades(self):
        pass


    def view_grades(self):
        pass

#how do i make it so that it shows the grade of each enrolled course , based on the grade assigned from the "view_grade"

    def get_info(self):
        print("****************************STUDENT INFO****************************")

        print(f"Student's name : {self.student_name} , Student's id : {self.student_id} , student's major : {self.major}")
        print(f"student's email : {self.email}")
        print(f"Student's enrolled courses : {self.courses_enrolled}") 

        print("********************************************************************")





class Exam:
    def __init__(self , exam_id , course ,  duration , student_results ,exam_date=None):
        self.exam_id = exam_id
        self.course = course
        self.exam_date = exam_date      
        self.duration = duration
        self.student_results = {}

    def schedule_exam(self , year , month , day):
        while True:
            try:
                self.exam_date = date(year , month , day)
                break
            except ValueError:
                print("Invalid date. please enter a valid date")
            


    def record_result(self , score , student_name):
        self.student_results[student_name] = score
        print(f"{student_name}' results have been saved as {score}")

    ## handle the grades attribute of Student and Professor classes
       

    def display_student_results(self):
        print("")
        print("****************************EXAM RESULTS****************************")
        print(f"result for exam {self.exam_id} in course {self.course} : ")
        for student, score in self.student_results.items():
            print(f"student : {student}'s score is {score}")
        print("********************************************************************")

    def view_exam_info(self):
        print(" ")
        print("*****************************EXAM INFO*****************************")
        print(f"exam ID : {self.exam_id} , course : {self.course}")
        if self.exam_date:
            print(f"{self.exam_id} is scheduled for {self.exam_date.strftime('%y-%m-%d')}" )
        else:
            print("exam has no scheduled date yet")
        print("*******************************************************************")

 
# adham: 
class Classroom:
    def __init__(self, classroom_id, location, capacity):
        self.classroom_id = classroom_id
        self.location = location
        self.capacity = capacity
        self.schedule = {}  

     ## use check avilabilty here for code reusability
    def allocate_class(self, course_name, time_slot, num_students):
        if time_slot not in self.schedule:
            if num_students <= self.capacity:
                self.schedule[time_slot] = course_name
                print(f"Classroom {self.classroom_id} allocated for {course_name} at {time_slot}.")
            else:
                print(f"Classroom {self.classroom_id} cannot accommodate {course_name} (capacity exceeded).")
        else:
            print(f"Classroom {self.classroom_id} is already booked at {time_slot}.")

    def check_availability(self, time_slot):
        if time_slot not in self.schedule:
            return "Available"
        return "Booked"

    def get_classroom_info(self):
        return f"Classroom ID: {self.classroom_id}, Location: {self.location}, Capacity: {self.capacity}"

    def __str__(self):  
        return self.get_classroom_info()



class Library:
    def __init__(self, library_id):
        self.library_id = library_id
        self.books = {}  # Dictionary to store books (key: book_id, value: book_name)
        ## self.students_registered = set() ?????????????? 
        self.students_registered = set()  # Set to store registered student names

    def add_book(self, book_id, book_name):
        self.books[book_id] = book_name
        print(f"Book '{book_name}' added to the library.")

    ## can be handeled by another way?
    def register_student(self, student_name):
        self.students_registered.add(student_name)
        print(f"Student {student_name} registered with the library.")

    ## we need dictionry to contain data about the students and borrowed books
    def borrow_book(self, student_name, book_id):
        if student_name in self.students_registered:
            if book_id in self.books:
                print(f"Student {student_name} borrowed '{self.books[book_id]}'.")
            else:
                print(f"Book with ID {book_id} not found.")
        else:
            print(f"Student {student_name} is not registered with the library.")

    def return_book(self, student_name, book_id):
        if student_name in self.students_registered:
            if book_id in self.books:
                print(f"Student {student_name} returned '{self.books[book_id]}'.")
            else:
                print(f"Book with ID {book_id} not found.")
        else:
            print(f"Student {student_name} is not registered with the library.")

    def get_library_info(self):
        return f"Library ID: {self.library_id}, Total Books: {len(self.books)}"

    def __str__(self):  # Overriding (string representation)
        return self.get_library_info()


# arwa:
class Department:
    def __init__(self, department_id, name, head_of_department):
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

    def list_professors(self, professors):
        self.faculty_members = professors
        return self.faculty_members


class Schedule:
    def __init__(self, schedule_id, course, professor, time_slot, location):
        self.schedule_id = schedule_id
        self.course = course
        self.professor = professor
        self.time_slot = time_slot
        self.location = location

    def assign_schedule(self, schedule_id, course, professor, time_slot, location):
        ## give it another function (as it does the same as constructor)
        self.schedule_id = schedule_id
        self.course = course
        self.professor = professor
        self.time_slot = time_slot
        self.location = location
        print("Schedule assigned successfully.")

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

class Admin:    
    
    def __init__(self, admin_id, name, role, contact_info):
        self.admin_id = admin_id
        self.name = name
        self.role = role
        self.contact_info = contact_info

    def add_student(self, course, student): 
        if course not in student.courses_enrolled and student not in course.enrolled_students:
            student.courses_enrolled.append(course)
            course.enrolled_students.append(student)
            print("student added sucessfully")
        else:
            print("ERROR, failed to add student, student may be already enrolled")


    def remove_student(self, course, student):
        if course in student.courses_enrolled and student in course.enrolled_students:
            student.courses_enrolled.remove(course)
            course.enrolled_students.remove(student)
        else:
            print("ERROR, failed to remove student, student may be NOT enrolled")



    def assign_professor(self, course, professor):
        ## check lw el prof. ynf3 ydi elmada de asln wla laa
        if course not in professor.courses_taught:
            professor.courses_taught.append(course)
            course.professor = professor
            print(f"prof. {professor.name} is assigned to course: {course.course_id}")


    def manage_course(self, operation, course, department):
        ## create course object eih raykom??
        if operation.lower == "add":
            if course not in department.courses_offered:
                department.courses_offered.append(course)
                print(f"course {course} added sucessfuly to department of {department}")
            else:
                print("CAN NOT BE ADDED. course already exists")
        if operation.lower() == "remove":
            if course in department.courses_offered:
                department.courses_offered.remove(course)
                print("course {course} removed sucessfuly from department of {department}")
            else:
                print("ERROR course doesn't exists")

   


class User:
    # eldoctor mkansh kateb password bs m7tagenha fe el login
    def __init__(self, user_id, name, role, email, __password):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.email = email
        self.__password = __password
        self.logged_in = False

    def login(self, email, password):
        if email == self.email and password == self.__password:
            self.logged_in = True
            print("logged in sucessfully")
            #3aizen n3ml option eno y create account
        else:
            print("invalid email or password")

    def logout(self):
        self.logged_in = False
        print("loged out sucessfully")

    def view_dashboard(self):
        print(f"Dashboard of : {self.name}")
        print(f"user data: \n Name: {self.name} \n role: {self.role} \n Id: {self.user_id} \n Email: {self.email}")


# habiba:
class professor:
    def __init__(self,name ,professor_id,email,department):
        self.name = name
        self.professor_id = professor_id
        self .email = email
        self.department = department
        self.courses_taught = []
        self.contact_info = []
        self.grades ={}
        
        
    def assign_grades(self,student_name,course,grade, max_grade):
        if 0 <= grade <= max_grade:
          if student_name not in self.grades:
              self.grades[student_name] = {}  
              self.grades[student_name][course] = grade 
              print(f"student name is:,{student_name},course:,{course},the grade assigned:,{grade}")
              
              
              
    def view_students(self):
        if not self.grades:
            print("No students have been assigned grades.")
        else:

            for student, courses in self.grades.items():
                print(f"Student: {student}")
            for course, grade in courses.items():
                    print(f"  Course: {course}, Grade: {grade}")

    
    
    
    def get_professor_info(self):
        print(f"professor name:,{self.name},id:,{self.professor_id},email:,{self.email},department:,{self.department}")
        
        
        


class course:
    def __init__(self ,course_name,course_id,department,credits,professor):
      self.course_name=course_name
      self.course_id=course_id
      self.department=department
      self.credits=credits
      self.professor=professor
      self.enrolled_students=[]
      
      
      
    def add_students(self,student_name):
        if student_name not in self.enrolled_students:
          self.enrolled_students.append(student_name)
          print(f"{student_name}has enrolled in  {self.course_name} course")
        else:
            print(f"{student_name}is already enrolled in this course")
            
            
            
    def remove_course(self, student_name):
       if student_name in self.enrolled_students:
          self.enrolled_students.remove(student_name)
          print(f"{student_name},is removed from{self.course_name},course")
       else:
              print(f"{student_name}is already not enrolled in this course")
              
              
              
    def get_course_info(self):
         print(f"course_name:{ self.course_name},course_id:{self.course_id},department:{self.department},credits:{self.credits},course_professor:{self.professor}")
    
    
################################################################################################################################
std = student("mohamed" , 124234 , "Cns" , "user@gmail.com" )
std.enroll_course("physics 112")
std.enroll_course("DLD")
std.enroll_course("chemistry")
std.get_info()


ex = Exam(1423 , "Advanced programming" , None , None , None )
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

schedule1 = Schedule(101, "Math 101", "Dr. Smith", "10:00 AM - 11:00 AM", "Room 202")
print(schedule1.view_schedule())
schedule1.update_schedule(time_slot="11:00 AM - 12:00 PM")
print(schedule1.view_schedule())


################################################################################################################################


cou1=course("advanced","csc1022","programming",4453,"ahmad")
cou1.add_students("jana")
cou1.add_students("ammar")
cou1.add_students("jissi")
cou1. remove_course("ghadeeer")
cou1. remove_course("emi")
cou1. get_course_info()       
   
prof1=professor("dr.john","p799776","john@gmail.com","computer science")
prof1.assign_grades("ahmad","math",78,90)
prof1.assign_grades("ghadeer","german",88,90)
prof1.assign_grades("kim","math",56,90)
prof1.view_students()            


################################################################################################################################

admn301 = Admin(301,"Ahmed", "student Affairs", "admin301@gmail.com")
admn301.add_student(cou1,std)
admn301.remove_student(cou1,std)
admn301.assign_professor(cou1,prof1)
admn301.manage_course("add", cou1, department1)

user5871 = User(5871, "Mohamed", "Student", "mohamed@example.com", "12345")
user5871.view_dashboard()
user5871.login(email="mohamed@example.com", password="12345")
user5871.view_dashboard()
user5871.logout()
