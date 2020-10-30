class Setting:
    def __init__(self, name, value):
        self.name = name
        self.setting = value
        self.settingId = 0
        self.controlType = 'text'
        self.group = 'search'

    def __str__(self):
        return 'name:' + self.name + ',' + 'setting:' + self.setting

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value == None or value == '':
            raise ValueError('Name cannot be null or empty.')
        self._name = value

    @property
    def setting(self):
        return self._setting

    @setting.setter
    def setting(self, value):
        self._setting = value

    @property
    def controlType(self):
        return self._controlType

    @controlType.setter
    def controlType(self, value):
        if value == None:
            raise ValueError('Control type cannot be null.')
        self._controlType = value

    @property
    def settingId(self):
        return self._settingId

    @settingId.setter
    def settingId(self, value):
        self._settingId = value

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value

    @property
    def label(self):
        return self._label
    @label.setter
    def label(self, value):
        self._label = value

    @property
    def help(self):
        return self._help
    @help.setter
    def help(self, value):
        self._help = value

    @property
    def required(self):
        return self._required
    @required.setter
    def required(self, value):
        self._required = value

    @property
    def placeholder(self):
        return self._placeholder
    @placeholder.setter
    def placeholder(self, value):
        self._placeholder = value

    @property
    def step(self):
        return self._step
    @step.setter
    def step(self, value):
        self._step = value

    @property
    def max(self):
        return self._max
    @max.setter
    def max(self, value):
        self._max = value

    @property
    def min(self):
        return self._min
    @min.setter
    def min(self, value):
        self._min = value

class SettingControlType:
    def __init__(self):
        self.id = 0
        self.name = ''