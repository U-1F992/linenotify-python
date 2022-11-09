from datetime import datetime, timezone
from typing import Optional, Tuple, Union

import cv2
import requests

from .exception import RequestFailedError, UnknownError
from .validate import validate_payloads, validate_token


class _Status:
    """
    Represents connection status
    """

    def __init__(self, res: requests.Response, tz: timezone) -> None:
        """
        Represents connection status
        """
        try:
            res.raise_for_status()
        except:
            try:
                raise RequestFailedError(res.json()["message"])
            except:
                raise UnknownError()

        self.__limit = int(res.headers["X-RateLimit-Limit"])
        self.__image_limit = int(res.headers["X-RateLimit-ImageLimit"])
        self.__remaining = int(res.headers["X-RateLimit-Remaining"])
        self.__image_remaining = int(res.headers["X-RateLimit-ImageRemaining"])
        self.__reset = datetime.fromtimestamp(
            int(res.headers["X-RateLimit-Reset"]), tz)

    @property
    def limit(self):
        """
        The limit of API calls per hour
        """
        return self.__limit

    @property
    def image_limit(self):
        """
        The number of possible remaining API calls
        """
        return self.__image_limit

    @property
    def remaining(self):
        """
        The limit of Uploading image per hour
        """
        return self.__remaining

    @property
    def image_remaining(self):
        """
        The number of possible remaining Uploading image
        """
        return self.__image_remaining

    @property
    def reset(self):
        """
        The time when the limit is reset
        """
        return self.__reset


class _Service:
    """
    Represents the LINE Notify service
    """

    def __init__(self, token: str, tz: timezone = datetime.utcnow().astimezone().tzinfo) -> None:
        """
        Represents the LINE Notify service
        """
        self.__header = validate_token(token)
        self.__tz = tz if tz is not None else timezone.utc

    def notify(self, message: str, attachment: Optional[Union[Tuple[int, int], Tuple[str, str], cv2.Mat]] = None, notification_disabled=False) -> _Status:
        """Sends notifications to users or groups that are related to an access token.

        Args:
            message (str): Message to be sent
            attachment (Optional[Union[Tuple[int, int], Tuple[str, str], cv2.Mat]], optional): Choose from image, image URL (thumbnail and body), or [sticker](https://developers.line.biz/en/docs/messaging-api/sticker-list/). Defaults to None.
            notification_disabled (bool, optional): Whether to disable push notifications for users. Defaults to False.

        Returns:
            _Status: Connection status
        """
        return _Status(requests.post(
            "https://notify-api.line.me/api/notify",
            headers=self.__header,
            **validate_payloads(message, attachment, notification_disabled)
        ), self.__tz)

    def status(self) -> _Status:
        """An API for checking connection status.

        Returns:
            _Status: Connection status
        """
        return _Status(requests.get(
            "https://notify-api.line.me/api/status",
            headers=self.__header
        ), self.__tz)


def get_service(token: str, tz: Optional[timezone] = None) -> _Service:
    """Get a LINE Notify service from token

    Args:
        token (str): Token
        tz (Optional[timezone], optional): Time Zone. If omitted, attempts to get the standard time zone of system. Defaults to None.

    Returns:
        _Service: LINE Notify service
    """
    return _Service(token) if tz is None else _Service(token, tz)
