#test commit

import Database

class CourseCatalog:
    def __init__(self, dbcursor):
        self.dbcursor = dbcursor

    def add_course(self, course):
        self.dbcursor

    def remove_course(self, course):
        self.courses.remove(course)

    def get_courses(self):
        return self.courses

    def search_courses(self, query):
        pass

    def __db_insert_course(self, course):
        self.dbcursor.execute(
        f"""
        INSERT INTO COURSES VALUES(
            '{course.id}',
            '{course.title}',
            '{course.department}',
            '{course.time}',
            '{course.days}',
            '{course.semester}',
            '{course.year}',
            '{course.credits}
        );
        """
        )

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

    def search_courses(self):
        print("Searching my courses...")


class Course():
    class Section():
        def __init__(self, num, capacity):
            self.students = []
            self.num = num
            self.capacity = capacity

        def add_student(self, student):
            if self.students.count() <= self.capacity:
                self.students.append(student)
                return True
            else:
                return False

        def remove_student(self, student):
            self.students.remove(student)

    sections = [Section]

    def __init__(self, id, title, department, time, days, semester, year, credits):
        self.id = id
        self.title = title
        self.department = department
        self.time = time
        self.days = days
        self.semester = semester
        self.year = year
        self.credits = credits

    def add_section(self, capacity):
        section_num = self.sections.count()
        self.sections.append(self.Section(section_num, capacity))
        return section_num

    def get_sections(self):
        section_nums = []
        for s in self.sections:
            section_nums.append(s.num)
        return section_nums

    def add_student(self, student, section=0):
        if section in self.get_sections():
            self.sections[section].add_student(student)

    def remove_student(self, student, section=0):
        if student in self.sections[section]:
            self.sections[section].remove_student(student)

class Instructor(User):
    def __init__(self, first_name, last_name):
        super().__init__(self, first_name, last_name)
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
instructor1 = Instructor("Marisha", "Rawlins")

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
