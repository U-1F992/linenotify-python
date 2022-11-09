from os import path
from typing import Any, Optional, Tuple, Union
from urllib import request

import cv2
import numpy as np
import requests

from .exception import UnknownError, ValidateError
from .sticker import Sticker

ENDPOINT = "hoge"

def _validate_token(token: str):
    pass

def _validate_message(message: str):
    if 1000 < len(message):
        raise ValidateError()

def _validate_attachment(attachment: Optional[Union[Sticker, Tuple[str, str], cv2.Mat]]):
    if attachment is None:
        return
    elif isinstance(attachment, Sticker):
        return

    elif isinstance(attachment, Tuple[str, str]):
        _validate_url_thumbnail(attachment[0])
        _validate_url_fullsize(attachment[1])

    elif isinstance(attachment, cv2.Mat):
        _validate_image(attachment)

def _get_image_from(url: str) -> cv2.Mat:
    try:
        with request.urlopen(url) as res:
            buf = np.frombuffer(res.read(), dtype=np.uint8)
            mat = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)
    except request.HTTPError:
        raise ValidateError()
    except:
        raise UnknownError()

    return mat

def _validate_image(image: cv2.Mat):
    height, width, _ = image.shape
    if 2048 < height or 2048 < width:
        raise ValidateError()

def _validate_url(url: str):
    _, ext = path.splitext(url)
    if ext != ".jpg" and ext != ".jpeg":
        raise ValidateError()

def _validate_url_thumbnail(url: str):
    _validate_url(url)
    height, width, _ = _get_image_from(url).shape
    if 240 < height or 240 < width:
        raise ValidateError()

def _validate_url_fullsize(url: str):
    _validate_url(url)
    _validate_image(_get_image_from(url))

def _build_header(name: str, data: Any):
    pass

def notify(token: str, message: str, attachment: Optional[Union[Sticker, Tuple[str, str], cv2.Mat]]=None, notification_disabled=False):
    _validate_token(token)
    _validate_message(message)
    _validate_attachment(attachment)
    res = requests.post()
