from __future__ import annotations
from os import environ, path

import cv2
import pytest

import linenotify as ln


TOKEN = environ['LINENOTIFY_TOKEN']


def test_status():
    service = ln.Service(TOKEN)
    with pytest.raises(ln.RequestFailedError):
        service.status


def test_notify():
    service = ln.Service(TOKEN)
    with pytest.raises(ln.RequestFailedError):
        service.notify("text")
