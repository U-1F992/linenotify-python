class LINENotifyException(Exception):
    """
    Base class for all exceptions raised by linenotify.
    """
    pass
class ValidateError(LINENotifyException):
    """
    Raised when validation fails.
    """
    pass
class RequestFailedError(LINENotifyException):
    """
    Raised when a request fails.
    """
    pass
class UnknownError(LINENotifyException):
    """
    Raised in case of failure with unknown cause
    """
    pass
