from .base import TripleParameterBody


class Parallelepiped(TripleParameterBody):
    """Rectangular parallelepiped."""

    def __str__(self) -> str:
        return (
            f"{self.shape_name}(a={self.a}, b={self.b}, c={self.c}, "
            f"material={self.material}, density={self.density})"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"a={self.a!r}, b={self.b!r}, c={self.c!r}, "
            f"density={self.density!r}, material={self.material!r}"
            f")"
        )

    @property
    def shape_name(self) -> str:
        return "Параллелепипед"

    def volume(self) -> float:
        return self.a * self.b * self.c

    def surface(self) -> float:
        return 2 * (self.a * self.b + self.b * self.c + self.a * self.c)
