from model.Event import Event

# remove attendees_list and status for now
# for test
class Seminar(Event):
    def __init__(self, id, status, name, convenor, detail, deregister, venue, start_date, end_date, early_bird, register_fee):
        super().__init__(id, status, name, convenor, detail, deregister, venue, early_bird, register_fee)
        self._start_date = start_date
        self._end_date = end_date
        self._sessions = []

    @property
    def start_date(self):
        return self._start_date
    @start_date.setter
    def start_date(self, start_date):
        self._start_date = start_date

    @property
    def end_date(self):
        return self._end_date
    @end_date.setter
    def end_date(self, end_date):
        self._end_date = end_date

    @property
    def sessions(self):
        return self._sessions

    def add_session(self, session):
        self._sessions.append(session)

    def get_sessions(self):
        return self._sessions

    def display(self):
        for session in self.sessions:
            print(session)

#    def get_seminar_name(self):
#        return self._name

    def __str__(self):
        return "Event ID: " + str(self._event_id) + " Status: " + str(self._status) + " Convenor: " + str(self._convenor) \
        + " end_date " + str(self.end_date)
