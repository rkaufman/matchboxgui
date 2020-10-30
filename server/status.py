class Status:
    def __init__(self, name, status, display, icon):
        self._name = name
        self._status = status
        self._display = display
        self._icon = icon

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
    @property
    def status(self):
        return self._status
    @status.setter
    def status(self, value):
        self._status = value

    @property
    def display(self):
        return self._display
    @display.setter
    def display(self, value):
        self._display = value

    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
