import sqlite3

def init_db():
    db = sqlite3.connect("LeopardWeb.db")
    dbcursor = db.cursor()

    dbcursor.execute(
        """
        DROP TABLE IF EXISTS COURSES
        """
    )

    dbcursor.execute(
        """
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
        """
    )

    return dbcursor
