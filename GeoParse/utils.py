import re

__author__ = 'booka'

def js_val_converter(self, val):
    """
    :param val: ``Any`` the value to get the equivalent Javascript value for
    :return: ``str`` the val converted to its proper javascript type
    """
    if type(val) is bool:
        return 'true' if val else 'false'
    elif type(val) is str:
        return "'{v}'".format(v=re.escape(val))
    elif type(val) is unicode:
        return "'{v}'".format(v=re.escape(str(val)))
    elif type(val) is int or type(val) is float:
        return val
    elif type(val) is list or type(val) is tuple:
        escaped = "["
        for v in val:
            escaped += "{val},".format(val=self._js_val_converter(v))
        escaped = escaped.rstrip(",")
        escaped += "]"
        return escaped
    elif type(val) is dict:
        escaped = "{"
        for k, v in val.items():
            escaped += "{k}:{v},".format(k=str(k), v=self._js_val_converter(v))
        escaped = escaped.rstrip(",")
        escaped += "}"
        return escaped
    elif isinstance(val, object):
        obj_fields = val.__dict__
        escaped = self._js_val_converter(obj_fields)
        return escaped
    else:
        return 'null'
