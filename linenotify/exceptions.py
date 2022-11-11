class LINENotifyException(Exception):
    """
    Base class for all exceptions raised by linenotify.
    """


class ValidateError(LINENotifyException):
    """
    Raised when validation fails.
    """

    def __init__(self, msg="validation failed", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class RequestFailedError(LINENotifyException):
    """
    Raised when a request fails.
    """

    def __init__(self, msg="request failed", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class InvalidRequestError(LINENotifyException):
    """
    Raised when an invalid request was given.
    """

    def __init__(self, msg="invalid request", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


class UnknownError(LINENotifyException):
    """
    Raised in case of failure with unknown cause.
    """

    def __init__(self, msg="unknown error occurred", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
