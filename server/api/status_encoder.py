import json
from json import JSONEncoder
from .status import Status


class StatusEncoder(JSONEncoder):
    def default(self, obj):

        if isinstance(obj, Status):

            return obj.__dict__

        else:

            # call base class implementation which takes care of

            # raising exceptions for unsupported types

            return json.JSONEncoder.default(self, obj)
