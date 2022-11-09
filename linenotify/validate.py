from io import BytesIO
from os import path
from typing import Optional, Tuple, Union
from urllib import request

import cv2
from PIL import Image
import numpy as np

from .exception import UnknownError, ValidateError


def validate_token(token: str):
    """
    Validate the token (but nothing so far)
    """
    return {"Authorization": f"Bearer {token}"}


def validate_payloads(message: str, attachment: Optional[Union[Tuple[int, int], Tuple[str, str], cv2.Mat]], notification_disabled: bool):
    """
    Validates the arguments and generates the payload dictionary
    """
    _dis = {"notificationDisabled": notification_disabled}

    if len(message) == 0 or 1000 < len(message):
        raise ValidateError("1 characters min, 1000 characters max")
    _msg = {"message": message, **_dis}

    if attachment is None:
        return {"params": _msg}

    elif isinstance(attachment, np.ndarray):
        return {
            "params": _msg,
            "files": _image(attachment)
        }

    elif isinstance(attachment[0], int) and isinstance(attachment[1], int):
        _att = {"stickerPackageId": attachment[0], "stickerId": attachment[1]}

    elif isinstance(attachment[0], str) and isinstance(attachment[1], str):
        _att = {**_image_url(attachment[0], "thumbnail"), **_image_url(attachment[1], "fullsize")}

    else:
        return {"params": _msg}

    return {"params": {**_msg, **_att}}


def _image(image: cv2.Mat):
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
    

def _image_url(url: str, type_: str):
    """
    Validate image from URL
    """
    _, ext = path.splitext(url)
    if ext != ".jpg" and ext != ".jpeg":
        raise ValidateError("image must be *.jpg or *.jpeg")

    key, limit = ("imageThumbnail", 240) if type_ == "thumbnail" else (
        "imageFullsize", 2048)

    height, width, _ = _get_image_from(url).shape
    if limit < height or limit < width:
        raise ValidateError(f"Maximum size of {limit}x{limit} for {key}")

    return {key: url}
