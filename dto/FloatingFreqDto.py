from .CommonDto import CommonDto


class FloatingFreqDto(metaclass=CommonDto):
    values: list
    maxFrequency: int
