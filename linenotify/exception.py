class LINENotifyException(Exception):
    pass

class ValidateError(LINENotifyException):
    pass
class UnknownError(LINENotifyException):
    pass