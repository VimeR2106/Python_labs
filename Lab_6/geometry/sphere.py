import math

# Модуль 3: Шар

def volume(r):
    """Объём = (4/3) * pi * r^3"""
    return (4 / 3) * math.pi * r ** 3

def surface(r):
    """Площадь поверхности = 4 * pi * r^2"""
    return 4 * math.pi * r ** 2

def mass(density, r):
    """Масса = плотность * объём"""
    return density * volume(r)
