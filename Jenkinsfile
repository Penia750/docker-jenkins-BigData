pipeline {
    agent any

    environment {
        // Ruta relativa dentro del workspace de Jenkins
        DATASET_PATH = 'sdss_sample.csv' // Archivo dentro del repo
    }

    stages {
        stage('Checkout del Repositorio') {
            steps {
                script {
                    echo 'Realizando checkout del repositorio...'
                    // Git está configurado desde SCM en la interfaz de Jenkins
                }
            }
        }

        stage('List Workspace (verificar CSV)') {
            steps {
                script {
                    echo 'Listando archivos en el workspace para confirmar que sdss_sample.csv está presente'
                    bat 'dir'
                }
            }
        }

        stage('Instalación de Dependencias') {
            steps {
                script {
                    echo 'Construyendo imagen Docker e instalando dependencias...'
                    bat 'docker build -t ml-pipeline-sdss .'
                }
            }
        }

        stage('Ejecución de Pruebas Básicas del Dataset') {
            steps {
                script {
                    echo 'Ejecutando pruebas básicas del dataset dentro del contenedor Docker...'
                    bat """
                        docker run --rm ^
                        -v %cd%\\basic_data_tests.py:/app/basic_data_tests.py ^
                        -v %cd%\\${DATASET_PATH}:/app/sdss_sample.csv ^
                        ml-pipeline-sdss python /app/basic_data_tests.py
                    """
                }
            }
        }

        stage('Ejecución del Script Principal') {
            steps {
                script {
                    echo 'Ejecutando el pipeline de ML dentro del contenedor Docker...'
                    bat """
                        docker run --rm ^
                        -v %cd%\\${DATASET_PATH}:/content/sample_data/sdss_sample.csv ^
                        -v %cd%\\outputs:/app/outputs ^
                        ml-pipeline-sdss
                    """
                }
            }
        }

        stage('Almacenamiento de Artefactos') {
            steps {
                script {
                    echo 'Archivando métricas y gráficas...'
                    archiveArtifacts artifacts: 'outputs\\**\\*', fingerprint: true
                    echo 'Pipeline de ML completado y artefactos archivados.'
                }
            }
        }
    }
}
