# Taller Integrador: Grey Wolf Optimizer (GWO) & Benchmark PSO
**Universidad de San Buenaventura - Medellín**  
**Facultad de Ingenierías | Inteligencia Computacional**  
**Docente:** Andrés Felipe Hernández Marulanda  

---

## 📌 Descripción del Proyecto
Este repositorio contiene la solución técnica y formal del **Taller Integrador: Grey Wolf Optimizer (GWO)**. El proyecto está diseñado con estándares de calidad de software e ingeniería de datos, preparado para integración continua (**Jenkins**), contenedorización (**Docker** / **Docker Compose**) y versionamiento colaborativo (**GitHub**).

El trabajo abarca:
1. **Desafío Manual y Verificación Matemática:** Cálculo analítico riguroso del movimiento del lobo $W_5$ con tolerancia absoluta $10^{-10}$.
2. **Implementación de GWO:** Algoritmo metaheurístico completo sin librerías externas de optimización, con actualización sincrónica y decaimientos de $a(t)$ lineal y cuadrático.
3. **Pruebas Automatizadas (PyTest):** Suite de pruebas unitarias que validan propiedades matemáticas, límites de dominio, monotonicidad de convergencia y presupuesto exacto de evaluaciones.
4. **Campaña Experimental:** Comparación estadística (20 corridas) sobre las funciones *Sphere* y *Rastrigin* ($d=10$) evaluando media, desviación estándar, mejor valor y tasa de éxito.
5. **Benchmark con PSO:** Comparación justa contra Particle Swarm Optimization en *Rastrigin* ($d=10$) con un presupuesto estricto de **2020 evaluaciones** por corrida.
6. **Reto Opcional:** Visualización 2D de curvas de nivel y trayectoria del lobo alfa sobre la función multimodal de *Himmelblau*.
7. **Jupyter Notebook Entregable:** `notebooks/GWO_Apellido1_Apellido2.ipynb` formateado para entrega académica o Google Colab.

---

## 📁 Estructura del Repositorio

```text
gwo-computational-intelligence/
├── Dockerfile                  # Imagen Docker para ejecucion reproducible
├── docker-compose.yml          # Orquestacion de servicios (tests, experiments, jupyter)
├── Jenkinsfile                 # Pipeline declarativo CI/CD para Jenkins
├── requirements.txt            # Dependencias de Python (NumPy, Matplotlib, PyTest, Jupyter)
├── .gitignore                  # Exclusion de artefactos, temporales y checkpoints
├── .dockerignore               # Archivos omitidos en el contexto del contenedor Docker
├── README.md                   # Documentacion tecnica del proyecto
├── src/                        # Modulos de codigo fuente
│   ├── __init__.py
│   ├── objectives.py           # Funciones Sphere, Rastrigin y Himmelblau
│   ├── gwo.py                  # Algoritmo GWO, actualizacion sincronica y graficador
│   ├── pso.py                  # Algoritmo PSO canonico para contraste
│   └── experiments.py          # Runner de la campana experimental y generador de graficas
├── tests/                      # Suite de pruebas automatizadas
│   ├── __init__.py
│   ├── test_manual_determinista.py  # Test determinista del calculo manual (tol 1e-10)
│   └── test_gwo_properties.py       # Pruebas de monotonicidad, limites y presupuesto
├── notebooks/                  # Cuaderno interactivo de entrega
│   └── GWO_Apellido1_Apellido2.ipynb
└── reports/                    # Directorio de salida para graficas y reportes JUnit
```

---

## 🚀 Guía de Instalación y Ejecución Local

### Prerrequisitos
* Python 3.10 o superior (ej. Python 3.11, 3.12, 3.14).
* Git instalado.

### 1. Clonar o acceder a la carpeta del proyecto
```bash
cd C:\Users\migue\.gemini\antigravity\scratch\gwo-computational-intelligence
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python -m venv venv
# En Windows PowerShell:
.\venv\Scripts\Activate.ps1
# En Linux/Mac/Git Bash:
# source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Ejecutar las pruebas unitarias
```bash
pytest -v tests/
```
> Todas las pruebas (deterministas y propiedades mínimas) deben pasar en verde (`PASSED`).

### 4. Ejecutar la campaña experimental y generar gráficas
```bash
python src/experiments.py
```
> Esto generará las figuras `reports/convergence_gwo.png` y `reports/convergence_pso_vs_gwo.png` junto con las tablas en consola.

### 5. Abrir el Jupyter Notebook
```bash
jupyter notebook notebooks/GWO_Apellido1_Apellido2.ipynb
```
O bien, subir directamente el archivo `notebooks/GWO_Apellido1_Apellido2.ipynb` a [Google Colab](https://colab.research.google.com/).

---

## 🐳 Despliegue con Docker y Docker Compose

El proyecto está 100% contenedorizado para garantizar reproducibilidad en cualquier sistema operativo sin necesidad de configurar librerías locales.

### Opción A: Con Docker Compose (Recomendado)

1. **Ejecutar las pruebas unitarias en contenedor:**
   ```bash
   docker-compose run --rm tests
   ```

2. **Ejecutar la campaña experimental:**
   ```bash
   docker-compose run --rm experiments
   ```
   *Las gráficas generadas se guardarán automáticamente en tu carpeta local `./reports` mediante volúmenes montados.*

3. **Levantar el entorno interactivo de Jupyter Notebook:**
   ```bash
   docker-compose up jupyter
   ```
   *Abre tu navegador en `http://localhost:8888` (sin contraseña requerida).*

