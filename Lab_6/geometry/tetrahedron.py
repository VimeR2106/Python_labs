import math

# Модуль 2: Правильный тетраэдр (все рёбра равны a)

def volume(a):
    """Объём = a^3 / (6 * sqrt(2))"""
    return (a ** 3) / (6 * math.sqrt(2))

def surface(a):
    """Площадь поверхности = sqrt(3) * a^2"""
    return math.sqrt(3) * a ** 2

def mass(density, a):
    """Масса = плотность * объём"""
    return density * volume(a)
