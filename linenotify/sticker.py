from abc import ABCMeta
from enum import Enum


class Sticker(Enum, metaclass=ABCMeta):
    pass

class MoonSpecialEdition(Sticker):
    A = 1, 1
