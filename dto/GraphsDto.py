import typing as T

from .CommonDto import CommonDto


class GraphsDto(metaclass=CommonDto):
    file: T.Any
    transformType: str
