from model.User import User
from model.Event import Event
from model.Course import Course
from model.Seminar import Seminar
from model.Session import Session
from model.Guest_User import Guest_User
import database.select_table as dbHandler
import database.insert_table as dbInserter
import database.delete_table as dbDeleter
import database.update_table as dbUpdater
from datetime import datetime

#didnt have time to clean the exceptions up and put them in another file
class postError(Exception):
    """Base class for exceptions in this module."""
    pass
class startDateError(postError):
    def __init__(self, msg):
        self.msg = msg

class EarlyBirdError(postError):
    def __init__(self, msg):
        self.msg = msg

class periodError(postError):
    def __init__(self, period, msg):
        self.period = period
        self.msg = msg

class deregisterError(postError):
    def __init__(self, period, msg):
        self.period = period
        self.msg = msg

class capacityError(postError):
    def __init__(self, msg):
        self.msg = msg

class invalidCreator(postError):
    def __init__(self, msg):
        self.msg = msg

class invalidFee(postError):
    def __init__(self, msg):
        self.msg = msg

class register_error(Exception):
    pass

class decommisioned_event(register_error):
    def __init__(self, msg):
        self.msg = msg

class invalid_attendant(register_error):
    def __init__(self, msg):
        self.msg = msg

class active_event(register_error):
    def __init__(self, msg):
        self.msg = msg

