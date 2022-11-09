from typing import Optional, Tuple, Union
from urllib import request

import cv2

from linenotify.sticker import Sticker

ENDPOINT = "hoge"

def notify(token: str, message: str, attachment: Optional[Union[Sticker, Tuple[str, str], cv2.Mat]]=None, notification_disabled=False):
    res = request.post()
