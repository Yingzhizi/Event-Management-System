from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, name, zID, email, password, role):
        self._name = name
        self._zID = zID
        self._email = email
        self._password = password
        self._role = role

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def zID(self):
        return self._zID
    @zID.setter
    def zID(self, zID):
        self._zID = zID

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, email):
        self._email = email

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, password):
        self._password = password

    @property
    def role(self):
        return self._role
    @role.setter
    def role(self, role):
        self._role = role

    def __str__(self):
        return "Name: " + self._name + " Password: " + self._password + " role: " + self._role

    def get_id(self):
        return self._email
