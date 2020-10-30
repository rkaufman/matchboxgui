class User():
    def __init__(self, id):
        self._id = id
        self._username = ''
        self._password = ''

    def __str__(self):
        return "User(id='%s')" % self.id

    @property
    def username(self):
        return self._username
    @username.setter
    def username(self, value):
        if value == None or value == '':
            raise ValueError('Username cannot be blank')
        self._username = value

    @property
    def password(self):
        return self._password
    @password.setter
    def password(self, value):
        self._password = value

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value
    