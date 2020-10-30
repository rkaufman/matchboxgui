class ControlType(object):
    def __init__(self, *args, **kwargs):
        self._id = args[0]
        self._name = args[1]
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value