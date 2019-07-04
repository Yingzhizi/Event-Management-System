import sqlite3
import database.update_table as dbUpdater

def insert_data(sql, values):
    with sqlite3.connect("EMS.db") as db:
        cursor = db.cursor()
        cursor.execute(sql, values)
        db.commit()

def insert_User(data):
    sql = "INSERT OR IGNORE INTO User (Name, zID, Email, Password, Role)  VALUES (?, ?, ?, ?, ?)"
    insert_data(sql, data)

def insert_Course(data):
    sql = "INSERT OR IGNORE INTO Course (CourseID, Status, Name, Convenor, Details, Deregister_Period, Capacity, noAttendees, Venue, Date_Start, Date_End, Early_Bird, Register_Fee)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    insert_data(sql, data)

def insert_Seminar(data):
    sql = "INSERT OR IGNORE INTO Seminar (SeminarID, Status, Name, Convenor, Details, Deregister_Period, Venue, Date_Start, Date_End, Early_Bird, Register_Fee, Capacity, noAttendees)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    insert_data(sql, data)

def insert_Session(data):
    sql = "INSERT OR IGNORE INTO Session (SessionID, Topic, Presenter, Details, Capacity, noAttendees, SeminarID, Status)  VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    insert_data(sql, data)

def insert_User_Course(event, data):
    sql = "INSERT OR IGNORE INTO User_Course (Email, CourseID, Status)  VALUES (?, ?, ?)"
    insert_data(sql, data)
    dbUpdater.increment_table('Course', 'noAttendees', 'CourseID', (1,event.event_id))

def insert_User_Seminar(data):
    sql = "INSERT OR IGNORE INTO User_Seminar (Email, SeminarID, Status)  VALUES (?, ?, ?)"
    insert_data(sql, data)

def insert_User_Session(event, data):
    sql = "INSERT OR IGNORE INTO User_Session (Email, SessionID, SeminarID, Status)  VALUES (?, ?, ?, ?)"
    insert_data(sql, data)
    dbUpdater.increment_table('Session', 'noAttendees', 'SessionID', (1,event.SessionID))
    dbUpdater.increment_table('Seminar', 'noAttendees', 'SeminarID', (1,event.SeminarID))
