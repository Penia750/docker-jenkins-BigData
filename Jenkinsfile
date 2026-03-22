pipeline {
    agent any

    environment {
        // Ahora usamos la ruta relativa dentro del workspace de Jenkins
        DATASET_PATH = 'sdss_sample.csv' // Archivo dentro del repo
    }

    stages {
        stage('Checkout del Repositorio') {
            steps {
                script {
                    echo 'Realizando checkout del repositorio...'
                    // git url: 'https://github.com/tu-usuario/tu-repositorio.git', branch: 'main'
                    // Jenkins clona el repo automáticamente si configuraste SCM
                }
            }
        }

        stage('Instalación de Dependencias') {
            steps {
                script {
                    echo 'Construyendo imagen Docker e instalando dependencias...'
                    // Construir la imagen Docker. Asegúrate de que Docker esté disponible en el agente de Jenkins.
                    sh 'docker build -t ml-pipeline-sdss .'
                }
            }
        }

        stage('Ejecución de Pruebas Básicas del Dataset') {
            steps {
                script {
                    echo 'Ejecutando pruebas básicas del dataset dentro del contenedor Docker...'
                    // Montamos el dataset desde el workspace de Jenkins
                    sh '''
                        docker run --rm \
                        -v $(pwd)/basic_data_tests.py:/app/basic_data_tests.py \
                        -v $(pwd)/${DATASET_PATH}:/app/sdss_sample.csv \
                        ml-pipeline-sdss python /app/basic_data_tests.py
                    '''
                }
            }
        }

        stage('Ejecución del Script Principal') {
            steps {
                script {
                    echo 'Ejecutando el pipeline de ML dentro del contenedor Docker...'
                    sh '''
                        docker run --rm \
                        -v $(pwd)/${DATASET_PATH}:/content/sample_data/sdss_sample.csv \
                        -v $(pwd)/outputs:/app/outputs \
                        ml-pipeline-sdss
                    '''
                }
            }
        }

        stage('Almacenamiento de Artefactos') {
            steps {
                script {
                    echo 'Archivando métricas y gráficas...'
                    archiveArtifacts artifacts: 'outputs/**/*', fingerprint: true
                    echo 'Pipeline de ML completado y artefactos archivados.'
                }
            }
        }
    }
}
