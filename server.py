from flask import Flask
from flask_login import LoginManager
from model.EMS import EMS
from model.User import User
from model.Course import Course
import database.create_table as dbCreator
import database.insert_table as dbInserter
import database.delete_table as dbDeleter

def valid_time(time):
    return time > 0

app = Flask(__name__)

system = EMS()
#store tmp seminar before actually create a course
seminar = None


db_name = "EMS.db"
dbCreator.create_user_table(db_name)
dbCreator.create_course_table(db_name)
dbCreator.create_seminar_table(db_name)
dbCreator.create_session_table(db_name)
dbCreator.create_user_course_table(db_name)
dbCreator.create_user_seminar_table(db_name)
dbCreator.create_user_session_table(db_name)

course = (1,1,'t',4119988,'t','2018-12-10 22:00:00',100,0,'t','2019-01-01 22:00:00','2019-01-30 22:00:00','2018-12-01 22:00:00',100)
dbInserter.insert_Course(course)
course = (2,1,'s',4119989,'s','2018-12-10 22:00:00',1,0,'s','2019-01-01 22:00:00','2019-01-30 22:00:00','2018-12-01 22:00:00',100)
dbInserter.insert_Course(course)
seminar = (1,1,'Test Seminar',4119993,'Testing','2018-12-10 22:00:00','UNSW','2019-01-01 22:00:00','2019-01-30 22:00:00','2018-12-1 22:00:00',1,100,0)
dbInserter.insert_Seminar(seminar)
session = (1,'Hi','Tommy','Hi',50,0,1,1)
dbInserter.insert_Session(session)
session = (2,'Bye','Tommy','Bye',50,0,1,1)
dbInserter.insert_Session(session)

with open("user.csv", "r") as w:
    for i in range(0, 24):
        (name, zID, email, password, role) = w.readline().split(",")
        print ((name, zID, email, password, role.rstrip('\n')))
        user = (name, zID, email, password, role.rstrip('\n'))
        dbInserter.insert_User(user)

import routes
