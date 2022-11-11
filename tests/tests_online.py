from __future__ import annotations
from os import environ, path

import cv2
import pytest

import linenotify as ln


TOKEN = environ['LINENOTIFY_TOKEN']


def test_status():
    service = ln.Service(TOKEN)
    service.status


@pytest.mark.parametrize(("message, attachment, notification_disabled"), [
    ("text", None, False),
    ("text + image", cv2.imread(path.join(path.dirname(__file__), "otaku.png")), False),
    ("text + sticker", (446, 1988), False),
    ("text + url", ("https://i.ibb.co/p18Z5BZ/thumb.jpg",
     "https://i.ibb.co/hKb7sPn/body.jpg"), False),
    ("text (without notification)", None, True),
    ("text + image (without notification)",
     cv2.imread(path.join(path.dirname(__file__), "otaku.png")), True),
    ("text + sticker (without notification)", (446, 1988), True),
    ("text + url (without notification)", ("https://i.ibb.co/p18Z5BZ/thumb.jpg",
     "https://i.ibb.co/hKb7sPn/body.jpg"), True),
])
def test_notify(message: str, attachment: cv2.Mat | tuple[str, str] | tuple[int, int] | None, notification_disabled: bool):
    service = ln.Service(TOKEN)
    service.notify(message, attachment, notification_disabled)
