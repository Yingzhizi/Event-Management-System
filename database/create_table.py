import sqlite3

def create_table(example, table_name, sql):
    with sqlite3.connect('EMS.db') as db:
        cursor = db.cursor() #navigate around database
        cursor.execute("select name from sqlite_master where name=?", (table_name,))
        # check if product tble already exists,
        #expects a tuple to be passed
        result = cursor.fetchall()
        keep_table = True
        if len(result) == 1: # table is present
            response = input("The table {0} already exists, do you wish to recreate it (y/n): ".format(table_name))
            if response == "y":
                keep_table = False
                print("The table {0} table will be recreated - all existing data will be lost.".format(table_name))
                cursor.execute("drop table if exists {0}".format(table_name))
                db.commit()
            else:
                print("The existing table was kept")
        else:
            keep_table = False
        if not keep_table:
            cursor.execute(sql)  #what actually runs the sql statment
            db.commit()          #changes that are made are saved

def create_user_table(db_name):
    sql = """CREATE TABLE User(
             Name text,
             zID integer,
             Email text Primary Key,
             Password text,
             Role text)""" #cascade or set null
             #can zID be NULL?
    create_table(db_name, "User", sql)

def create_course_table(db_name):
    sql = """CREATE TABLE Course(
             CourseID integer Primary Key,
             Status integer,
             Name text,
             Convenor integer,
             Details text,
             Deregister_Period integer,
             Capacity integer,
             noAttendees integer,
             Venue text,
             Date_Start text,
             Date_End text,
             Early_Bird text,
             Register_Fee text)"""
    create_table(db_name, "Course", sql)

def create_seminar_table(db_name):
    sql = """CREATE TABLE Seminar(
             SeminarID integer Primary Key,
             Status integer,
             Name text,
             Convenor integer,
             Details text,
             Deregister_Period integer,
             Venue text,
             Date_Start text,
             Date_End text,
             Early_Bird text,
             Register_Fee integer,
             Capacity integer,
             noAttendees integer)"""
    create_table(db_name, "Seminar", sql)

def create_session_table(db_name):
    sql = """CREATE TABLE Session(
             SessionID integer Primary Key,
             Topic text,
             Presenter text,
             Details text,
             Capacity integer,
             noAttendees integer,
             SeminarID integer,
             Status integer,
             Foreign Key(SeminarID) references Seminar(SeminarID)
             on update restrict on delete restrict)"""
    create_table(db_name, "Session", sql)

def create_user_course_table(db_name):
    sql = """CREATE TABLE User_Course(
             Email text,
             CourseID integer,
             Status integer,
             Primary Key(Email, CourseID)
             Foreign Key(Email) references User(Email)
             Foreign Key(CourseID) references Course(CourseID)
             Foreign Key(Status) references Course(Status)
             on update cascade on delete cascade)"""
    create_table(db_name, "User_Course", sql)

def create_user_seminar_table(db_name):
    sql = """CREATE TABLE User_Seminar(
             Email text,
             SeminarID integer,
             Status integer,
             Primary Key(Email, SeminarID)
             Foreign Key(Email) references User(Email)
             Foreign Key(SeminarID) references Seminar(SeminarID)
             Foreign Key(Status) references Seminar(Status)
             on update cascade on delete cascade)"""
    create_table(db_name, "User_Seminar", sql)

def create_user_session_table(db_name):
    sql = """CREATE TABLE User_Session(
             Email integer,
             SessionID integer,
             SeminarID integer,
             Status integer,
             Primary Key(Email, SessionID, SeminarID)
             Foreign Key(Email) references User(Email)
             Foreign Key(SessionID) references Session(SessionID)
             Foreign Key(SeminarID) references Seminar(SeminarID)
             Foreign Key(Status) references Seminar(Status)
             on update cascade on delete cascade)"""
    create_table(db_name, "User_Session", sql)
