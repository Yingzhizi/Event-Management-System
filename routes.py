from server import app, valid_time, system
from flask import Flask, render_template, request, session, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from datetime import datetime
from model.EMS import EMS
from model.User import User
from model.Event import Event
from model.Course import Course
from model.Seminar import Seminar
from model.Session import Session

#Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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
    def __init__(self, msg):
        self.msg = msg

class deregisterError(postError):
    def __init__(self, msg):
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


@app.route("/")
def index():
    return redirect(url_for('login'))


@app.route("/customer_register",  methods=['GET', 'POST'])
def customer_register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        success = system.add_user(name, None, email, password, 'guest')
        print(success)
        if success == 0:
            print("Signing up fail...")
            message="This email has been used, you cannot register again."
            return render_template('signup.html', message=message)
        else:
            user = system.get_user(email)
            if user == None or user.password != password:
                return render_template("login.html")
            else:
                print("Signing up...")
                login_user(user)
                return redirect(url_for('signup_success', name=user.name))
    else:
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = system.get_user(username)
        if user is None:
            return render_template('login.html', message = "User name doesn't exist.")
        elif user.password != password:
            return render_template('login.html', message = "Wrong password.")
        else:
            print("Logging in...")
            login_user(user)
            return redirect(url_for('home'))
    else:
        return render_template("login.html")

@login_manager.user_loader
def load_user(user_name):
    return system.get_user(user_name)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    current_user.authenticated = False
    return redirect(url_for('index'))

@app.route("/<name>/signup_successfully", methods=['GET'])
@login_required
def signup_success(name):
    return render_template('signup_confirm.html', name=name)


@app.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    courseList = system.events_list('Course')
    seminarList = system.events_list('Seminar')
    courseReceipts = system.registrations('Course', 'User_Course', current_user.email, None)
    seminarReceipts = system.registrations('Seminar', 'User_Seminar', current_user.email, None)
    return render_template("dashboard.html", courses=courseList, seminars=seminarList, \
    courseReceipts=courseReceipts, seminarReceipts=seminarReceipts)

@app.route("/home", methods=['GET'])
def home():
    if current_user.is_authenticated:
        courseList = system.events_left('Course', 'User_Course', current_user.email)
        seminarList = system.events_left('Seminar', 'User_Seminar', current_user.email)
    else:
        courseList = system.open_events_list('Course')
        seminarList = system.open_events_list('Seminar')
    return render_template("home.html", courses=courseList, seminars=seminarList)

@app.route("/<event_type>/<event_id>/<event_name>/detail", methods=["GET"])
def display_event(event_type, event_id, event_name):
    if request.method == 'GET':
        event = system.get_event(event_type, event_id)
        sessionList = []
        attendees_list = []
        registered_sessions=[]
        fee = 0
        if event_type == 'Seminar':
            sessionList = system.sessionList(event_id)
            attendees_list = system.get_attendees(event_type, event_id)
            if current_user.is_authenticated:
                registered_sessions = system.sessionID(current_user.email)
        else:
            attendees_list = system.get_attendees(event_type, event_id)
        ableToCancel = 0
        ableToRegister = 0
        ableToDeregister = 0
        earlyBird = 0
        if datetime.now().strftime("%Y-%m-%dT%H:%M") < event.start_date :
            ableToCancel = 1
            ableToRegister = 1
        if datetime.now().strftime("%Y-%m-%dT%H:%M") < event.deregister:
            ableToDeregister = 1

        #has early bird discount or not
        if current_user.is_authenticated:
            fee = system.registration_rules(current_user, event)
        return render_template("info.html", event_type=event_type, event=event,
        sessions=sessionList, attendees_list=attendees_list,
        ableToCancel=ableToCancel, ableToRegister=ableToRegister,
        ableToDeregister=ableToDeregister, fee=fee, registered_sessions=registered_sessions)

