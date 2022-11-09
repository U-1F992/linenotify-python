from os import environ, path
from time import sleep

import cv2

import linenotify as ln


def print_status(status: ln._Status):
    print("--- status ---")
    print(status.limit)
    print(status.image_limit)
    print(status.remaining)
    print(status.image_remaining)
    print(status.reset)
    print()

if __name__ == "__main__":

    service = ln.get_service(environ['LINENOTIFY_TOKEN'])

    print("show status")
    print_status(service.status())
    sleep(2)

    print("notify text")
    print_status(service.notify("text"))
    sleep(2)

    print("notify text & image")
    print_status(service.notify("text & image", cv2.imread(path.join(path.dirname(__file__), "otaku.png"))))
    sleep(2)

    print("notify text & sticker")
    print_status(service.notify("text & sticker", (446, 1988)))
    sleep(10)

    # print("notify text & image_url")
    # print_status(service.notify("text & image_url", ("https://sample.com/thumb.jpg", "https://sample.com/full.jpeg")))
    # sleep(10)

    print("notify without notification")
    print_status(service.notify("notify without notification", notification_disabled=True))
    sleep(10)

    service.notify("with notification")
