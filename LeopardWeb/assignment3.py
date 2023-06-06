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

print("\nAdmins:")
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

print("\nCourse Instructors")
cursor.execute("""
SELECT INSTRUCTOR.SURNAME, COURSES.ID
FROM INSTRUCTOR, COURSES
WHERE INSTRUCTOR.DEPT = COURSES.DEPARTMENT
""")

query_result = cursor.fetchall()

for i in query_result:
    print(i)

database.commit()
database.close()
