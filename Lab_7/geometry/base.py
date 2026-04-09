from abc import ABC, abstractmethod


class GeometryBody(ABC):
    """Base abstract class for geometric bodies."""

    def __init__(self, density: float, material: str) -> None:
        self._density = density
        self.material = material
        print("!!!!")

    @property
    def density(self) -> float:
        return self._density

    @density.setter
    def density(self, value: float) -> None:
        value = float(value)
        if value <= 0:
            raise ValueError("Плотность должна быть положительным числом")
        self._density = value

    @property
    def material(self) -> str:
        return self._material

    @material.setter
    def material(self, value: str) -> None:
        value = str(value).strip()
        if not value:
            raise ValueError("Материал не может быть пустым")
        self._material = value

    @property
    @abstractmethod
    def shape_name(self) -> str:
        """Human-readable shape name."""

    @abstractmethod
    def volume(self) -> float:
        """Return body volume in m^3."""

    @abstractmethod
    def surface(self) -> float:
        """Return body surface area in m^2."""

    def mass(self) -> float:
        return self.density * self.volume()


class SingleParameterBody(GeometryBody):
    """Body with one key linear dimension (a)."""

    def __init__(self, a: float, density: float, material: str) -> None:
        super().__init__(density=density, material=material)
        self.a = a

    @property
    def a(self) -> float:
        return self._a

    @a.setter
    def a(self, value: float) -> None:
        value = float(value)
        if value <= 0:
            raise ValueError("Размер a должен быть положительным числом")
        self._a = value

    def __str__(self) -> str:
        return (
            f"{self.shape_name} "
            f"(a={self.a}, material={self.material}, density={self.density})"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"a={self.a!r}, density={self.density!r}, material={self.material!r}"
            f")"
        )


class TripleParameterBody(GeometryBody):
    """Body with three linear dimensions (a, b, c)."""

    def __init__(self, a: float, b: float, c: float, density: float, material: str) -> None:
        super().__init__(density=density, material=material)
        self.a = a
        self.b = b
        self.c = c

    @staticmethod
    def _validate_side(value: float, name: str) -> float:
        value = float(value)
        if value <= 0:
            raise ValueError(f"Размер {name} должен быть положительным числом")
        return value

    @property
    def a(self) -> float:
        return self._a

    @a.setter
    def a(self, value: float) -> None:
        self._a = self._validate_side(value, "a")

    @property
    def b(self) -> float:
        return self._b

    @b.setter
    def b(self, value: float) -> None:
        self._b = self._validate_side(value, "b")

    @property
    def c(self) -> float:
        return self._c

    @c.setter
    def c(self, value: float) -> None:
        self._c = self._validate_side(value, "c")

    def __str__(self) -> str:
        return (
            f"{self.shape_name} "
            f"(a={self.a}, b={self.b}, c={self.c}, "
            f"material={self.material}, density={self.density})"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"a={self.a!r}, b={self.b!r}, c={self.c!r}, "
            f"density={self.density!r}, material={self.material!r}"
            f")"
        )