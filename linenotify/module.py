from __future__ import annotations
from datetime import datetime, timezone

import cv2
import requests

from .exception import *
from .validate import Status, validate_payload, validate_response, validate_token


class Service:
    """
    Represents the LINE Notify service
    """

    def __init__(self, token: str, tz: timezone = datetime.utcnow().astimezone().tzinfo) -> None:
        """Represents the LINE Notify service

        All documentation can be found [here](https://notify-bot.line.me/doc/en/)

        Args:
            token (str): Token
            tz (timezone, optional):Time Zone. If omitted, attempts to get the standard time zone of system. Defaults to datetime.utcnow().astimezone().tzinfo.
        """
        self.__header = validate_token(token)
        self.__tz = tz if tz is not None else timezone.utc

    def notify(self, message: str, attachment: cv2.Mat | tuple[str, str] | tuple[int, int] | None = None, notification_disabled=False) -> Status:
        """Sends notifications to users or groups that are related to an access token.

        Args:
            message (str): Message to be sent
            attachment (cv2.Mat | tuple[str, str] | tuple[int, int] | None, optional): Choose from image, image URL (thumbnail and body), or sticker. Defaults to None.
            notification_disabled (bool, optional): Whether to disable push notifications for users. Defaults to False.

        Returns:
            Status: Connection status
        """
        payload = validate_payload(message, attachment, notification_disabled)
        try:
            res = requests.post(
                "https://notify-api.line.me/api/notify",
                headers=self.__header,
                **payload
            )
        except requests.exceptions.RequestException:
            raise RequestFailedError()
        except:
            raise UnknownError()

        return validate_response(res, self.__tz)

    def status(self) -> Status:
        """An API for checking connection status.

        Returns:
            Status: Connection status
        """
        try:
            res = requests.get(
                "https://notify-api.line.me/api/status",
                headers=self.__header
            )
        except requests.exceptions.RequestException:
            raise RequestFailedError()
        except:
            raise UnknownError()

        return validate_response(res, self.__tz)
