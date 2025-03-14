# mohmmed: 
class student:

    available_courses = ["Advanced programming" , "fundementals of programming" , "physics 112" , "Math 111" , "DLD"]

    def __init__(self, student_name , student_id , major , email):
        self.student_name = student_name
        self.student_id = student_id
        self.major = major
        self.email = email
        self.courses_enrolled = []
        self.grades = {}


    def enroll_course(self):
        
        if course in available_courses:
            self.courses_enrolled.append(course)
            print (f"{self.student_name} has enrolled in {course}")

        else:
            print(f" no such course as {course}")


    def drop_course(self):
        if course in available_courses:

            if course in courses_enrolled:
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
        print(f"Student's name : {self.student_name} , Student's id : {self.student_id} , student's major : {self.major}")
        print(f"student's email : {self.email}")
        print(f"Student's enrolled courses : {self.courses_enrolled}") 
    
# adham:
# arwa:
# habiba:
# aya: