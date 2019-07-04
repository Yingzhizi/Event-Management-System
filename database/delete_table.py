import sqlite3
import database.update_table as dbUpdater

def delete_data(table_name, ID, data):
    with sqlite3.connect("EMS.db") as db:
        cursor =db.cursor()
        sql = "DELETE from {0} where {0}=?".format(table_name, ID)
        cursor.execute(sql, data)
        db.commit()

def delete_user_course(event, data):
    with sqlite3.connect("EMS.db") as db:
        cursor =db.cursor()
        sql = "DELETE from User_Course where Email=? and CourseID=?"
        cursor.execute(sql, data)
        db.commit()
        dbUpdater.reduce_table('Course', 'noAttendees', 'CourseID', (1,event.event_id))

def delete_user_seminar(data):
    with sqlite3.connect("EMS.db") as db:
        cursor =db.cursor()
        sql = "DELETE from User_Seminar where Email=? and SeminarID=?"
        cursor.execute(sql, data)
        db.commit()

def delete_user_session(event, data):
    with sqlite3.connect("EMS.db") as db:
        cursor =db.cursor()
        sql = "DELETE from User_Session where Email=? and SessionID=?"
        cursor.execute(sql, data)
        db.commit()
        dbUpdater.reduce_table('Session', 'noAttendees', 'SessionID', (1,event.SessionID))
        dbUpdater.reduce_table('Seminar', 'noAttendees', 'SeminarID', (1,event.SeminarID))
