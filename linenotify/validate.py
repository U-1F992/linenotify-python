from __future__ import annotations
from datetime import datetime, timezone
from io import BytesIO
from os import path
import re
from typing_extensions import Literal
from urllib import request

import cv2
import numpy as np
from PIL import Image
from pydantic.dataclasses import dataclass
import requests

from .exception import *


@dataclass(frozen=True)
class Status:
    """
    Represents connection status
    """
    limit: int
    """
    The limit of API calls per hour
    """
    image_limit: int
    """
    The number of possible remaining API calls
    """
    remaining: int
    """
    The limit of Uploading image per hour
    """
    image_remaining: int
    """
    The number of possible remaining Uploading image
    """
    reset: datetime
    """
    The time when the limit is reset
    """


def validate_response(res: requests.Response, tz: timezone) -> Status:
    try:
        res.raise_for_status()
    except:
        try:
            msg = res.json()["message"]
        except:
            raise UnknownError()
        raise RequestFailedError(msg)

    try:
        limit = int(res.headers["X-RateLimit-Limit"])
        image_limit = int(res.headers["X-RateLimit-ImageLimit"])
        remaining = int(res.headers["X-RateLimit-Remaining"])
        image_remaining = int(res.headers["X-RateLimit-ImageRemaining"])
        reset = datetime.fromtimestamp(
            int(res.headers["X-RateLimit-Reset"]), tz)

    except KeyError:
        raise InvalidRequestError()

    try:
        return Status(limit, image_limit, remaining, image_remaining, reset)
    except:
        raise InvalidRequestError()


def validate_token(token: str) -> dict[Literal["Authorization"], str]:
    """
    Validate the token
    """
    if not isinstance(token, str):
        raise ValidateError("token must be str")
    elif len(token) == 0:
        raise ValidateError("token is one or more characters")
    return {"Authorization": f"Bearer {token}"}


def validate_payload(message: str, attachment: cv2.Mat | tuple[str, str] | tuple[int, int] | None, notification_disabled: bool):
    """
    Validates the arguments and generates the payload dictionary
    """
    _param = {
        **_message(message),
        **_notification_disabled(notification_disabled)
    }

    if attachment is None:
        return {
            "params": _param
        }

    elif isinstance(attachment, np.ndarray):
        return {
            "params": _param,
            "files": _image(attachment),
        }

    if not isinstance(attachment, tuple) or len(attachment) != 2:
        raise ValidateError("Invalid type of attachment")

    a0 = attachment[0]
    a1 = attachment[1]

    if isinstance(a0, int) and isinstance(a1, int):
        return {
            "params": {
                **_param,
                "stickerPackageId": a0,
                "stickerId": a1
            }
        }

    elif isinstance(a0, str) and isinstance(a1, str):
        return {
            "params": {
                **_param,
                **_image_url(a0, "thumbnail"),
                **_image_url(a1, "fullsize")
            }
        }

    else:
        raise ValidateError("Invalid type of attachment")


def _notification_disabled(notification_disabled: bool) -> dict[Literal["notificationDisabled"], bool]:
    """
    Validate notification_disabled
    """
    if not isinstance(notification_disabled, bool):
        raise ValidateError("notification_disabled must be bool")
    return {"notificationDisabled": notification_disabled}


def _message(message: str) -> dict[Literal["message"], str]:
    """
    Validate message
    """
    if not isinstance(message, str):
        raise ValidateError("message must be str")
    if len(message) == 0 or 1000 < len(message):
        raise ValidateError("1 characters min, 1000 characters max")
    return {"message": message}


def _image(image: cv2.Mat) -> dict[Literal["imageFile"], bytes]:
    """
    Validate image
    """
    height, width, _ = image.shape
    if 2048 < height or 2048 < width:
        raise ValidateError("Maximum size of 2048x2048px")

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    png = BytesIO()
    Image.fromarray(rgb).save(png, format='png')
    return {"imageFile": png.getvalue()}


def _get_image_from(url: str) -> cv2.Mat:
    """
    Get image from URL
    """
    try:
        with request.urlopen(url) as res:
            buf = np.frombuffer(res.read(), dtype=np.uint8)
            mat = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)
    except request.HTTPError:
        raise ValidateError("URL not found")
    except:
        raise UnknownError()

    if not isinstance(mat, np.ndarray):
        raise UnknownError()

    return mat


def _image_url(url: str, type_: Literal["thumbnail", "fullsize"]) -> dict[Literal["imageThumbnail", "imageFullsize"], str]:
    """
    Validate image from URL
    """
    if re.fullmatch(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', url) is None:
        raise ValidateError("url must qualifie as a URL")

    _, ext = path.splitext(url)
    if ext != ".jpg" and ext != ".jpeg":
        raise ValidateError("image must be *.jpg or *.jpeg")

    key, limit = ("imageThumbnail", 240) if type_ == "thumbnail" else (
        "imageFullsize", 2048)

    height, width, _ = _get_image_from(url).shape
    if limit < height or limit < width:
        raise ValidateError(f"Maximum size of {limit}x{limit} for {key}")

    return {key: url}
