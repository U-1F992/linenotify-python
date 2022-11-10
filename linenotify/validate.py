from io import BytesIO
from os import path
from typing import Optional, Tuple, Union
from typing_extensions import TypedDict
from urllib import request

import cv2
from PIL import Image
import numpy as np

from .exception import UnknownError, ValidateError

class ParamRequired(TypedDict):
    message: str
    notificationDisabled: bool
class Param(ParamRequired, total=False):
    stickerPackageId: int
    stickerId: int
    imageThumbnail: str
    imageFullsize: str
class ImageFile(TypedDict):
    imageFile: bytes

class PayloadRequired(TypedDict):
    param: Param
class Payload(PayloadRequired, total=False):
    files: ImageFile

def validate_token(token: str):
    """
    Validate the token (but nothing so far)
    """
    return {"Authorization": f"Bearer {token}"}


def validate_payload(message: str, attachment: Optional[Union[Tuple[int, int], Tuple[str, str], cv2.Mat]], notification_disabled: bool) -> Payload:
    """
    Validates the arguments and generates the payload dictionary
    """
    _param: Param = {**_message(message), **_notification_disabled(notification_disabled)}

    if attachment is None:
        ret: Payload = {
            "params": _param
        }
        return ret

    elif isinstance(attachment, np.ndarray):
        ret: Payload = {
            "params": _param,
            "files": _image(attachment)
        }
        return ret

    elif isinstance(attachment[0], int) and isinstance(attachment[1], int):
        ret: Payload = {
            "params": {
                **_param,
                "stickerPackageId": attachment[0],
                "stickerId": attachment[1]
            }
        }
        return ret

    elif isinstance(attachment[0], str) and isinstance(attachment[1], str):
        ret: Payload = {
            "params": {
                **_param,
                **_image_url(attachment[0], "thumbnail"),
                **_image_url(attachment[1], "fullsize")
            }
        }
        return ret

    else:
        raise ValidateError("Invalid type of attachment")


def _notification_disabled(notification_disabled: bool):
    """
    Validate notification_disabled
    """
    if not isinstance(notification_disabled, bool):
        raise ValidateError("notification_disabled must be bool")
    return {"notificationDisabled": notification_disabled}


def _message(message: str):
    """
    Validate message
    """
    if len(message) == 0 or 1000 < len(message):
        raise ValidateError("1 characters min, 1000 characters max")
    return {"message": message}

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
