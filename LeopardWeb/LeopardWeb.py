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
    def __init__(self, id: str, title: str, department: str, time: str, days: str, semester: str, year: int, credits: int, max_students = 30, students = []):
        self.id = id
        self.title = title
        self.department = department
        self.time = time
        self.days = days
        self.semester = semester
        self.year = year
        self.credits = credits
        self.max_students = max_students    # Max students that can be enrolled
        self.students = students            # List of students 

        #dbcursor.execute(f"SELECT STUDENTS FROM COURSES WHERE ID = \'{id}\'")
        #students_string = dbcursor.fetchone()[0]
        #dbcursor.execute(f"SELECT ID FROM STUDENT")
        #student_ids = dbcursor.fetchall()

        #for student_id in student_ids:
        #    if str(student_id[0]) in students_string:
        #        self.students.append(search_students("ID", student_id[0])[0])

    def from_search_result(search_result: str, max_students = 30):

        #dbcursor.execute(f"SELECT STUDENTS FROM COURSES WHERE ID = \'{search_result[0]}\'")
        #students_string = dbcursor.fetchone()[0]
        #dbcursor.execute(f"SELECT ID FROM STUDENT")
        #student_ids = dbcursor.fetchall()

        #students = []

        #for student_id in student_ids:
        #    student_id = str(student_id[0])
        #    if student_id in students_string:
        #        students.append(search_students("ID", student_id)[0])

        return Course(
                search_result[0],
                search_result[1],
                search_result[2],
                search_result[3],
                search_result[4],
                search_result[5],
                search_result[6],
                search_result[7],
                max_students,
                []
                )

    def __repr__(self):
        return f"ID: {self.id}, title: {self.title}, department: {self.department}, time: {self.time}, days: {self.days}, semester: {self.semester}, year: {self.year}, credits: {self.credits}, max_students: {self.max_students}"

    def __eq__(self, other):
        return self.id == other.id

    def add_student(self, student):
        if len(self.students) < self.max_students:
            self.students.append(student)

            #dbcursor.execute(f"UPDATE COURSES SET STUDENTS = (STUDENTS || ', {student.WIT_ID}') WHERE ID = '{self.id}'")
            #database.commit()

            return True
        return False

    def remove_student(self, student):
        self.students.remove(student)

        #dbcursor.execute(f"SELECT STUDENTS FROM COURSES WHERE ID = \'{self.id}\'")
        #students_string = dbcursor.fetchone()[0]

        #students_string = students_string.replace(f", {student.id}", "")

        #dbcursor.execute(f"UPDATE COURSES SET STUDENTS = \'{students_string}\' WHERE ID = \'{self.id}\'")
        #database.commit()

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
                self.courses.append(search_courses("ID", course_id[0])[0])

    def __repr__(self):
        return f"{self.surname}, {self.name} - {self.WIT_ID} (student)"

    def time_conflict(self):
        # Check if courses enrolled have time conflicts in schedule
        courses = self.courses
        
        days = ["M", "T", "W", "R", "F"]

        for i in range (0, len(courses)):
            for j in range (0, len(courses)):

                if (i != j): 
                    for day in days:
                        if (day in courses(i).days and day in courses(j).days):
                            start_time1 = int(courses(i).time[0:4:1].replace(":", ""))
                            end_time1 = int(courses(i).time[6:10:1].replace(":", ""))
                            start_time2 = int(courses(j).time[0:4:1].replace(":", ""))
                            end_time2 = int(courses(j).time[6:10:1].replace(":", ""))

                            if (end_time1 > start_time2 and end_time2 > start_time1):
                                print("There is a time conflict with " + courses(i).ID + " and " + courses(j).ID)
                                return (True)
                            else:
                                return (False)

    # Quang and Alexander Puttre
    def add_course(self, course):
        # Check if the course is already enrolled
        if course in self.courses:
            print("You are already enrolled in this course.")
        else:
            # Check if the course has available slots
            if len(course.students) < course.max_students:
                print(course.id)

                self.courses.append(course)

                if self.time_conflict() :
                    self.courses.remove(course)

                else: 

                    dbcursor.execute(f"UPDATE STUDENT SET COURSES = (COURSES || ', {course.id}') WHERE EMAIL = '{self.email}'")
                    database.commit()

                    course.add_student(self)

                    print("Added course:", course.title)

            else:
                print("Course is full. Unable to enroll.")

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

            dbcursor.execute(f"SELECT COURSES FROM STUDENT WHERE EMAIL = \'{self.email}\'")
            courses_string = dbcursor.fetchone()[0]

            courses_string = courses_string.replace(f", {course.id}", "")

            dbcursor.execute(f"UPDATE STUDENT SET COURSES = \'{courses_string}\' WHERE EMAIL = \'{self.email}\'")
            database.commit()

            print(f"{course.id} has been removed from your schedule.\n")
        else:
            print(f"{course.id} is not in your schedule.\n")

    def from_search_result(search_result: tuple, max_students = 30):

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
    def __init__(self, WIT_ID, name, surname, title, hireyear, dept, email, courses = []):
        self.WIT_ID = WIT_ID
        self.name = name
        self.surname = surname
        self.title = title
        self.hireyear = hireyear
        self.dept = dept 
        self.email = email
        self.courses = courses

        dbcursor.execute(f"SELECT COURSES FROM INSTRUCTOR WHERE ID = {WIT_ID}")
        course_string = dbcursor.fetchone()[0]
        dbcursor.execute(f"SELECT ID FROM COURSES")
        course_ids = dbcursor.fetchall()

        for course_id in course_ids:
            if course_id[0] in course_string:
                self.courses.append(search_courses("ID", course_id[0])[0])

    def __repr__(self):
        return f"{self.surname}, {self.name} - {self.WIT_ID} ({self.title})"
       
    def from_search_result(search_result: tuple):
        courses = []

        course_string = search_result[7]
        dbcursor.execute(f"SELECT ID FROM COURSES")
        course_ids = dbcursor.fetchall()

        for course_id in course_ids:
            if course_id[0] in course_string:
                courses.append(search_courses("ID", course_id[0])[0])
        
        return Instructor(
            search_result[0],
            search_result[1],
            search_result[2],
            search_result[3],
            search_result[4],
            search_result[5],
            search_result[6],
            courses
        )

    def add_course(self, course):
        self.courses.append(course)

        dbcursor.execute(f"UPDATE INSTRUCTOR SET COURSES = (COURSES || ', {course.id}') WHERE EMAIL = '{self.email}'")
        database.commit()

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

            dbcursor.execute(f"SELECT COURSES FROM INSTRUCTOR WHERE EMAIL = \'{self.email}\'")
            courses_string = dbcursor.fetchone()[0]

            courses_string = courses_string.replace(f", {course.id}", "")

            dbcursor.execute(f"UPDATE INSTRUCTOR SET COURSES = \'{courses_string}\' WHERE EMAIL = \'{self.email}\'")
            database.commit()

            print(f"{course.id} has been removed from your schedule.\n")
        else:
            print(f"{course.id} is not in your schedule.\n")

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

            dbcursor.execute(f"SELECT COURSES FROM INSTRUCTOR WHERE EMAIL = \'{self.email}\'")
            courses_string = dbcursor.fetchone()[0]

            courses_string = courses_string.replace(f", {course.id}", "")

            dbcursor.execute(f"UPDATE INSTRUCTOR SET COURSES = \'{courses_string}\' WHERE EMAIL = \'{self.email}\'")
            database.commit()

            print(f"{course.id} has been removed from your schedule.\n")
        else:
            print(f"{course.id} is not in your schedule.\n")

    def print_courses(self):
        if (len(self.courses) > 0):
            print("Prof.", self.surname)
            display_courses(self.course_list)
        else:
            print("Your course roster is empty\n")

