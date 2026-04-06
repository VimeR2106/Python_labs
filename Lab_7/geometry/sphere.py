import math

from .base import SingleParameterBody


class Sphere(SingleParameterBody):
    """Sphere with radius a."""

    @property
    def shape_name(self) -> str:
        return "Шар"

    def volume(self) -> float:
        return (4 / 3) * math.pi * self.a ** 3

    def surface(self) -> float:
        return 4 * math.pi * self.a ** 2
