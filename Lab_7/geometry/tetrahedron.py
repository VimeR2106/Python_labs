import math

from .base import SingleParameterBody


class Tetrahedron(SingleParameterBody):
    """Regular tetrahedron with edge a."""

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
        return "Тетраэдр"

    def volume(self) -> float:
        return (self.a ** 3) / (6 * math.sqrt(2))

    def surface(self) -> float:
        return math.sqrt(3) * self.a ** 2