class Admin(User):
    # The super() function allows the methods & attributes of the parent class.
    def __init__(self, WIT_ID, name, surname, title, office, email):
        self.WIT_ID = WIT_ID
        self.name = name
        self.surname = surname
        self.title = title
        self.office = office
        self.email = email

    def add_course(self, course):
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
    def add_student(self, student):
        dbcursor.execute(f"""INSERT INTO STUDENT VALUES(
            "{student.WIT_ID}",
            "{student.name}",
            "{student.surname}",
            "{student.gradyear}",
            "{student.major}",
            "{student.email}",
            "",
            "{student.name}"
        """)

    def add_instructor(self, instructor):
        dbcursor.execute(f"""INSERT INTO INSTRUCTOR VALUES(
            "{instructor.WIT_ID}",
            "{instructor.name}",
            "{instructor.surname}",
            "{instructor.title}",
            "{instructor.hireyear}",
            "{instructor.dept}",
            "{instructor.email}",
            "",
            "{instructor.name}"
        """)

    def add_admin(self, admin):
        dbcursor.execute(f"""INSERT INTO ADMIN VALUES(
            "{admin.WIT_ID}",
            "{admin.name}",
            "{admin.surname}",
            "{admin.title}",
            "{admin.office}",
            "{admin.email}",
            "{admin.password}"
        """)

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