@app.route("/register/<event_type>/<event_id>", methods=["GET", "POST"])
@login_required
def register(event_type, event_id):
    if request.method == 'GET':
        try:
            event = system.get_event(event_type, event_id)
            updated_event = system.update_attendees('register', event, event_type, current_user.email)

            if event_type == 'Course':
                return redirect(url_for('display_event', event_type=event_type, event_id=event_id, event_name=updated_event.name))
            else:
                #get the correspoding seminar of each session
                seminar_id = event.SeminarID
                Seminar = system.get_event("Seminar", seminar_id)
                return redirect(url_for('display_event', event_type="Seminar", event_id=seminar_id, event_name=Seminar.name))
        except Exception:
            return render_template("dashboard.html", system=system)
    return render_template("home.html", system=system)


@app.route("/deregister/<event_type>/<event_id>", methods=["GET", "POST"])
@login_required
def deregister(event_type, event_id):
    if request.method == 'GET':
        event = system.get_event(event_type, event_id)
        updated_event = system.update_attendees('deregister', event, event_type, current_user.email)
        if event_type == 'Course':
            return redirect(url_for('display_event', event_type=event_type, event_id=event_id, event_name=updated_event.name))
        else:
            #get the correspoding seminar of each session
            seminar_id = event.SeminarID
            Seminar = system.get_event("Seminar", seminar_id)
            return redirect(url_for('display_event', event_type="Seminar", event_id=seminar_id, event_name=Seminar.name))
    return render_template("home.html", system=system)

@app.route("/course", methods=["GET", "POST"])
@login_required
def create_course():
    if request.method == "POST":
        try:
            name = request.form['name']
            detail = request.form['detail']
            capacity = int(request.form['capacity'])
            venue = request.form['venue']
            date_format = "%Y-%m-%dT%H:%M"
            deregister = datetime.strptime(request.form['deregister'], date_format)
            start_date = datetime.strptime(request.form['start_date'], date_format)
            end_date = datetime.strptime(request.form['end_date'], date_format)
            early_bird = datetime.strptime(request.form['early_bird'], date_format)
            fee = int(request.form['fee'])

            if capacity < 1:
                raise capacityError("The capacity must at least be 1.")
            elif datetime.now() > start_date:
                raise startDateError("The start date must be after the current date.")
            elif early_bird > deregister:
                raise EarlyBirdError("The early bird period must be before the deregister period.")
            elif end_date < start_date:
                raise periodError("The start date must before or equal to the end date.")
            elif start_date < deregister:
                raise deregisterError("The deregister period cannot be after the start date.")
            elif current_user.role != 'trainer':
                raise invalidCreator("Unauthorised Creator")
            elif fee < 0:
                raise invalidFee("Register fee must at least be 0.")
            else:
                success = system.createCourse(current_user, name, detail, deregister, capacity, venue, start_date, end_date, early_bird, fee)

        except ValueError:
            return render_template("course.html", message="Unsuccessful: Unfilled input or incorrect input form")
        except capacityError as error:
            return render_template("course.html", message=error.msg)
        except startDateError as error:
            return render_template("course.html", message=error.msg)
        except EarlyBirdError as error:
            return render_template("course.html", message=error.msg)
        except periodError as error:
            return render_template("course.html", message=error.msg)
        except deregisterError as error:
            return render_template("course.html", message=error.msg)
        except invalidCreator as error:
            return render_template("course.html", message=error.msg)
        except invalidFee as error:
            return render_template("course.html", message=error.msg)
        else:
            if success == 0:
                return render_template("course.html", message="Unsuccessful: Event name is active")
            else:
                return redirect(url_for('home'))
    else:
        return render_template("course.html", user=current_user)

