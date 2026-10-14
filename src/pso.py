"""
UNIVERSIDAD DE SAN BUENAVENTURA - MEDELLIN
Facultad de Ingenierias | Inteligencia Computacional
Algoritmo: Particle Swarm Optimization (PSO)
Implementacion canonica para comparacion con GWO (2020 evaluaciones exactas).
"""
import numpy as np


def pso(f, dim=10, lb=-5.12, ub=5.12, n_particles=20,
        iterations=100, seed=42, w=0.7, c1=1.5, c2=1.5):
    """
    Particle Swarm Optimization (PSO) para minimizacion.

    Parametros:
        f: funcion objetivo.
        dim: dimension del problema.
        lb, ub: limites del espacio de busqueda.
        n_particles: numero de particulas en el enjambre (default 20).
        iterations: iteraciones T (default 100).
        seed: semilla para reproducibilidad.
        w: peso de inercia.
        c1: coeficiente cognitivo (pbest).
        c2: coeficiente social (gbest).

    Retorna:
        gbest_x: mejor posicion global encontrada.
        gbest_f: menor valor de f obtenido.
        historial: curva de mejor historico monotona (tamano iterations).
        evaluaciones: total de evaluaciones (n_particles * (iterations + 1)).
    """
    rng = np.random.default_rng(seed)
    
    # Inicializar posiciones y velocidades
    X = rng.uniform(lb, ub, size=(n_particles, dim))
    v_max = 0.2 * (ub - lb)
    V = rng.uniform(-v_max, v_max, size=(n_particles, dim))

    # Evaluacion inicial
    fitness = np.array([float(f(x)) for x in X])
    evaluaciones = n_particles

    # Mejores posiciones individuales (pbest)
    pbest_X = X.copy()
    pbest_f = fitness.copy()

    # Mejor posicion global (gbest)
    best_idx = np.argmin(pbest_f)
    gbest_x = pbest_X[best_idx].copy()
    gbest_f = float(pbest_f[best_idx])

    historial = []

    for t in range(iterations):
        r1 = rng.uniform(0.0, 1.0, size=(n_particles, dim))
        r2 = rng.uniform(0.0, 1.0, size=(n_particles, dim))

        # Actualizacion de velocidad
        V = (w * V +
             c1 * r1 * (pbest_X - X) +
             c2 * r2 * (gbest_x - X))
        V = np.clip(V, -v_max, v_max)

        # Actualizacion de posicion
        X = np.clip(X + V, lb, ub)

        # Evaluacion
        fitness = np.array([float(f(x)) for x in X])
        evaluaciones += n_particles

        # Actualizar pbest y gbest
        for i in range(n_particles):
            if fitness[i] < pbest_f[i]:
                pbest_f[i] = fitness[i]
                pbest_X[i] = X[i].copy()
                if fitness[i] < gbest_f:
                    gbest_f = fitness[i]
                    gbest_x = X[i].copy()

        historial.append(gbest_f)

    return gbest_x, gbest_f, np.asarray(historial), evaluaciones

