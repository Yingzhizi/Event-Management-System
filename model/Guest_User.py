from flask_login import UserMixin

class Guest_User(UserMixin):
    def __init__(self, GuestID, Name, Email, Password):
        self._GuestID = GuestID
        self._name = Name
        self._email = Email
        self._password = Password

    @property
    def GuestID(self):
        return self._GuestID
    @GuestID.setter
    def GuestID(self, GuestID):
        self._GuestID = GuestID

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, password):
        self._password = password

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, email):
        self._email = email

    def get_id(self):
        return self._email