@app.route("/seminar", methods=["GET", "POST"])
@login_required
def create_seminar():
    if request.method == "POST":
        try:
            name = request.form['name']
            detail = request.form['detail']
            #capacity = request.form['capacity']
            venue = request.form['venue']
            date_format = "%Y-%m-%dT%H:%M"
            deregister = datetime.strptime(request.form['deregister'], date_format)
            start_date = datetime.strptime(request.form['start_date'], date_format)
            end_date = datetime.strptime(request.form['end_date'], date_format)
            early_bird = datetime.strptime(request.form['early_bird'], date_format)
            fee = int(request.form['fee'])

            if datetime.now() > start_date:
                raise startDateError("The start date must after the current date.")
            elif early_bird > deregister:
                raise EarlyBirdError("The early bird period must before the deregister period.")
            elif end_date < start_date:
                raise periodError("The start date must before or equal to the end date.")
            elif start_date < deregister:
                raise deregisterError("The deregister period cannot after the start date.")
            elif current_user.role != 'trainer':
                raise invalidCreator("Unauthorised Creator")
            elif fee < 0:
                raise invalidFee("Register fee must at least be 0.")
            else:
                seminar = system.create_seminar(current_user, name, detail, deregister, venue, start_date, end_date, early_bird, fee)
        except ValueError:
            return render_template("seminar.html", message="Unsuccessful: Unfilled input or incorrect input form")
        except startDateError as error:
            return render_template("seminar.html", message=error.msg)
        except EarlyBirdError as error:
            return render_template("seminar.html", message=error.msg)
        except periodError as error:
            return render_template("seminar.html", message=error.msg)
        except deregisterError as error:
            return render_template("seminar.html", message=error.msg)
        except invalidFee as error:
            return render_template("seminar.html", message=error.msg)
        except invalidCreator as error:
            return render_template("seminar.html", message=error.msg)
        else:
            if seminar == 0:
                return render_template("seminar.html", message="Unsuccessful: Event name is active")
            else:
                return redirect(url_for('create_session'))
    else:
        return render_template("seminar.html", user=current_user)

@app.route("/session/create", methods=["GET", "POST"])
@login_required
def create_session():
    seminar = system.tmpSeminar
    if request.method == "POST":
        if request.form['submit'] == "createSession":
            try:
                topic = request.form['topic']
                presenter = request.form['presenter']
                detail = request.form['detail']
                capacity = int(request.form['capacity'])
                guest_type = request.form['presenter_type']
                sessions = seminar.sessions
                count = len(sessions)
                if capacity < 1:
                    raise capacityError("The capacity must at least be 1.")
                else:
                    session = system.create_session(seminar, topic, detail, presenter, capacity)
                    sessions = seminar.sessions
                    count = len(sessions)
            except ValueError:
                return render_template("session.html", message='Unsuccessful: Unfilled input or incorrect input form', seminar=seminar, count=count)
            except capacityError as error:
                return render_template("session.html", message=error.msg, seminar=seminar, count=count)
            else:
                if guest_type == 'guest_speaker':
                    #help guest speaker registered into the
                    username = str(presenter) + '@guestSpeaker.unsw'
                    password = 'admin' + str(presenter)
                    system.add_user(presenter, None, username, password, 'guest')
                    return render_template("session.html", seminar=seminar, sessions=sessions, count=count, check=1)
                    #help the guest speaker register to the session of that event they prensent for
                    # event = system.get_event(event_type, event_id)
                    # system.update_attendees('register', event, event_type, current_user.email)

                return render_template("session.html", seminar=seminar, sessions=sessions, count=count, check=0)

        if request.form['submit'] == "createSeminar":
            success = system.add_seminar(seminar)
            if success == 0:
                return render_template("session.html", message="Minimum two sessions")
            else:
                system.add_sessions(seminar)
                return redirect(url_for('home'))
    else:
        return render_template("session.html", count=0, seminar=None)

#convenor are able to close the event once the event is finished
#just change to event status to 'CLOSED', 'OPEN' or 'CANCEL'
@app.route("/<event_type>/<event_id>/<status>", methods=["GET"])
@login_required
def update_status(event_type, event_id, status):
    if request.method == 'GET':
        system.update_status(event_type, event_id, status)
        event = system.get_event(event_type, event_id)
        return redirect(url_for("display_event", event_type=event_type, \
        event_id=event_id, event_name=event.name))
