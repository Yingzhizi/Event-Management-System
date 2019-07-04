class Event(object):
    def __init__(self, event_id, status, name, convenor, detail, deregister, venue, early_bird, register_fee):
        self._event_id = event_id
        self._convenor = convenor
        self._name = name
        self._detail = detail
        self._deregister = deregister
        self._status = status
        self._venue = venue
        self._early_bird = early_bird
        self._register_fee = register_fee

    @property
    def event_id (self):
        return self._event_id

    @event_id.setter
    def event_id (self, id):
        self._event_id = id

    #get convenor name
    @property
    def convenor(self):
        return self._convenor

    #set convenor name
    @convenor.setter
    def convenor(self, convenor):
        self._convenor = convenor

    #get event name
    @property
    def name(self):
        return self._name

    #set event name
    @name.setter
    def name(self, name):
        self.name = name

    #get event details
    #???use _str_
    @property
    def detail(self):
        return self._detail

    #set event detail
    @detail.setter
    def detail(self, detail):
        self._detail = detail

    #get de-register prtiod
    @property
    def deregister(self):
        return self._deregister

    #set de-register period
    @deregister.setter
    def deregister(self, deregister):
        self._deregister = deregister

    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, status):
        self._status = status

    @property
    def venue(self):
        return self._venue
    @venue.setter
    def venue(self, venue):
        self._venue = venue

    @property
    def early_bird(self):
        return self._early_bird
    @early_bird.setter
    def early_bird(self, early_bird):
        self._early_bird = early_bird

    @property
    def register_fee(self):
        return self._register_fee
    @register_fee.setter
    def register_fee(self, register_fee):
        self._register_fee = register_fee

    def __str__(self):
        return "It can be cancelled before {}".format(self.deregister)
