import datetime


class LogMessage(object):
    def __init__(self, message, submission_date = None):
        if submission_date is None:
            self._submission_date = datetime.datetime.now()
        else:
            self._submission_date = submission_date
        self._message = message

    @property
    def submissiondate(self):
        return self._submission_date

    @submissiondate.setter
    def submissiondate(self, value):
        self._submission_date = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value