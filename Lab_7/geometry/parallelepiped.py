from .base import TripleParameterBody


class Parallelepiped(TripleParameterBody):
    """Rectangular parallelepiped."""

    @property
    def shape_name(self) -> str:
        return "Параллелепипед"

    def volume(self) -> float:
        return self.a * self.b * self.c

    def surface(self) -> float:
        return 2 * (self.a * self.b + self.b * self.c + self.a * self.c)
