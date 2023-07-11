#test commit

#import assignment3
import sqlite3

database = sqlite3.connect("assignment3.db")

# Attributes: First, last name, ID
class User:
    def __init__(self, first_name, last_name, WIT_ID): # Base Class
        self.first_name = first_name
        self.last_name = last_name
        self.WIT_ID = WIT_ID

    def first(self):
        print("First name:", self.first_name)

    def last(self):
        print("Last name:", self.last_name)

    def ID(self):
        print("ID: ", self.WIT_ID)

    def speak(self):
        print("Goverment Name:", self.first_name, self.last_name)
        print("My WIT ID is:", self.WIT_ID)

    # Quang
    def add_course(course):
        # Check if the course is already enrolled
        if course in self.courses:
            print("You are already enrolled in this course.")
        else:
            # Check if the course has available slots
            if len(course.students) < course.max_students:
                self.courses.append(course)
                course.add_student(self)
                print("Added course:", course.name)
            else:
                print("Course is full. Unable to enroll.")

    # Quang
    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)
            course.students.remove(self)
            print("Removed course:", course.name)
        else:
            print("You are not enrolled in this course.")

    def search_courses(self):
        print("Searching my courses...")


class Course(User):
    def __init__(self, name, max_students):
        self.name = name
        self.max_students = max_students    # Max students that can be enrolled
        self.students = []                  # List of studnets 

 # Students can add a course to their schedule but will have a max threshold.
    def add_student(self, student):
        if len(self.students) < self.max_students:
            self.students.append(student)
            return True
        return False                        # If students exceed the threshold, it will return a false




class Instructor(User):
    def __init__(self, first_name):
        self.first_name = first_name
        self.course_list = []               # Will list the # of courses

    def add_course(self, course):
        self.course_list.append(course)

    def print_courses(self):
        print("Professor.", self.first_name)
        for course in self.course_list:
            print(course.name)


class Admin(User):
    # The super() function allows the methods & attributes of the parent class.
    def __init__(self, first_name, last_name, WIT_ID):
        super().__init__(first_name, last_name, WIT_ID)

    def add_course(self, course):
        #self.course_list.append(course)
        print("Adding course:", course.name)

    def remove_course(self, course):
        print("Removing course:", course.name)
 
    def add_user_course(self, user, course):
        print("Student:", user.first_name, user.last_name, "has been added to:", course.name)

    def remove_user_course(self, user, course):
        print("Sudent", user.first_name, user.last_name, "has been removed from:", course.name)

    def add_user(self, user):
        print("Added student:", user.first_name, user.last_name)

    def remove_user(self, user):
        print("Removed student:", user.first_name, user.last_name)

    # Query is used to address the dataframe. In this case it searches for the course name
    def search(self, query):
        print("Searching for:", query)

    def print_course(self, course):
        print("Course Name:", course.name)
        print("Maximum Students:", course.max_students)
        print("Enrolled Students:", len(course.students))
        print ("\n")  

    def print_roster(self, course):
        print("Class list:", course.name)
        for student in course.students:
            print(student.first_name, student.last_name, "| WIT_ID:", student.WIT_ID)
        print ("\n")  





# What if I want 100+ students
S1 = User("Quang", "Vu.", "W00000")
S2 = User("Alex", "Puttre.", "W00001")
S3 = User("Yasmina", "Habchi.", "W00002")
S4 = User("Liam", "Nasar.", "W00003")
#S1.speak()
#S2.speak()
#S3.speak()
#S4.speak()
print()


# Create a class called course1
course1 = Course("Applied Programming Concepts", 3) # 3 stands for max threshold

# Instructure1 is the name for the professor when you call it. 
instructor1 = Instructor("Rawlins")

# Adding professor to a "course1"
instructor1.add_course(course1)

# Add students to a specific course
course1.add_student(S1)
course1.add_student(S2)
course1.add_student(S3)


# Print course roster (Instructor & Admin)
for student in course1.students:
    print("First Name:", student.first_name)
    print("Last Name:", student.last_name)
    print("ID:", student.WIT_ID)
    print()

'''
# What classes does each professor teach?
instructor1.print_courses()
print()
'''

# Remove the commenting to use admin prviliges 
'''
admin = Admin("Admin", "Headmaster", "WIT_ADMIN")
admin.search("Applied Programming") # CaSe SenSiTiVe
admin.print_roster(course1)
admin.print_course(course1)
admin.remove_course(course1)
admin.add_course(course1)
admin.add_user(S1)
admin.remove_user(S2)
admin.add_user_course(S1, course1)
admin.remove_user_course(S1, course1)
'''



