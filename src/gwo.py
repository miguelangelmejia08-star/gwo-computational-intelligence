"""
UNIVERSIDAD DE SAN BUENAVENTURA - MEDELLIN
Facultad de Ingenierias | Inteligencia Computacional
Algoritmo: Grey Wolf Optimizer (GWO)
Implementacion completa con validaciones, actualizacion sincronica y pruebas.
"""
import numpy as np
import matplotlib.pyplot as plt


def actualizar_lobo(x, lideres, a, rng):
    """
    Actualiza UN lobo desde las posiciones de la iteracion anterior.

    Parametros:
        x: vector 1D con la posicion actual del lobo.
        lideres: lista/tupla de 3 vectores [alpha, beta, delta].
        a: parametro de control de decaimiento (lineal o cuadratico).
        rng: generador pseudoaleatorio de NumPy (default_rng).

    Retorna:
        Vector 1D con la posicion promedio calculada a partir de las 3 propuestas.
    """
    dim = len(x)
    propuestas = []

    for lider in lideres:
        # TODO 3: generar r1 y r2 independientes, vectores de tamano len(x).
        r1 = rng.uniform(0.0, 1.0, size=dim)
        r2 = rng.uniform(0.0, 1.0, size=dim)

        # TODO 4: calcular A, C, D y la propuesta del lider.
        A = 2.0 * a * r1 - a
        C = 2.0 * r2
        D = np.abs(C * lider - x)
        P = lider - A * D
        propuestas.append(P)

    # TODO 5: retornar el promedio de las tres propuestas.
    return (propuestas[0] + propuestas[1] + propuestas[2]) / 3.0


def update_one_wolf(x, lideres, a, r1_fixed, r2_fixed):
    """
    Funcion auxiliar determinista para verificar el calculo manual sin depender del RNG.
    
    Parametros:
        x: vector posicion del lobo a actualizar.
        lideres: lista [alpha, beta, delta].
        a: valor escalar de a(t).
        r1_fixed: lista o arreglo de 3 vectores (o escalares por lider).
        r2_fixed: lista o arreglo de 3 vectores (o escalares por lider).
    """
    x = np.asarray(x, dtype=float)
    propuestas = []
    for j in range(3):
        lider = np.asarray(lideres[j], dtype=float)
        r1 = np.asarray(r1_fixed[j], dtype=float)
        r2 = np.asarray(r2_fixed[j], dtype=float)
        A = 2.0 * a * r1 - a
        C = 2.0 * r2
        D = np.abs(C * lider - x)
        P = lider - A * D
        propuestas.append(P)
    return (propuestas[0] + propuestas[1] + propuestas[2]) / 3.0


def gwo(f, dim=2, lb=-5.12, ub=5.12, n_lobos=20,
        iteraciones=100, seed=42, modo='lineal'):
    """
    Algoritmo Grey Wolf Optimizer (GWO) para minimizacion.

    Parametros:
        f: funcion objetivo a minimizar.
        dim: dimension del espacio de busqueda (>= 1).
        lb: limite inferior de las variables (escalar o vector).
        ub: limite superior de las variables (escalar o vector).
        n_lobos: tamano de la manada (>= 3).
        iteraciones: numero total de ciclos T (>= 1).
        seed: semilla para reproducibilidad.
        modo: decaimiento de a(t) ('lineal' o 'cuadratico').

    Retorna:
        mejor_posicion: vector con el mejor punto historico encontrado.
        mejor_valor: menor valor de f obtenido.
        historial: arreglo 1D con la curva de convergencia monotona (tamano T).
        evaluaciones: total de evaluaciones de la funcion objetivo.
    """
    if n_lobos < 3:
        raise ValueError("n_lobos debe ser mayor o igual a 3 para seleccionar alfa, beta y delta.")
    if dim < 1:
        raise ValueError("dim debe ser un entero positivo >= 1.")
    if iteraciones < 1:
        raise ValueError("iteraciones debe ser >= 1.")
    if np.any(np.asarray(lb) >= np.asarray(ub)):
        raise ValueError("El limite inferior 'lb' debe ser estrictamente menor que 'ub'.")
    if modo not in ('lineal', 'cuadratico'):
        raise ValueError("modo debe ser 'lineal' o 'cuadratico'.")

    rng = np.random.default_rng(seed)
    
    # Inicializar poblacion
    X = rng.uniform(lb, ub, size=(n_lobos, dim))
    fitness = np.array([float(f(x)) for x in X])
    evaluaciones = n_lobos  # incluir la poblacion inicial

    # Identificar el mejor historico inicial
    idx_mejor_inicial = np.argmin(fitness)
    mejor_valor = fitness[idx_mejor_inicial]
    mejor_posicion = X[idx_mejor_inicial].copy()

    historial = []

    for t in range(iteraciones):
        # TODO 1: ordenar fitness y obtener una COPIA de los 3 lideres.
        orden = np.argsort(fitness)
        lider_alpha = X[orden[0]].copy()
        lider_beta  = X[orden[1]].copy()
        lider_delta = X[orden[2]].copy()
        lideres = [lider_alpha, lider_beta, lider_delta]

        # TODO 2: calcular a(t) segun el modo elegido.
        # En t=0, a=2. En t=T-1, a decrece hacia 0.
        frac = t / float(iteraciones)
        if modo == 'lineal':
            a = 2.0 * (1.0 - frac)
        elif modo == 'cuadratico':
            a = 2.0 * (1.0 - (frac ** 2))

        # Actualizacion SINCRONICA
        X_anterior = X.copy()
        X_nuevo = np.empty_like(X_anterior)

        for i in range(n_lobos):
            # TODO 5: llamar actualizar_lobo y aplicar np.clip(lb, ub).
            x_prop = actualizar_lobo(X_anterior[i], lideres, a, rng)
            X_nuevo[i] = np.clip(x_prop, lb, ub)

        X = X_nuevo
        fitness = np.array([float(f(x)) for x in X])
        evaluaciones += n_lobos

        # TODO 6: actualizar mejor_valor y mejor_posicion SOLO si mejora.
        min_idx = np.argmin(fitness)
        if fitness[min_idx] < mejor_valor:
            mejor_valor = fitness[min_idx]
            mejor_posicion = X[min_idx].copy()

        # TODO 6: agregar mejor_valor al historial (curva monotona no creciente).
        historial.append(mejor_valor)

    return mejor_posicion, mejor_valor, np.asarray(historial), evaluaciones


def graficar(historial, titulo='Convergencia GWO'):
    """Grafica la curva de convergencia en escala semilogaritmica."""
    plt.figure(figsize=(8, 4))
    plt.semilogy(np.maximum(historial, 1e-15))
    plt.xlabel('Iteracion')
    plt.ylabel('Mejor valor historico (escala log)')
    plt.title(titulo)
    plt.grid(True, alpha=0.3)
    plt.show()

