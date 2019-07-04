from model.Event import Event

class Course(Event):
    def __init__(self, event_id, status, name, convenor, detail, deregister, capacity, noAttendees, venue, start_date, end_date, early_bird, register_fee):
        super().__init__(event_id, status, name, convenor, detail, deregister, venue, early_bird, register_fee)
        self._capacity = capacity
        self._noAttendees = noAttendees
        self._start_date = start_date
        self._end_date =end_date

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
    def capacity(self):
        return self._capacity
    #set event detail
    @capacity.setter
    def capacity(self, capacity):
        self._capacity = capacity

    @property
    def noAttendees(self):
        return self._noAttendees
    @noAttendees.setter
    def noAttendees(self, num):
        self._noAttendees = num
