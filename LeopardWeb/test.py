import unittest
import sqlite3
from LeopardWeb import Admin
from LeopardWeb import Instructor
from LeopardWeb import Course
from LeopardWeb import check_database
from Database import fetch_course


class TestAdminAddRemoveCourse(unittest.TestCase):

    def setUp(self):
        db = sqlite3.connect("assignment3.db")
        dbcursor = db.cursor()

        dbcursor.execute("DELETE FROM COURSES WHERE ID = 'id'")

        db.commit()
        db.close()

        self.test_admin = Admin("first_name", "last_name", 0)
        self.test_course = Course("id", "title", "department", "time", "days", "semester", 2023, 4, 25)

        # self.db = sqlite3.connect("assignment3.db")
        # self.dbcursor = self.db.cursor()

    def tearDown(self):
        pass
        # self.dbcursor.execute("DELETE FROM COURSES WHERE ID = 'id'")
        # self.db.commit()
        # self.db.close()

    def test_add_course(self):
        self.test_admin.add_course(self.test_course)

        db = sqlite3.connect("assignment3.db")
        dbcursor = db.cursor()

        search_result = fetch_course(dbcursor, "id")

        assert len(search_result) == 1, f"Search result has incorrect length: {len(search_result)}"

        course = Course.from_search_result(search_result[0], self.test_course.max_students)

        assert course.id == self.test_course.id, f"Course from table has incorrect ID: {course.id}"
        assert course.title == self.test_course.title, f"Course from table has incorrect title: {course.title}"
        assert course.department == self.test_course.department, f"Course from table has incorrect department: {course.department}"
        assert course.time == self.test_course.time, f"Course from table has incorrect time: {course.time}"
        assert course.days == self.test_course.days, f"Course from table has incorrect days: {course.days}"
        assert course.semester == self.test_course.semester, f"Course from table has incorrect semester: {course.semester}"
        assert course.year == self.test_course.year, f"Course from table has incorrect year: {course.year}"
        assert course.credits == self.test_course.credits, f"Course from table has incorrect credits: {course.credits}"
        assert course.max_students == self.test_course.max_students, f"Course from table has incorrect max_students: {course.max_students}"

        dbcursor.execute("DELETE FROM COURSES WHERE ID = 'id'")

        db.commit()
        db.close()

    def test_remove_course(self):
        self.test_admin.add_course(self.test_course)
        self.test_admin.remove_course(self.test_course)

        db = sqlite3.connect("assignment3.db")
        dbcursor = db.cursor()

        search_result = fetch_course(dbcursor, "id")

        assert len(search_result) == 0, "Course not removed from table"

        db.commit()
        db.close()

if __name__ == '__main__':
    unittest.main()

"""

class TestInstructorSearchUser(unittest.TestCase):

    def setUp(self):
        db = sqlite3.connect("assignment3.db")
        dbcursor = db.cursor()

        dbcursor.execute("SELECT * FROM ADMIN WHERE email = \'{email}\' AND ID = \'{id}'")
        dbcursor.execute("SELECT * FROM STUDENT WHERE email = \'{email}\' AND ID = \'{id}'")
        dbcursor.execute("SELECT * FROM INSTRUCTOR WHERE email = \'{email}\' AND ID = \'{id}'")

        db.commit()
        db.close()

        self.test_instructor = Instructor("first_name", "last_name", 0)
        self.test_student = Student("first_name", "last_name", 0)
        self.test_admin = Admin("first_name", "last_name", 0)

    def tearDown(self):
        pass

    def test_checkdatabase(self):
        self.test_instructor.check_database(self.test_instructor)
        self.test_student.check_database(self.test_student)
        self.test_admin.check_database(self.test_admin)

        db = sqlite3.connect("assignment3.db")
        dbcursor = db.cursor()

        search_result = fetch_course(dbcursor, "id")

        assert len(search_result) == 1, f"Search result has incorrect length: {len(search_result)}"

        course = Course.from_search_result(search_result[0], self.test_course.max_students)

        check_database("hamiltonm", 30001)
        check_database("turinga", 20004)
        check_database("habchiy", 10011)


        db.commit()
        db.close()

    """
