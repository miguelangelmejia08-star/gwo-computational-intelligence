# syntax=docker/dockerfile:1
FROM python:3.11-slim

LABEL maintainer="Inteligencia Computacional - Universidad de San Buenaventura"
LABEL description="Entorno reproducible para Grey Wolf Optimizer (GWO), tests, experimentos y Jupyter Notebook"

# Evitar prompts interactivos y generacion de archivos .pyc innecesarios
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema minimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el codigo fuente del proyecto
COPY . .

# Crear directorio para reportes
RUN mkdir -p reports

# Exponer el puerto para JupyterLab / Notebook
EXPOSE 8888

# Por defecto, ejecutar la suite completa de pruebas de verificacion
CMD ["pytest", "-v", "tests/"]

