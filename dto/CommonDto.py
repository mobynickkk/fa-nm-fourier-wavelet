from dataclasses import dataclass

from .Serializable import Serializable


class CommonDto(type):

    def __new__(mcs, name, bases, dict_):
        result = type(name, (Serializable,) + bases, dict_)
        return dataclass(init=True, frozen=True)(result)
