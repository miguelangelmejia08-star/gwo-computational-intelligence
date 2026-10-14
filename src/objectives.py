"""
UNIVERSIDAD DE SAN BUENAVENTURA - MEDELLIN
Facultad de Ingenierias | Inteligencia Computacional
Funciones Objetivo Benchmark
"""
import numpy as np


def sphere(x):
    """
    Funcion Sphere (unimodal, convexa).
    Minimo global f(0, ..., 0) = 0.
    """
    x = np.asarray(x, dtype=float)
    return float(np.sum(x ** 2))


def rastrigin(x):
    """
    Funcion Rastrigin (multimodal, altamente no lineal con multiples minimos locales).
    Minimo global f(0, ..., 0) = 0.
    Dominio tipico: [-5.12, 5.12].
    """
    x = np.asarray(x, dtype=float)
    d = len(x)
    return float(10.0 * d + np.sum(x ** 2 - 10.0 * np.cos(2.0 * np.pi * x)))


def himmelblau(x):
    """
    Funcion Himmelblau (2D, 4 minimos globales con f(x) = 0).
    f(x, y) = (x^2 + y - 11)^2 + (x + y^2 - 7)^2.
    """
    x = np.asarray(x, dtype=float)
    if len(x) != 2:
        raise ValueError("Himmelblau solo esta definida para dimension 2.")
    return float((x[0]**2 + x[1] - 11.0)**2 + (x[0] + x[1]**2 - 7.0)**2)