## Yasmina: Login - Logout && Menu to implement changes
def check_database(email, id):
    database = sqlite3.connect("assignment3.db")
    cursor = database.cursor()

    query1 = f"SELECT * FROM ADMIN WHERE email = \'{email}\' AND ID = \'{id}\'"
    cursor.execute(query1)
    query1_result = cursor.fetchone()

    query2 = f"SELECT * FROM INSTRUCTOR WHERE email = \'{email}\' AND ID = \'{id}\'"
    cursor.execute(query2)
    query2_result = cursor.fetchone()

    query3 = f"SELECT * FROM STUDENT WHERE email = \'{email}\' AND ID = \'{id}\'"
    cursor.execute(query3)
    query3_result = cursor.fetchone()

    database.close()

    if query1_result:
        print("Login as admin successful!")
        return "admin"

    elif query2_result:
        print("Login as instructor successful!")
        return "instructor"

    elif query3_result:
        print("Login as student successful!")
        return "student"
    else:
        print("Login error!")
        return ""


def check_courses(course_id):
    database = sqlite3.connect("assignment3.db")
    cursor = database.cursor()

    query4 = f"SELECT * FROM COURSES WHERE id = \'{course_id}\'"
    cursor.execute(query4)
    query4_result = cursor.fetchone()

    if query4_result:
        print("Course found!")
        return "course_id"

    else:
        print("No course code available!")
        return ""




check = 0

while check != 1:
    print("\nWelcome! Login:\n \n")
    username = input("Username:\n")
    WIT_ID = int(input("WIT_ID: \n"))
    password = input("Password: \n")

    user_type = check_database(username, WIT_ID)

    if user_type == "student":
        print("----------Student Options-----------\n\n")
        print("Choose one of the following options:\n")
        student_choice = int(input("\n1- Search all courses\n2- Add / Remove courses from semester schedule\n\n"))
        if student_choice == 1:
            course_id = input("\nWhat is the course code you're searching for: \n")
            check_coursecode = check_courses(course_id)
            if check_coursecode == "course_id":
                print("COURSE: ")
            else:
                print("Error in course code!")
            

        else:
            print("\nError!")
        check = 1

    elif user_type == "admin":
        print("---------Admin menu---------\n\n")
        print("Choose one of the following options:\n")
        admin_choice = int(input("\n1- Search all courses\n2- Add /Remove courses from the system\n\n"))
        if admin_choice == 1:
             course_id = input("\nWhat is the course code you're searching for: \n")
             check_coursecode = check_courses(course_id)
             if check_coursecode == "course_id":
                    print("COURSE: ")
             else:
                    print("Error in course code!")
        else:
            print("\nError!")
        check = 1

    elif user_type == "instructor":
        print("---------Instructor Options---------\n\n")
        print("Choose one of the following options:\n")
        instructor_choice = int(input("\n1- Search all courses\n2- Assemble and print course roster\n\n"))
        if instructor_choice == 1:
             course_id = input("\nWhat is the course code you're searching for: \n")
             check_coursecode = check_courses(course_id)
             if check_coursecode == "course_id":
                print("COURSE: ")
             else:
                print("Error in course code!")
        else:
            print("\nError!")
        check = 1

    else:
         print("Login Error!")
         check = 0



    # Quang: Add/Remove courses based on course ID



''' check = 0

while check != 1:
    print("\nChoose from the following options:\n1- Login Admin\n2- Login Instructor\n3- Login Student\n")
    choice = int(input("Enter here: "))

    if choice == 1:
        firstname = input("Enter admin's first name: ")
        lastname = input("Enter admin's last name: ")
        WIT_ID = int(input("Enter admin's ID: "))
        password = input("Enter password: ")

        person1 = Admin(firstname, lastname, WIT_ID)

        print("1- OPTION 1\n 2- OPTION 2\n 3- OPTION 3...")
        adminchoice = int(input("Enter a number: "))

        if adminchoice == 1:
            print("OPTION 1")
        elif adminchoice == 2:
            print("OPTION 2")
        elif adminchoice == 3:
            print("OPTION 3")

        check = 0

    elif choice == 2:
        firstname = input("Enter instructor's first name: ")
        lastname = input("Enter instructor's last name: ")
        WIT_ID = int(input("Enter instructor's ID: "))

        person1 = Instructor(firstname, lastname, WIT_ID)
        
        print("1- OPTION 1\n 2- OPTION 2\n 3- OPTION 3...")
        instructorchoice = int(input("Enter a number: "))

        if instructorchoice == 1:
            print("OPTION 1")
        elif instructorchoice == 2:
            print("OPTION 2")
        elif instructorchoice == 3:
            print("OPTION 3")

        check = 0
        

    elif choice == 3:
        firstname = input("Enter student's first name: ")
        lastname = input("Enter student's last name: ")
        WIT_ID = int(input("Enter student's ID: "))

        person1 = User(firstname, lastname, WIT_ID)
        
        print("1- OPTION 1\n 2- OPTION 2\n 3- OPTION 3...")
        studentchoice = int(input("Enter a number: "))

        if studentchoice == 1:
            print("OPTION 1")
        elif studentchoice == 2:
            print("OPTION 2")
        elif studentchoice == 3:
            print("OPTION 3")

        check = 0

    else:
        check = 1

print("Error! Please select one of the following options: ")
print("\nChoose from the following options:\n1- Login Admin\n2- Login Instructor\n3- Login Student\n")
choice = int(input("Enter your choice: "))
'''