class EMS():
    def __init__(self):
        self._tmpSeminar = None

    @property
    def tmpSeminar(self):
        return self._tmpSeminar
    @tmpSeminar.setter
    def tmpSeminar(self, seminar):
        self._tmpSeminar = seminar

    def get_event(self, event_type, event_id):
        event = dbHandler.select_product(event_type, "{0}ID".format(event_type), event_id)
        requestedEvent = self.converter(event_type, event)
        return requestedEvent

    def converter (self, event_type, row):
        if event_type == 'Course':
            event = Course(row[0], row[1], row[2], row[3], row[4], row[5],\
            row[6], row[7], row[8], row[9], row[10], row[11], row[12])
        elif event_type == 'Seminar':
            event = Seminar(row[0], row[1], row[2], row[3], row[4], row[5],\
            row[6], row[7], row[8], row[9], row[10])
        else:
            event = Session(row[0], row[1], row[2], row[3], row[4], row[5], row[6],\
            row[7])
        return event

    def events_list (self, event_type):
        """
        Produces a list of all events regradless of the status
        Input: event_type(string)
        Output: List(event)
        """
        events = dbHandler.select_all_products(event_type)
        eventList = []
        for event in events:
            eventList.append(self.converter(event_type, event))
        return eventList

    def open_events_list(self, event_type):
        """
        Produces a list of only open events for the public user(not authenticated)
        on homepage
        Also does an automatic check to close an event after its end date
        Input: event_type(string)
        Output: List(event)
        """
        openEventList = []
        for event in self.events_list(event_type):
            if event.status == 1:
                check = self.automatic_close(event_type, event)
                if check.status == 1:
                    openEventList.append(check)
        return openEventList

    def sessionList(self, SeminarID):
        """
        Compile rows of sessions with matching SeminarID
        into a list of session objects
        Input: SeminarID(string)
        Output: List(sessions)
        """
        sessions = dbHandler.select_products('Session', 'SeminarID', SeminarID)
        sessionList = []
        for session in sessions:
            sessionList.append(self.converter('Session', session))
        return sessionList

    def events_left (self, field, table_name, email):
        """
        Allows for the dynamic homepage which removes events that have been
        registered for
        Input: {field, table_name, email}-> string
        Output: list of events that are yet to be registered for
        """
        sql = "SELECT {0}ID FROM {1} WHERE Email=?".format(field, table_name)
        eventRego = dbHandler.select_column(sql, (email,))

        if eventRego == []:
            eventLeft = self.open_events_list(field)
            return eventLeft

        sql = "SELECT {0}ID FROM {0} WHERE Status=?".format(field)
        eventList = dbHandler.select_column(sql, (1,))

        events = [x for x in eventList if x not in eventRego]
        eventsLeft = []
        for event in events:
            add_event = self.get_event(field, event[0])
            eventsLeft.append(add_event)
        return eventsLeft

    def registrations(self, field, table_name, email, SeminarID):
        """
        Gets all events that have been registered for by a certain zID
        Input: {field, table_name, email, SeminarID}-> string, {SeminarID}-> in
        Output: list of events that have been registed for
        """
        if table_name == 'User_Session':
            sql = "SELECT {0}ID FROM {1} WHERE Email=? and SeminarID=?".format(field, table_name)
            sql = "SELECT {0}ID FROM {1} WHERE Email=?".format(field, table_name)
        else:
            sql = "SELECT {0}ID FROM {1} WHERE Email=?".format(field, table_name)
        receipts =  dbHandler.select_column(sql, (email,))

        registrations = []
        if receipts == None:
            return registrations
        for receipt in receipts:
            if table_name == 'User_Course':
                event = self.get_event('Course', receipt[0])
            elif table_name == 'User_Seminar':
                event = self.get_event('Seminar', receipt[0])
            else:
                event = self.get_event('Session', receipt[0])
            registrations.append(event)
        return registrations

    def sessionID(self, email):
        """
        A list of all SessionIDs that a user has registered for (requested by front end)
        Input: {email} -> string
        Output: list of ints
        """
        sessions = dbHandler.select_products('User_Session', 'Email', email)
        list = []
        for item in sessions:
            list.append(item[1])
        return list

    def add_user(self, name, zID, email, password, role):
        """
        Adds Users
        Input: {name, email, password, role}->string, {zID}->int
        Output: int
        """
        user_list = dbHandler.select_all_products('User')
        for user in user_list:
            if email in user:
                return 0
        user = (name, zID, email, password, role)
        dbInserter.insert_User(user)
        return 1

    def get_user(self, username):
        """
        Gets a user for verification allowing for verification by email or by zID
        if they have one
        Input: {username}->string
        Output: User else None
        """
        if '@' in username:
            userInfo = dbHandler.select_product("User", "Email", username)
            if userInfo is None:
                return None
            else:
                user = User(userInfo[0], userInfo[1], userInfo[2], userInfo[3], userInfo[4])
                return user
        else:
            userInfo = dbHandler.select_product("User", "zID", username)
            if userInfo is None:
                return None
            else:
                user = User(userInfo[0], userInfo[1], userInfo[2], userInfo[3], userInfo[4])
                return user

    def createCourse(self, user, name, detail, deregister, capacity, venue, start_date, end_date, early_bird, register_fee):
        """
        Creates a course entry in the database
        Input: {user}->user object, {name, detail, venue, deregister,
        start_date, end_date}->string, {capacity}->int
        Output: boolean value to confirm success or failure
        """
        if isinstance(start_date, str):
            date_format = "%Y-%m-%d %H:%M:%S"
            start_date = datetime.strptime(start_date, date_format)
            end_date = datetime.strptime(end_date, date_format)
            deregister = datetime.strptime(deregister, date_format)
            early_bird = datetime.strptime(Early_Bird, date_format)
        if capacity < 1:
            raise capacityError("The capacity must at least be 1.")
        elif datetime.now() > start_date:
            raise startDateError("The start date must before the current date.")
        elif early_bird > deregister:
            raise EarlyBirdError("The early bird period must be before the deregister period.")
        elif end_date < start_date:
            raise periodError(period, "The start date must before or equal to the end date.")
        elif start_date < deregister:
            raise deregisterError(d_period, "The deregister period cannot after the start date.")
        elif user.role != 'trainer':
            raise invalidCreator("Unauthorised Creator")
        elif register_fee < 0:
            raise invalidFee("Register fee must at least be 0.")
        else:
            courseList = dbHandler.select_all_products('Course')
            CourseID = len(courseList)+1
            for course in courseList:
                if user.zID in course and name in course and course[1] == 1:
                    return 0

            Status = 1
            noAttendees = 0
            data = (CourseID, Status, name, user.zID, detail, deregister, capacity, \
            noAttendees, venue, start_date, end_date, early_bird, register_fee)
            dbInserter.insert_Course(data)
            return 1

    def create_seminar(self, user, name, detail, deregister, venue, start_date, end_date, early_bird, register_fee):
        """
        Creates a seminar object stored in system temporarily
        Input: {user}->user object, {name, detail, venue, deregister,
        start_date, end_date}->string, {capacity}->int
        Output: boolean value confirm success or failure
        """
        if isinstance(start_date, str):
            date_format = "%Y-%m-%d %H:%M:%S"
            start_date = datetime.strptime(start_date, date_format)
            end_date = datetime.strptime(end_date, date_format)
            deregister = datetime.strptime(deregister, date_format)
            early_bird = datetime.strptime(early_bird, date_format)
        if datetime.now() > start_date:
            raise startDateError("The start date must before the current date.")
        elif early_bird > deregister:
            raise EarlyBirdError("The early bird period must be before the deregister period.")
        elif end_date < start_date:
            raise periodError(period, "The start date must br before or equal to the end date.")
        elif start_date < deregister < 0:
            raise deregisterError(d_period, "The deregister period cannot be after the start date.")
        elif user.role != 'trainer':
            raise invalidCreator("Unauthorised Creator")
        elif register_fee < 0:
            raise invalidFee("Register fee must at least be 0.")
        else:
            seminarList = dbHandler.select_all_products('Seminar')
            SeminarID = len(seminarList)+1
            for seminar in seminarList:
                if user.zID in seminar and name in seminar and seminar[1] == 1:
                    return 0
            Status = 1
            info = (SeminarID, Status, name, user.zID, detail, deregister, venue,\
            start_date, end_date, early_bird, register_fee)
            new_seminar = self.converter('Seminar', info)
            self.tmpSeminar = new_seminar
            return new_seminar

    def create_session(self, seminar, topic, detail, presenter, capacity):
        """
        Creates a session object stored in system temporarily
        Input: {seminar}->seminar object {topic, detail, presentar}->string
        Output: boolean value confirm success or failure
        """
        if capacity < 1:
            raise capacityError("The capacity must at least be 1.")

        SessionID = len(seminar.sessions)+1
        for session in seminar.sessions:
            if session.topic == topic and session.presenter == presenter:
                return 0
        noAttendees = 0
        status = 1
        info = (SessionID, topic, detail, presenter, capacity, noAttendees, seminar.event_id, 1)
        newSession = self.converter('Session', info)
        seminar.add_session(newSession)
        # return newSession
        return 1


    def add_seminar(self, seminar):
        """
        Creates a seminar entry in the database
        Input: {user}->user object, {name, detail, venue, deregister,
        start_date, end_date}->string, {capacity}->int
        Output: N/A
        """
        if len(seminar.sessions) < 2:
            return 0

        capacity = 0
        for session in seminar.sessions:
            capacity += session.capacity
        noAttendees = 0
        data = (seminar.event_id, seminar.status, seminar.name, seminar.convenor, seminar.detail, seminar.deregister,\
        seminar.venue, seminar.start_date, seminar.end_date, seminar.early_bird, seminar.register_fee, capacity, noAttendees)
        dbInserter.insert_Seminar(data)

        return 1

    def add_sessions(self, seminar):
        """
        Creates a session entry in the database
        Input: {seminar}->seminar object
        Output: N/A
        """
        SessionID = len(dbHandler.select_all_products('Session'))
        for session in seminar.sessions:
            SessionID += 1
            data = (SessionID, session.topic, session.presenter, session.detail,\
            session.capacity, session.noAttendees, seminar.event_id, session.status)
            dbInserter.insert_Session(data)
            self.update_attendees('register', session, "Session", session.presenter)
        return 1

    def update_status(self, event_type, event_id, action):
        """
        Updates status of an event, handling opening, closing and cancelling of events
        """
        dbUpdater.update_table(event_type, "Status", "{0}ID".format(event_type), (action, event_id))
        if event_type == 'Seminar':
            sessions = dbHandler.select_products('Session', 'SeminarID', event_id)
            for session in sessions:
                dbUpdater.update_table("Session", "Status", "SessionID", (action, session[0]))

    def automatic_close(self, event_type, event):
        """
        Checks for dates to close event after end_date
        Input: {event_type}-> string, {event}-> event objects
        Output: updated event object
        """
        date_format = "%Y-%m-%d %H:%M:%S"
        end_date = datetime.strptime(event.end_date, date_format)
        if datetime.now() > end_date:
            event.status = 0
            self.update_status(event_type, event.event_id, 0)
        return event

    def update_attendees(self, action, event, event_type, email):
        """
        Updates attendee list based on whether they are registering or not:
        Input: {action, event_type, email}-> string, {event}-> event object
        Output: Updated event (course or seminar)
        """
        date_format = "%Y-%m-%d %H:%M:%S"
        if event.status == 0:
            raise decommisioned_event("This event has been closed")
        elif event.status == -1:
            raise decommisioned_event("This event has been cancelled")
        else:
            e = event
            if event_type == "Session":
                e = self.get_event("Seminar", event.SeminarID)

            if email == e.convenor:
                raise invalid_attendant("You are the convenor for this course")

            if datetime.strptime(e.start_date, date_format) < datetime.now() and\
            datetime.strptime(e.end_date, date_format) > datetime.now():
                raise active_event("This event is currently active")

        if action == 'register':
            if event.noAttendees < event.capacity and event_type != "Seminar":
                if event_type == 'Course':
                    dbInserter.insert_User_Course(event, (email, event.event_id, event.status))
                else:
                    dbInserter.insert_User_Session(event, (email, event.SessionID, event.SeminarID, event.status))
                    dbInserter.insert_User_Seminar((email, event.SeminarID, event.status))
            else:
                return 0
        else:
            if event.noAttendees > 0:
                if event_type == 'Course' and event_type != "Seminar":
                    dbDeleter.delete_user_course(event, (email, event.event_id))
                else:
                    dbDeleter.delete_user_session(event, (email, event.SessionID))
                    sql = "SELECT SessionID FROM User_Session WHERE Email=? and SeminarID=?"
                    if dbHandler.select_column(sql, (email, event.SeminarID)) == []:
                        dbDeleter.delete_user_seminar((email, event.SeminarID))
            else:
                return 0

        if event_type == 'Course':
            return self.get_event('Course', event.event_id)
        else:
            return self.get_event('Seminar', event.SeminarID)

    def get_attendees(self, event_type, event_id):
        """
        Produces a list of attendees for a particular event
        Input: {event_type}-> string, {event_id}-> int
        Output: list of atttendees
        """
        sql = "SELECT Email FROM User_{0} WHERE {0}ID=?".format(event_type)
        attendees = dbHandler.select_column(sql, (event_id,))
        attendees_list = []
        for attendee in attendees:
            attendees_list.append(self.get_user(attendee[0]))
        return attendees_list

    def registration_rules(self, user, event):
        """
        Input: {user}-> user object, {event}-> object
        Output: integer fee
        """
        if (user.role == 'guest'):
            if datetime.now().strftime("%Y-%m-%dT%H:%M") < event.early_bird:
                fee = int(event.register_fee) * 0.5
            else:
                fee = event.register_fee
        else:
            fee = 0
        return fee
