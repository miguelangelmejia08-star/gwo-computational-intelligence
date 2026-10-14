"""
Prueba de verificacion determinista - Seccion 2 del Taller Integrador GWO
Desafio manual: W5 = (3, 3) con los valores exactos especificados.
"""
import sys
from pathlib import Path

# Asegurar que el directorio raiz del proyecto este en sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import numpy as np
import pytest
from src.gwo import update_one_wolf
from src.objectives import sphere


def test_desafio_manual_w5_determinista():
    """
    Verifica que la actualizacion manual para W5 con r1 y r2 fijos
    produzca exactamente (0.02, 0.54) y f = 0.292 con tolerancia 1e-10.
    """
    # Posicion inicial de W5
    w5 = np.array([3.0, 3.0])

    # Lideres identificados en la seccion 2
    # W4=(0.5, 0.5) con f=0.5 -> alpha
    # W2=(-1.0, 1.0) con f=2.0 -> beta
    # W1=(1.0, 2.0)  con f=5.0 -> delta
    lider_alpha = np.array([0.5, 0.5])
    lider_beta  = np.array([-1.0, 1.0])
    lider_delta = np.array([1.0, 2.0])
    lideres = [lider_alpha, lider_beta, lider_delta]

    # a(5) para T=10, t=5: a = 2*(1 - 5/10) = 1.0
    a = 1.0

    # Numeros dados: r1=(0.60, 0.25, 0.90), r2=(0.50, 0.80, 0.10)
    # En el desafio manual se especifica: "usar los mismos r1 y r2 en ambas dimensiones de cada lider"
    r1_fixed = [
        np.array([0.60, 0.60]),  # alpha
        np.array([0.25, 0.25]),  # beta
        np.array([0.90, 0.90])   # delta
    ]
    r2_fixed = [
        np.array([0.50, 0.50]),  # alpha
        np.array([0.80, 0.80]),  # beta
        np.array([0.10, 0.10])   # delta
    ]

    # Calculo mediante la funcion auxiliar determinista
    x_nuevo = update_one_wolf(w5, lideres, a, r1_fixed, r2_fixed)

    # Valores teoricos esperados
    x_esperado = np.array([0.02, 0.54])
    f_esperado = 0.292

    # Aserciones con tolerancia absoluta 1e-10
    np.testing.assert_allclose(x_nuevo, x_esperado, atol=1e-10,
                               err_msg="La posicion calculada no coincide con el valor teorico (0.02, 0.54)")

    f_nuevo = sphere(x_nuevo)
    assert abs(f_nuevo - f_esperado) <= 1e-10, (
        f"El fitness obtenido {f_nuevo} no coincide con el teorico {f_esperado}"
    )

    # Verificacion de las preguntas conceptuales:
    # d) Mejoro W5? Inicial f(W5) = 18.0 -> nuevo = 0.292. Si, mejoro.
    assert f_nuevo < sphere(w5), "W5 debe mejorar su posicion anterior"
    # d) Supero al alpha actual? f(alpha) = 0.5 -> nuevo = 0.292 < 0.5. Si, lo supero.
    assert f_nuevo < sphere(lider_alpha), "W5 nuevo debe superar al lider alfa actual"


if __name__ == "__main__":
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    pytest.main(["-v", __file__])