def search_instructors(search_criterion: str, value: str) -> list:
    dbcursor = database.cursor()

    search_criterion = search_criterion.upper()

    query = ""

    match search_criterion:
        case "ID":
            query = f"SELECT * FROM INSTRUCTOR WHERE {search_criterion} = \'{value}\'"
        case "NAME":
            query = f"SELECT * FROM INSTRUCTOR WHERE {search_criterion} = \'{value}\'"
        case "SURNAME":
            query = f"SELECT * FROM INSTRUCTOR WHERE {search_criterion} = \'{value}\'"
        case "TITLE":
            query = f"SELECT * FROM INSTRUCTOR WHERE {search_criterion} = \'{value}\'"
        case "HIREYEAR":
            query = f"SELECT * FROM INSTRUCTOR WHERE {search_criterion} = \'{value}\'"
        case "DEPT":
            query = f"SELECT * FROM INSTRUCTOR WHERE {search_criterion} = \'{value}\'"
        case "EMAIL":
            query = f"SELECT * FROM INSTRUCTOR WHERE {search_criterion} = \'{value}\'"
        case "COURSES":
            query = f"SELECT * FROM INSTRUCTOR WHERE {search_criterion} = {value}"
        case _:
            raise Exception("Invalid search criterion")

    dbcursor.execute(query)
    result = dbcursor.fetchall()

    search_matches = []

    for i in result:
        search_matches.append(Instructor.from_search_result(i))

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

                    if user_input1 == 2:
                        user_input2 = input("Enter the id of the course to remove: ")
                        user.remove_course(search_courses("id", user_input2)[0])

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
                admin_choice = int(input("\n1- Log out\n2- Search all courses\n3- Add / Remove courses from the system\n4- Display all courses\n5- Add / remove users from the system\n6- Link / unlink a user from a course\n\n"))
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
                elif admin_choice == 5:
                    admin_choice = int(input("\n1- Add a user\n2- Remove a user\n\n")) 

                    if admin_choice == 1:
                        admin_choice = int(input("\n1- Add an admin\n2- Add an instructor\n3- Add a student\n\n"))
                        if admin_choice == 1:
                            new_user = Admin(
                                int(input("Enter the user's ID: ")),
                                str(input("Enter the user's name: ")),
                                str(input("nnter the user's surname: ")),
                                str(input("Enter the user's title: ")),
                                str(input("Enter the user's office: ")),
                                str(input("Enter the user's email: ")),
                            )

                            dbcursor.execute(f"INSERT INTO ADMIN VALUES (\'{new_user.WIT_ID}\', \'{new_user.name}\', \'{new_user.surname}\', \'{new_user.title}\', \'{new_user.office}\', \'{new_user.email}\', \'{new_user.name}\')")
                            database.commit()

                        elif admin_choice == 2:
                            new_user_id = int(input("Enter the user's ID: "))
                            new_user_name = str(input("Enter the user's name: "))
                            new_user_surname = str(input("nnter the user's surname: "))
                            new_user_title = str(input("Enter the user's title: "))
                            new_user_hireyear = int(input("Enter the user's hire year: "))
                            new_user_dept = str(input("Enter the user's department: "))
                            new_user_email = str(input("Enter the user's email: "))

                            dbcursor.execute(f"INSERT INTO INSTRUCTOR VALUES (\'{new_user_id}\', \'{new_user_name}\', \'{new_user_surname}\', \'{new_user_title}\', \'{new_user_hireyear}\', \'{new_user_dept}\', \'{new_user_email}\', \'\', \'{new_user_name}\')")
                            database.commit()

                        elif admin_choice == 3:
                            new_user_id = int(input("Enter the user's ID: "))
                            new_user_name = str(input("Enter the user's name: "))
                            new_user_surname = str(input("nnter the user's surname: "))
                            new_user_gradyear = int(input("Enter the user's graduation year: "))
                            new_user_major = str(input("Enter the user's major: "))
                            new_user_email = str(input("Enter the user's email: "))

                            dbcursor.execute(f"INSERT INTO STUDENT VALUES (\'{new_user_id}\', \'{new_user_name}\', \'{new_user_surname}\', \'{new_user_gradyear}\', \'{new_user_major}\', \'{new_user_email}\', \'\', \'{new_user_name}\')")
                            database.commit()

                    elif admin_choice == 2:
                        admin_choice = str(input("Enter the id of the user to remove: "))

                        dbcursor.execute(f"DELETE FROM ADMIN WHERE ID = {admin_choice}")
                        dbcursor.execute(f"DELETE FROM STUDENT WHERE ID = {admin_choice}")
                        dbcursor.execute(f"DELETE FROM INSTRUCTOR WHERE ID = {admin_choice}")
                        database.commit()
                elif admin_choice == 6:
                    admin_choice = int(input("\n1- Link a course\n2- Unlink a course\n"))
                    if admin_choice == 1:
                        admin_choice = str(input("\nEnter the ID of the instructor or student: "))
                        selected_user = None
                        search_result = search_students("id", admin_choice)

                        if len(search_result) == 0:
                            search_result = search_instructors("id", admin_choice)
                        if len(search_result) == 0:
                            print("\nThat user is not in the database.\n")
                        else:
                            selected_user = search_result[0]
                            print(selected_user)
                            display_courses(selected_user.courses)
                            admin_choice = str(input("\nEnter the ID of the course to add: "))
                            search_result = search_courses("id", admin_choice)
                            if len(search_result) > 0:
                                course = search_result[0]
                                selected_user.add_course(course)
                            else:
                                print("\nThat course is not in the database.\n")
                    elif admin_choice == 2:
                        admin_choice = str(input("\nEnter the ID of the instructor or student: "))
                        selected_user = None
                        search_result = search_students("id", admin_choice)

                        if len(search_result) == 0:
                            search_result = search_instructors("id", admin_choice)
                        if len(search_result) == 0:
                            print("\nThat user is not in the database.\n")
                        else:
                            selected_user = search_result[0]
                            print(selected_user)
                            display_courses(selected_user.courses)
                            admin_choice = str(input("\nEnter the ID of the course to remove: "))
                            search_result = search_courses("id", admin_choice)
                            if len(search_result) > 0:
                                course = search_result[0]
                                selected_user.remove_course(course)
                            else:
                                print("\nThat course is not in the database.\n")
                else:
                    print("Please choose from one of the displayed options\n")
        elif user_type == "instructor":
            print("---------Instructor Options---------\n\n")

            user = search_instructors("email", username)[0]

            while user_type != "":
                print("Choose one of the following options:\n")
                instructor_choice = int(input("\n1- Exit\n2- Search all courses\n3- Add / Remove a course\n4- Assemble and print course roster\n5- Display your schedule\n6- Display all courses\n\n"))
                if instructor_choice == 1:
                    print(f"Goodbye {username}!\n")
                    user_type = ""
                elif instructor_choice == 2:
                    search_courses_menu()
                elif instructor_choice == 4:
                        courses = user.courses
                        display_courses(user.courses)
                        user_input = str(input("Enter the id of the course to print the roster for: "))
                        print()

                        found_course = False
                        for c in courses:
                            if c.id == user_input:
                                found_course = True

                                dbcursor.execute("SELECT * FROM STUDENT")
                                search_results = dbcursor.fetchall()

                                for result in search_results:
                                    if c.id in result[6]:
                                        print(Student.from_search_result(result))

                        if (not found_course):
                            print("You are not scheduled to teach that course.\n")

                elif instructor_choice == 3:
                    user_input = int(input("\n1- Add a course\n2- Remove a course\n\n"))

                    match user_input:
                        case 1:
                            display_courses()
                            user_input = str(input("Enter the id of the course to add: "))
                            to_add = search_courses("id", user_input)
                            if len(to_add) > 0:
                                user.add_course(to_add[0])
                            else:
                                print(f"No course with id {user_input} found in database\n")
                        case 2:
                            for c in user.courses:
                                print(c)

                            user_input = str(input("Enter the id of the course to remove: "))

                            found_course = False
                            for c in user.courses:
                                if c.id == user_input:
                                    found_course = True
                                    user.remove_course(c)

                            if not found_course:
                                print("You are not scheduled to teach the course.\n")

                        case _:
                            pass
                elif instructor_choice == 5:
                    display_courses(user.courses)
                elif instructor_choice == 6:
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
