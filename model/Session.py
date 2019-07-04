class Session():
    def __init__(self, SessionID, topic, detail, presenter, capacity, noAttendees, SeminarID, status):
        self._SessionID = SessionID
        self._topic = topic
        self._detail = detail
        self._presenter = presenter
        self._capacity = capacity
        self._noAttendees = noAttendees
        self._SeminarID = SeminarID
        self._status = status

    @property
    def SessionID(self):
        return self._SessionID
    @SessionID.setter
    def SessionID(self, SessionID):
        self._SessionID  = SessionID

    @property
    def presenter(self):
        return self._presenter
    @presenter.setter
    def presenter(self, presenter):
        self._presenter = presenter

    def get_seminar(self):
        return self._seminar

    @property
    def detail(self):
        return self._detail

    @detail.setter
    def detail(self, detail):
        self._detail = detail

    @property
    def topic(self):
        return self._topic
    @topic.setter
    def topic(self, topic):
        self._topic = topic

    @property
    def capacity(self):
        return self._capacity
    @capacity.setter
    def capacity(self, capacity):
        self._capacity = capacity

    @property
    def noAttendees(self):
        return self._noAttendees
    @noAttendees.setter
    def noAttendees(self, noAttendees):
        self._noAttendees = noAttendees

    @property
    def SeminarID(self):
        return self._SeminarID
    @SeminarID.setter
    def SeminarID(self, SeminarID):
        self._SeminarID = SeminarID

    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, status):
        self._status = status
