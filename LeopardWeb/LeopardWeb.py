#test commit

import sqlite3

database = sqlite3.connect("assignment3.db")
cursor = database.cursor() 

cursor.execute("INSERT INTO STUDENT VALUES(10011, 'Yasmina', 'Habchi', 2024, 'BSCO', 'habchiy');")
cursor.execute("INSERT INTO STUDENT VALUES(10012, 'Quang', 'Vu', 2024, 'BSCO', 'vuq1');")

cursor.execute("DELETE FROM INSTRUCTOR WHERE id = 20003;")

cursor.execute("UPDATE ADMIN SET title='Vice-President' WHERE id=30002;")

cursor.execute("""
CREATE TABLE COURSES (
ID TEXT PRIMARY KEY NOT NULL,
TITLE TEXT NOT NULL,
DEPARTMENT TEXT NOT NULL,
TIME TEXT NOT NULL,
DAYS TEXT NOT NULL,
SEMESTER TEXT NOT NULL,
YEAR INTEGER NOT NULL,
CREDITS INTEGER NOT NULL)
;
""")

cursor.execute("INSERT INTO COURSES VALUES('ELEC3600', 'Signals & Systems', 'BSEE', '10:00-11:50', 'MW', 'Summer', 2023, 4);")
cursor.execute("INSERT INTO COURSES VALUES('HUMN4243', 'Contemporary Art & Theory', 'HUSS', '10:00-11:50', 'TR', 'Fall', 2023, 4);")
cursor.execute("INSERT INTO COURSES VALUES('COMP1000', 'Computer Science I', 'BSCO', '14:00-14:50', 'MWF', 'Fall', 2023, 4);")
cursor.execute("INSERT INTO COURSES VALUES('MECH2000', 'Engineering Statics', 'BSME', '13:00-14:50', 'TR', 'Fall', 2023, 4);")
cursor.execute("INSERT INTO COURSES VALUES('COMP1200', 'Computer Organization', 'BSCO', '14:00-15:20', 'MW', 'Fall', 2023, 4);")

print("Courses:")
cursor.execute("SELECT * FROM COURSES")
query_result = cursor.fetchall()
for i in query_result:
    print(i)

print()

print("Admins:")
cursor.execute("""SELECT * FROM ADMIN""")
query_result = cursor.fetchall()

for i in query_result:
    print(i)

print("\nStudents")
cursor.execute("""SELECT * FROM STUDENT""")
query_result = cursor.fetchall()

for i in query_result:
    print(i)

print("\nInstructors:")
cursor.execute("""SELECT * FROM INSTRUCTOR""")
query_result = cursor.fetchall()

for i in query_result:
    print(i)

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
course1.add_student(S4)
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
