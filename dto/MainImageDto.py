from .CommonDto import CommonDto


class MainImageDto(metaclass=CommonDto):
    title: str
    src: str
    minFreq: float
    maxFreq: float
    stepFreq: float
