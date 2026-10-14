"""Modulo principal GWO e Inteligencia Computacional."""
from .objectives import sphere, rastrigin, himmelblau
from .gwo import gwo, actualizar_lobo, update_one_wolf, graficar
from .pso import pso

__all__ = [
    'sphere', 'rastrigin', 'himmelblau',
    'gwo', 'actualizar_lobo', 'update_one_wolf', 'graficar',
    'pso'
]

