import math

from .base import SingleParameterBody


class Sphere(SingleParameterBody):
    """Sphere with radius a."""

    def __str__(self) -> str:
        return f"{self.shape_name}(a={self.a}, material={self.material}, density={self.density})"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"a={self.a!r}, density={self.density!r}, material={self.material!r}"
            f")"
        )

    @property
    def shape_name(self) -> str:
        return "Шар"

    def volume(self) -> float:
        return (4 / 3) * math.pi * self.a ** 3

    def surface(self) -> float:
        return 4 * math.pi * self.a ** 2
