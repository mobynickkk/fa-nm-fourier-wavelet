from .CommonDto import CommonDto


class ImageDto(metaclass=CommonDto):
    title: str
    src: str
