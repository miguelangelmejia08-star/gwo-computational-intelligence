"""
Pruebas automaticas minimas requeridas por la rubrica del Taller Integrador GWO:
1. np.isfinite(best_f)
2. best_f >= -1e-10 para Sphere y Rastrigin
3. np.all(np.diff(hist) <= 1e-12) (curva monotonica no creciente)
4. len(hist) == T
5. n_eval == n_wolves * (T + 1) (contar todas las evaluaciones, incluida la inicial)
6. Todas las posiciones dentro de limites [lb, ub]
7. Validacion de excepciones para parametros no validos
"""
import numpy as np
import pytest
from src.gwo import gwo
from src.objectives import sphere, rastrigin


@pytest.mark.parametrize("f_obj, dim, lb, ub", [
    (sphere, 2, -5.12, 5.12),
    (sphere, 10, -5.12, 5.12),
    (rastrigin, 2, -5.12, 5.12),
    (rastrigin, 10, -5.12, 5.12),
])
@pytest.mark.parametrize("modo", ["lineal", "cuadratico"])
def test_gwo_propiedades_minimas(f_obj, dim, lb, ub, modo):
    n_lobos = 20
    iteraciones = 50
    seed = 42

    posicion, valor, historial, evals = gwo(
        f=f_obj,
        dim=dim,
        lb=lb,
        ub=ub,
        n_lobos=n_lobos,
        iteraciones=iteraciones,
        seed=seed,
        modo=modo
    )

    # 1. np.isfinite(best_f)
    assert np.isfinite(valor), "El mejor valor debe ser finito."

    # 2. best_f >= -1e-10 (Sphere y Rastrigin tienen minimo teorico >= 0)
    assert valor >= -1e-10, "El valor optimo no puede ser significativamente menor a 0."

    # 3. Curva monotonica no creciente: ningun paso posterior empeora el mejor historico
    diffs = np.diff(historial)
    assert np.all(diffs <= 1e-12), "El mejor historico no debe empeorar en ninguna iteracion."

    # 4. Longitud del historial exactamente igual a T
    assert len(historial) == iteraciones, f"El historial debe tener longitud T={iteraciones}."

    # 5. Conteo exacto de evaluaciones: inicial + T iteraciones
    evals_esperadas = n_lobos * (iteraciones + 1)
    assert evals == evals_esperadas, f"Las evaluaciones deben ser {evals_esperadas}, pero fueron {evals}."

    # 6. Posiciones dentro de limites
    assert np.all(posicion >= lb - 1e-10) and np.all(posicion <= ub + 1e-10), (
        "La mejor posicion encontrada esta fuera de los limites [lb, ub]."
    )


def test_gwo_validaciones_parametros():
    """Verifica que se levanten excepciones adecuadas con parametros invalidos."""
    with pytest.raises(ValueError):
        gwo(sphere, n_lobos=2)  # Menos de 3 lobos
    with pytest.raises(ValueError):
        gwo(sphere, dim=0)  # Dimension invalida
    with pytest.raises(ValueError):
        gwo(sphere, iteraciones=0)  # Iteraciones invalidas
    with pytest.raises(ValueError):
        gwo(sphere, lb=5.0, ub=-5.0)  # lb >= ub
    with pytest.raises(ValueError):
        gwo(sphere, modo='invalido')  # Modo no soportado

