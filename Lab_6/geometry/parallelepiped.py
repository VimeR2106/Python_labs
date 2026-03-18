# Модуль 1: Параллелепипед

def volume(a, b, c):
    """Объём = a * b * c"""
    return a * b * c

def surface(a, b, c):
    """Площадь поверхности = 2*(ab + bc + ac)"""
    return 2 * (a * b + b * c + a * c)

def mass(density, a, b, c):
    """Масса = плотность * объём"""
    return density * volume(a, b, c)
