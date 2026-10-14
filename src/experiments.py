"""
UNIVERSIDAD DE SAN BUENAVENTURA - MEDELLIN
Facultad de Ingenierias | Inteligencia Computacional
Modulo de Campana Experimental y Benchmark (Secciones 4 y 5)
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from src.objectives import sphere, rastrigin
from src.gwo import gwo
from src.pso import pso


def run_campaign(output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)
    semillas = [0, 1, 2, 3, 4]
    dim = 10
    lb, ub = -5.12, 5.12
    n_lobos = 20
    T = 100

    print("=" * 80)
    print("EJECUTANDO CAMPANA EXPERIMENTAL GWO (SECCION 4)")
    print("=" * 80)

    funciones = [
        ("Sphere", sphere),
        ("Rastrigin", rastrigin)
    ]
    modos = ["lineal", "cuadratico"]

    resultados = {}
    curvas_promedio = {}

    for f_nombre, f_func in funciones:
        for modo in modos:
            clave = f"{f_nombre}_{modo}"
            valores_finales = []
            historiales = []
            evals_list = []

            for s in semillas:
                pos, val, hist, evals = gwo(
                    f=f_func, dim=dim, lb=lb, ub=ub,
                    n_lobos=n_lobos, iteraciones=T, seed=s, modo=modo
                )
                valores_finales.append(val)
                historiales.append(hist)
                evals_list.append(evals)

            valores_finales = np.array(valores_finales)
            historiales = np.array(historiales)  # shape (5, T)
            media = np.mean(valores_finales)
            std = np.std(valores_finales, ddof=1) if len(semillas) > 1 else 0.0
            mejor = np.min(valores_finales)
            evals_corrida = evals_list[0]

            # Tasa de exito para Rastrigin (f_best < 1e-3)
            tasa_exito = np.mean(valores_finales < 1e-3) if f_nombre == "Rastrigin" else np.nan

            resultados[clave] = {
                "media": media,
                "std": std,
                "mejor": mejor,
                "evals": evals_corrida,
                "tasa_exito": tasa_exito
            }
            curvas_promedio[clave] = np.mean(historiales, axis=0)

    # Imprimir Tabla de la Seccion 4
    print("\nTABLA DE RESULTADOS - CAMPANA EXPERIMENTAL GWO")
    print("| Funcion | a(t) | Media final | Desv. est. | Mejor final | Evals/corrida | Tasa Exito (<1e-3) |")
    print("|---|---|---|---|---|---|---|")
    for (f_nombre, _) in funciones:
        for modo in modos:
            clave = f"{f_nombre}_{modo}"
            res = resultados[clave]
            tasa_str = f"{res['tasa_exito']*100:.1f}%" if not np.isnan(res['tasa_exito']) else "N/A"
            print(f"| {f_nombre:<9} | {modo.capitalize():<10} | {res['media']:<11.4e} | {res['std']:<10.4e} | {res['mejor']:<11.4e} | {res['evals']:<13} | {tasa_str:<18} |")

    # Grafica de Convergencia GWO (Sphere y Rastrigin)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Sphere
    ax = axes[0]
    ax.semilogy(np.maximum(curvas_promedio["Sphere_lineal"], 1e-12), label="Lineal", color="navy", lw=2)
    ax.semilogy(np.maximum(curvas_promedio["Sphere_cuadratico"], 1e-12), label="Cuadratico", color="crimson", lw=2, linestyle="--")
    ax.set_title("Convergencia Promedio - Sphere (d=10)", fontsize=12)
    ax.set_xlabel("Iteracion", fontsize=11)
    ax.set_ylabel("Mejor fitness historico (log)", fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)

    # Rastrigin
    ax = axes[1]
    ax.semilogy(np.maximum(curvas_promedio["Rastrigin_lineal"], 1e-12), label="Lineal", color="navy", lw=2)
    ax.semilogy(np.maximum(curvas_promedio["Rastrigin_cuadratico"], 1e-12), label="Cuadratico", color="crimson", lw=2, linestyle="--")
    ax.set_title("Convergencia Promedio - Rastrigin (d=10)", fontsize=12)
    ax.set_xlabel("Iteracion", fontsize=11)
    ax.set_ylabel("Mejor fitness historico (log)", fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)

    plt.tight_layout()
    gwo_fig_path = os.path.join(output_dir, "convergence_gwo.png")
    plt.savefig(gwo_fig_path, dpi=300)
    plt.close()
    print(f"\nGrafico de convergencia GWO guardado en: {gwo_fig_path}")

    # =========================================================================
    # SECCION 5: COMPARACION CON PSO (Rastrigin d=10, 2020 evaluaciones)
    # =========================================================================
    print("\n" + "=" * 80)
    print("EJECUTANDO COMPARACION GWO VS PSO EN RASTRIGIN d=10 (SECCION 5)")
    print("=" * 80)

    pso_valores = []
    pso_historiales = []

    for s in semillas:
        pos, val, hist, evals = pso(
            f=rastrigin, dim=dim, lb=lb, ub=ub,
            n_particles=n_lobos, iterations=T, seed=s
        )
        pso_valores.append(val)
        pso_historiales.append(hist)

    pso_valores = np.array(pso_valores)
    pso_historiales = np.array(pso_historiales)
    pso_media = np.mean(pso_valores)
    pso_std = np.std(pso_valores, ddof=1)
    pso_mejor = np.min(pso_valores)

    gwo_res = resultados["Rastrigin_lineal"]

    print("\nTABLA COMPARATIVA: GWO (Lineal) vs PSO en Rastrigin (d=10, 2020 evaluaciones)")
    print("| Algoritmo | Media final | Desv. est. | Mejor final | Evaluaciones |")
    print("|---|---|---|---|---|")
    print(f"| GWO (Lineal) | {gwo_res['media']:<11.4e} | {gwo_res['std']:<10.4e} | {gwo_res['mejor']:<11.4e} | {gwo_res['evals']} |")
    print(f"| PSO          | {pso_media:<11.4e} | {pso_std:<10.4e} | {pso_mejor:<11.4e} | {2020} |")

    # Grafica Comparativa GWO vs PSO
    pso_promedio = np.mean(pso_historiales, axis=0)
    evals_axis = np.linspace(n_lobos, n_lobos * (T + 1), T)

    plt.figure(figsize=(9, 5))
    plt.plot(evals_axis, curvas_promedio["Rastrigin_lineal"], label="GWO (Lineal)", color="navy", lw=2.5)
    plt.plot(evals_axis, pso_promedio, label="PSO", color="darkorange", lw=2.5, linestyle="--")
    plt.title("Comparacion de Convergencia: GWO vs PSO en Rastrigin (d=10)", fontsize=13)
    plt.xlabel("Evaluaciones de la Funcion Objetivo", fontsize=11)
    plt.ylabel("Mejor Fitness Historico", fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()

    comp_fig_path = os.path.join(output_dir, "convergence_pso_vs_gwo.png")
    plt.savefig(comp_fig_path, dpi=300)
    plt.close()
    print(f"Grafico comparativo GWO vs PSO guardado en: {comp_fig_path}")

    return resultados, pso_media, pso_std, pso_mejor


if __name__ == "__main__":
    run_campaign()

