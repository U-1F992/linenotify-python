# linenotify-python

LINE notify Web API wrapper

Plenty of [internal validations](./linenotify/validations.py), easy [error handling](./linenotify/exceptions.py).

## Install

```
pip install linenotify-python
```

## Usage

```python
from os import environ, path

import cv2
import linenotify as ln


TOKEN = environ['LINENOTIFY_TOKEN']


#
# Standard usage
# - Provides all the options described in the documentation.
#
service = ln.Service(TOKEN)

service.notify("text")
service.notify("text + image", cv2.imread(path.join(path.dirname(__file__), "otaku.png")))
service.notify("text + sticker", (446, 1988))
service.notify("text + url", ("http://example.com/thumb.jpg", "https://example.com/body.jpeg"))
service.notify("without notification", notification_disabled=True)

#
# Check API status
# - Status can be obtained from "status" and "notify".
#
status = service.status
status = service.notify("text")

#
# Error handling
# - All exceptions are derived from LINENotifyException, easily caught.
#
invalid_service = ln.Service("invalid token")
try:
    invalid_service.notify("raises an error")
    invalid_service.notify("text + image", cv2.imread("very_large_image.png"))
    invalid_service.notify("text + url", ("url_which_does_not_exist", "same_as_left"))
    # and so on ...

except ln.LINENotifyException:
    pass
```

# API documents

- [LINE Notify API Document](https://notify-bot.line.me/doc/en/)
- [List of available stickers](https://developers.line.biz/en/docs/messaging-api/sticker-list/)
