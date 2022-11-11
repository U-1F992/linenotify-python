from __future__ import annotations
from datetime import datetime, timezone

# https://github.com/python/mypy/issues/6239
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from pydantic.dataclasses import dataclass

import requests

from .exceptions import *


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


def get_status(res: requests.Response, tz: timezone) -> Status:
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
        return Status(
            limit=limit,
            image_limit=image_limit,
            remaining=remaining,
            image_remaining=image_remaining,
            reset=reset
        )
    except:
        raise InvalidRequestError()
