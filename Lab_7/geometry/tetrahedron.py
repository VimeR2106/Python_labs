import math

from .base import SingleParameterBody


class Tetrahedron(SingleParameterBody):
    """Regular tetrahedron with edge a."""

    @property
    def shape_name(self) -> str:
        return "Тетраэдр"

    def volume(self) -> float:
        return (self.a ** 3) / (6 * math.sqrt(2))

    def surface(self) -> float:
        return math.sqrt(3) * self.a ** 2
