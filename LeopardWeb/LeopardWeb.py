#test commit

#import assignment3
from ctypes import sizeof
import sqlite3
from tkinter.font import names
from typing import *

database = sqlite3.connect("LeopardWeb\\assignment3.db")
dbcursor = database.cursor()

curr_user = None

# Attributes: First, last name, ID
class User:
    def __init__(self, first_name, last_name, WIT_ID, email): # Base Class
        self.first_name = first_name
        self.last_name = last_name
        self.WIT_ID = WIT_ID
        self.email = email

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

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)
            course.students.remove(self)
            print("Removed course:", course.name)
        else:
            print("You are not enrolled in this course.")


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

class Student(User):
    def __init__(self, WIT_ID, name, surname, gradyear, major, email, courses = []):
        self.WIT_ID = WIT_ID
        self.name = name
        self.surname = surname
        self.gradyear = gradyear
        self.major = major
        self.email = email
        self.courses = courses

        dbcursor.execute(f"SELECT COURSES FROM STUDENT WHERE ID = {WIT_ID}")
        course_string = dbcursor.fetchone()[0]
        dbcursor.execute(f"SELECT ID FROM COURSES")
        course_ids = dbcursor.fetchall()

        for course_id in course_ids:
            if course_id[0] in course_string:
                courses.append(search_courses("ID", course_id[0])[0])

    # Quang and Alexander Puttre
    def add_course(self, course):
        # Check if the course is already enrolled
        if course in self.courses:
            print("You are already enrolled in this course.")
        else:
            # Check if the course has available slots
            if len(course.students) < course.max_students:
                print(course.id)

                dbcursor.execute(f"UPDATE STUDENT SET courses = (courses || ', {course.id}') WHERE email = '{self.email}'")
                database.commit()

                self.courses.append(course)
                course.add_student(self)

                print("Added course:", course.title)
            else:
                print("Course is full. Unable to enroll.")

    def time_conflict(courses):
        for i in range (0, len(courses)-1):
            for j in range (0, len(courses)-1):
                if (courses(i).time == courses(j).time):
                    if (courses(i).days == courses(j).days):
                        print(courses(i) + " conflicts " + courses(j))


    def from_search_result(search_result: str, max_students = 30):

        return Student(
                search_result[0],
                search_result[1],
                search_result[2],
                search_result[3],
                search_result[4],
                search_result[5],
                []
                )

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
        dbcursor = database.cursor()

        dbcursor.execute(f"""INSERT INTO COURSES VALUES(
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

    def remove_course(self, course):
        dbcursor = database.cursor()

        dbcursor.execute(f"DELETE FROM COURSES WHERE ID = '{course.id}'")

        database.commit()
 
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


def check_database(email, id, password):
    dbcursor = database.cursor()


    ##cursor.execute(f"ALTER TABLE INSTRUCTOR ADD PASSWORD text NOT NULL'")
    ##cursor.execute(f"ALTER TABLE ADMIN ADD PASSWORD text NOT NULL'")


    query1 = f"SELECT * FROM ADMIN WHERE email = \'{email}\' AND ID = \'{id}\' AND PASSWORD = \'{password}\'"
    dbcursor.execute(query1)
    query1_result = dbcursor.fetchone()

    query2 = f"SELECT * FROM INSTRUCTOR WHERE email = \'{email}\' AND ID = \'{id}\' AND PASSWORD = \'{password}\'"
    dbcursor.execute(query2)
    query2_result = dbcursor.fetchone()

    query3 = f"SELECT * FROM STUDENT WHERE email = \'{email}\' AND ID = \'{id}\' AND PASSWORD = \'{password}\'"
    dbcursor.execute(query3)
    query3_result = dbcursor.fetchone()

    if query1_result:
        return "admin"

    elif query2_result:
        return "instructor"

    elif query3_result:
        return "student"
    else:
        return ""


def search_courses(search_criterion: str, value: str) -> list:
    dbcursor = database.cursor()

    search_criterion = search_criterion.upper()

    query = ""

    match search_criterion:
        case "ID":
            query = f"SELECT * FROM COURSES WHERE {search_criterion} = \'{value}\'"
        case "TITLE":
            query = f"SELECT * FROM COURSES WHERE {search_criterion} = \'{value}\'"
        case "DEPARTMENT":
            query = f"SELECT * FROM COURSES WHERE {search_criterion} = \'{value}\'"
        case "TIME":
            query = f"SELECT * FROM COURSES WHERE {search_criterion} = \'{value}\'"
        case "DAYS":
            query = f"SELECT * FROM COURSES WHERE {search_criterion} = \'{value}\'"
        case "SEMESTER":
            query = f"SELECT * FROM COURSES WHERE {search_criterion} = \'{value}\'"
        case "YEAR":
            query = f"SELECT * FROM COURSES WHERE {search_criterion} = {value}"
        case "CREDITS":
            query = f"SELECT * FROM COURSES WHERE {search_criterion} = {value}"
        case _:
            raise Exception("Invalid search criterion")

    dbcursor.execute(query)
    result = dbcursor.fetchall()

    search_matches = []

    for i in result:
        search_matches.append(Course.from_search_result(i))

    return search_matches

def search_students(search_criterion: str, value: str) -> list:
    dbcursor = database.cursor()

    search_criterion = search_criterion.upper()

    query = ""

    match search_criterion:
        case "ID":
            query = f"SELECT * FROM STUDENT WHERE {search_criterion} = \'{value}\'"
        case "NAME":
            query = f"SELECT * FROM STUDENT WHERE {search_criterion} = \'{value}\'"
        case "SURNAME":
            query = f"SELECT * FROM STUDENT WHERE {search_criterion} = \'{value}\'"
        case "GRADYEAR":
            query = f"SELECT * FROM STUDENT WHERE {search_criterion} = \'{value}\'"
        case "MAJOR":
            query = f"SELECT * FROM STUDENT WHERE {search_criterion} = \'{value}\'"
        case "EMAIL":
            query = f"SELECT * FROM STUDENT WHERE {search_criterion} = \'{value}\'"
        case "COURSES":
            query = f"SELECT * FROM STUDENT WHERE {search_criterion} = {value}"
        case _:
            raise Exception("Invalid search criterion")

    dbcursor.execute(query)
    result = dbcursor.fetchall()

    search_matches = []

    for i in result:
        search_matches.append(Student.from_search_result(i))


    return search_matches


def display_courses(to_display = None):
    dbcursor = database.cursor()

    courses = []
    if to_display == None:
        from_db = dbcursor.execute("SELECT * FROM COURSES")
        for i in from_db:
            courses.append(Course.from_search_result(i))
    else:
        courses = to_display

    for course in courses:
        print(course)


def search_courses_menu():
    exit = 0
    while exit == 0:
        user_input = int(input("\nSelect which attribute you would like to search by:\n1- ID\n2- Title\n3- Department\n4- Time\n5- Days\n6- Semester\n7- Year\n8- Credits\n"))

        if (user_input < 1 or user_input > 8):
            print("Invalid input\n")
        else:
            exit = 1

    search_criterion = ["ID", "TITLE", "DEPARTMENT", "TIME", "DAYS", "SEMESTER", "YEAR", "CREDITS"][user_input - 1]
    search_value = input(f"\nSearch for courses with {search_criterion.lower()}: ")
    search_results = search_courses(search_criterion, search_value)

    num_results = len(search_results)
    if(num_results > 0):
        print(f"\nThere {'is' if num_results == 1 else 'are'} {num_results} {'course' if num_results == 1 else 'courses'} with {search_criterion.lower()} = {search_value}:\n")
        display_courses(search_results)
    else:
        print(f"\nNo courses matching search criterion {search_criterion.lower()} = {search_value}")



if __name__ == "__main__":
    exit = False
    while not exit:
        username = ""
        user_type = ""
        exit = False
        while user_type == "":
            print("\nWelcome! Login:\n \n")
            username = input("Username:\n")
            WIT_ID = int(input("WIT_ID: \n"))
            password = input("Password: \n")

            user_type = check_database(username, WIT_ID, password)

            if user_type == "":
                print("Error: user not found. Please try again\n")
            else:
                print(f"Logged in successfully as {user_type}!\n")

        if user_type == "student":
            print("----------Student Options-----------\n\n")

            user = search_students("email", username)[0]

            print(user.name)
            print(user.courses)

            while user_type != "":
                print("Choose one of the following options:\n")
                student_choice = int(input("\n1- Log out\n2- Search all courses\n3- Add / Remove courses from semester schedule\n4- Display semester schedule\n5- Display all courses\n\n"))
                if student_choice == 1:
                    print(f"Goodbye {username}!\n")
                    user_type = ""
                elif student_choice == 2:
                    search_courses_menu()
                elif student_choice == 3:
                    user_input1 = int(input("\n1- Add course\n2- Remove course\n"))
                    if user_input1 == 1:
                        user_input2 = input("Enter the id of the course to add: ")
                        user.add_course(search_courses("id", user_input2)[0])

                        for i in user.courses:
                            print(i)

                elif student_choice == 4:
                    display_courses(user.courses)
                elif student_choice == 5:
                    display_courses()
                else:
                    print("Please choose from one of the displayed options\n")
        elif user_type == "admin":
            print("---------Admin menu---------\n\n")

            while user_type != "":
                print("Choose one of the following options:\n")
                admin_choice = int(input("\n1- Log out\n2- Search all courses\n3- Add /Remove courses from the system\n4- Display all courses\n\n"))
                if admin_choice == 1:
                    print(f"Goodbye {username}!\n")
                    user_type = ""
                elif admin_choice == 2:
                    search_courses_menu()
                elif admin_choice == 3:
                    user_input = int(input("\n1- Add course\n2- Remove course\n\n"))
                    match user_input:
                        case 1:
                            course_id = str(input("ID: "))
                            course_title = str(input("Title: "))
                            course_department = str(input("Department: "))
                            course_time = str(input("Time: "))
                            course_days = str(input("Days: "))
                            course_semester = str(input("Semester: "))
                            course_year = int(input("Year: "))
                            course_credits = int(input("Credits: "))

                            Admin.add_course(None, Course(course_id, course_title, course_department, course_time, course_days, course_semester, course_year, course_credits))
                        case 2:
                            user_input = input("Enter the id of the course you would like to remove: ")
                            search_results = search_courses("id", user_input)
                            if (len(search_results) > 0):
                                Admin.remove_course(None, search_results[0])
                            else:
                                print(f"No course with id {user_input} found in database\n")
                        case _:
                            print("Invalid selection\n")
                elif admin_choice == 4:
                    display_courses()
                else:
                    print("Please choose from one of the displayed options\n")
        elif user_type == "instructor":
            print("---------Instructor Options---------\n\n")

            user = Instructor(username)

            while user_type != "":
                print("Choose one of the following options:\n")
                instructor_choice = int(input("\n1- Exit\n2- Search all courses\n3- Assemble and print course roster\n4- Display all Courses\n\n"))
                if instructor_choice == 1:
                    print(f"Goodbye {username}!\n")
                    user_type = ""
                elif instructor_choice == 2:
                    search_courses_menu()
                elif instructor_choice == 3:
                    user_input = int(input("\n1- Add a course to your roster\n2- Remove a course from your roster\n3- Print your course roster\n\n"))
                    match user_input:
                        case 1:
                            user_input = input("Enter the id of the course you would like to add: ")
                            search_results = search_courses("id", user_input)
                            if (len(search_results) > 0):
                                user.add_course(search_results[0])
                                print(f"Course {user_input} has been added to your roster.\n")
                            else:
                                print(f"No course with id {user_input} found in the database\n")
                        case 2:
                            if (len(user.course_list) > 0):
                                print("Your course roster:\n")
                                display_courses(user.course_list)
                                user_input = input("Enter the id of the course you would like to remove: ")
                                search_results = search_courses("id", user_input)
                                if (len(search_results) > 0):
                                    user.remove_course(search_results[0])
                                    print(f"Course {user_input} has been removed from your roster.\n")
                                else:
                                    print(f"No course with id {user_input} found in the database\n")
                            else:
                                print("You have no courses to remove\n")
                        case 3:
                            user.print_courses()
                elif instructor_choice == 4:
                    display_courses()
                else:
                    print("Please choose from one of the displayed options\n")

        user_input = ""
        while(user_input == ""):
            user_input = input("Log in as another user? y/n\n")
            match user_input:
                case "y":
                    break
                case "n":
                    exit = True
                case _:
                    print("Please enter \"y\" or \"n\"")
                    user_input = ""

    database.close()

check = 0
