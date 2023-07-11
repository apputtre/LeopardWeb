#test commit

#import assignment3
from ctypes import sizeof
import sqlite3
from typing import *

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

# Quang Vu & Alexander Puttre
class Course(User):
    def __init__(self, id: str, title: str, department: str, time: str, days: str, semester: str, year: int, credits: int, max_students = 30):
        self.id = id
        self.title = title
        self.department = department
        self.time = time
        self.days = days
        self.semester = semester
        self.year = year
        self.credits = credits
        self.max_students = max_students    # Max students that can be enrolled

        self.students = []                  # List of studnets 

    def from_search_result(search_result: str, max_students = 30):

        return Course(
                search_result[0],
                search_result[1],
                search_result[2],
                search_result[3],
                search_result[4],
                search_result[5],
                search_result[6],
                search_result[7],
                max_students
                )

    def __repr__(self):
        return f"ID: {self.id}, title: {self.title}, department: {self.department}, time: {self.time}, days: {self.days}, semester: {self.semester}, year: {self.year}, credits: {self.credits}, max_students: {self.max_students}"

    def __eq__(self, other):
        return self.id == other.id

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

    def remove_course(self, course):
        self.course_list.remove(course)

    def print_courses(self):
        if (len(self.course_list) > 0):
            print("Prof.", self.first_name)
            display_courses(self.course_list)
        else:
            print("Your course roster is empty\n")


class Admin(User):
    # The super() function allows the methods & attributes of the parent class.
    def __init__(self, first_name, last_name, WIT_ID):
        super().__init__(first_name, last_name, WIT_ID)

    def add_course(self, course):
        database = sqlite3.connect("assignment3.db")
        cursor = database.cursor()

        cursor.execute(f"""INSERT INTO COURSES VALUES(
                "{course.id}",
                "{course.title}",
                "{course.department}",
                "{course.time}",
                "{course.days}",
                "{course.semester}",
                {course.year},
                {course.credits}
            )
           """
        )

        database.commit()
        database.close()

    def remove_course(self, course):
        database = sqlite3.connect("assignment3.db")
        cursor = database.cursor()

        cursor.execute(f"DELETE FROM COURSES WHERE ID = '{course.id}'")

        database.commit()
        database.close()
 
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

"""

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


# How to put a txt or .db file
##
