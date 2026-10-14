pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        PYTHONPATH = "${WORKSPACE}"
        IMAGE_NAME = "gwo-optimizer"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Preparacion del Entorno') {
            steps {
                echo "=========================================================="
                echo "Iniciando Pipeline de CI para Grey Wolf Optimizer (GWO)"
                echo "Workspace: ${WORKSPACE}"
                echo "Build ID: ${BUILD_NUMBER}"
                echo "=========================================================="
                sh 'python3 --version || python --version || true'
                sh 'pip --version || true'
                sh 'docker --version || true'
                sh 'mkdir -p reports'
            }
        }

        stage('Verificacion de Sintaxis y Lint') {
            steps {
                echo "--> Validando sintaxis de archivos Python..."
                sh '''
                    python3 -m py_compile src/*.py tests/*.py || python -m py_compile src/*.py tests/*.py
                '''
            }
        }

        stage('Pruebas Unitarias y Deterministas') {
            steps {
                echo "--> Ejecutando pruebas deterministas y de propiedades minimas..."
                sh '''
                    pytest -v tests/ --junitxml=reports/junit-results.xml || python -m pytest -v tests/ --junitxml=reports/junit-results.xml
                '''
            }
        }

        stage('Ejecucion de Experimentos y Benchmark') {
            steps {
                echo "--> Corriendo campana experimental (Sphere, Rastrigin d=10 y PSO)..."
                sh '''
                    python3 src/experiments.py || python src/experiments.py
                '''
            }
        }

        stage('Construccion y Validacion Docker') {
            steps {
                echo "--> Construyendo imagen Docker contenedorizada..."
                sh """
                    if command -v docker >/dev/null 2>&1; then
                        docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .
                        docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} pytest -v tests/
                    else
                        echo "Aviso: Docker CLI no esta montado en el agente Jenkins actual. Etapa omitida con exito."
                    fi
                """
            }
        }
    }

    post {
        always {
            echo "--> Archivando resultados de pruebas y graficas generadas..."
            junit testResults: 'reports/junit-*.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'reports/**, notebooks/**', allowEmptyArchive: true
        }
        success {
            echo "=========================================================="
            echo "Pipeline GWO completado EXITOSAMENTE!"
            echo "Todos los tests matematicos y experimentales fueron validados."
            echo "=========================================================="
        }
        failure {
            echo "=========================================================="
            echo "ERROR: El pipeline ha fallado. Revisar los logs anteriores."
            echo "=========================================================="
        }
    }
}