### Opción B: Con comandos directos de Docker

1. **Construir la imagen:**
   ```bash
   docker build -t gwo-optimizer:latest .
   ```

2. **Ejecutar los tests:**
   ```bash
   docker run --rm gwo-optimizer:latest pytest -v tests/
   ```

3. **Ejecutar experimentos y extraer reportes:**
   ```bash
   docker run --rm -v ${PWD}/reports:/app/reports gwo-optimizer:latest python src/experiments.py
   ```

---

## 🏗️ Integración Continua con Jenkins

El archivo `Jenkinsfile` implementa un **Pipeline Declarativo** que automatiza la validación matemática, experimental y de contenedorización.

### Etapas del Pipeline (`Jenkinsfile`):
1. **Preparación del Entorno:** Validación de versiones (`python`, `pip`, `docker`) y creación de directorios.
2. **Verificación de Sintaxis y Lint:** Compilación estática de bytecode con `py_compile`.
3. **Pruebas Unitarias y Deterministas:** Ejecución de `pytest` generando reportes XML estándar `junit-results.xml`.
4. **Ejecución de Experimentos y Benchmark:** Corridas de Sphere, Rastrigin y PSO.
5. **Construcción y Validación Docker:** Construcción de la imagen y prueba dentro del contenedor.
6. **Post-Acciones:** Publicación de resultados de tests JUnit y archivo de artefactos (gráficas PNG y notebook).

### Pasos para configurar el Pipeline en Jenkins:
1. Abrir Jenkins (`http://localhost:8080`).
2. Click en **Nueva Tarea (New Item)** $\to$ Nombre: `GWO-Computational-Intelligence` $\to$ Seleccionar **Pipeline** $\to$ Click en **OK**.
3. En la sección **Pipeline**:
   * **Definition:** Seleccionar `Pipeline script from SCM`.
   * **SCM:** Seleccionar `Git`.
   * **Repository URL:** Colocar la URL de tu repositorio de GitHub (ej. `https://github.com/tu-usuario/gwo-computational-intelligence.git`).
   * **Branch Specifier:** `*/main` o `*/master`.
   * **Script Path:** `Jenkinsfile`.
4. Guardar y hacer clic en **Construir Ahora (Build Now)**.
5. Visualizar los resultados y descargar las gráficas desde los **Build Artifacts**.

---

## 🐙 Publicación en GitHub

Para subir este proyecto a un nuevo repositorio en GitHub:

1. **Crear un nuevo repositorio en GitHub:**
   * Entra a [github.com/new](https://github.com/new).
   * Nombre del repositorio: `gwo-computational-intelligence` (o el nombre de tu preferencia).
   * Visibilidad: Pública o Privada.
   * **No** inicializar con README ni .gitignore (ya están incluidos en el proyecto).

2. **Inicializar git y subir desde tu terminal:**
   ```bash
   cd C:\Users\migue\.gemini\antigravity\scratch\gwo-computational-intelligence

   # Inicializar git
   git init

   # Configurar rama principal
   git branch -M main

   # Agregar todos los archivos
   git add .

   # Crear el commit inicial
   git commit -m "feat: implementacion completa GWO, tests deterministas, campana experimental, Docker y Jenkins"

   # Vincular con tu repositorio de GitHub (reemplaza con tu URL)
   git remote add origin https://github.com/TU_USUARIO/gwo-computational-intelligence.git

   # Subir cambios
   git push -u origin main
   ```

---

## 📊 Síntesis de Resultados y Rúbrica Académica

### 1. Desafío Manual (W5 = (3, 3), t=5, T=10, a=1.0)
* **Líder Alfa ($\alpha$):** $W_4 = (0.5, 0.5)$, $f=0.5$
* **Líder Beta ($\beta$):** $W_2 = (-1.0, 1.0)$, $f=2.0$
* **Líder Delta ($\delta$):** $W_1 = (1.0, 2.0)$, $f=5.0$
* **Propuestas:** $P_\alpha = (0.0, 0.0)$, $P_\beta = (1.3, 1.7)$, $P_\delta = (-1.24, -0.08)$
* **Posición Nueva:** $X_{\text{nuevo}} = (0.02, 0.54)$
* **Fitness Nuevo:** $f(X_{\text{nuevo}}) = 0.2920$
* **Conclusiones:** $W_5$ mejoró de $18.0 \to 0.2920$ y superó al líder alfa actual ($0.2920 < 0.5$).

### 2. Comparación GWO vs PSO (Rastrigin d=10, 2020 evaluaciones)
1. GWO logró un menor valor medio final en Rastrigin $d=10$ que PSO.
2. PSO mejoró más rápido al inicio gracias al impulso cinético de su velocidad.
3. PSO colapsó prematuramente al atraparse en óptimos locales.
4. PSO depende de inercia y memoria personal ($pbest$) y global ($gbest$).
5. GWO carece de memoria individual y velocidad, guiándose por el promedio de tres líderes.
6. La triangulación de $\alpha, \beta, \delta$ ofrece mayor diversidad exploratoria y evita trampas multimodales.

