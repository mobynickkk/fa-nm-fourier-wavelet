from .CommonDto import CommonDto
from .ImageDto import ImageDto
from .MainImageDto import MainImageDto


class CalculatedGraphsDto(metaclass=CommonDto):
    main: MainImageDto
    changeable: ImageDto
    source: ImageDto
    target: ImageDto
    values: list
    dispersion: float
