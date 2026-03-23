pipeline {
    agent any

    environment {
        // Archivo CSV dentro del repo
        DATASET_PATH = 'sdss_sample.csv'
    }

    stages {
        stage('Checkout del Repositorio') {
            steps {
                script {
                    echo 'Realizando checkout del repositorio...'
                    git branch: 'main', url: 'https://github.com/Penia750/docker-jenkins-BigData.git'
                }
            }
        }

        stage('List Workspace (verificar CSV)') {
            steps {
                script {
                    echo 'Listando archivos en el workspace para confirmar que sdss_sample.csv está presente'
                    sh 'ls -l ${WORKSPACE}'
                }
            }
        }

        stage('Instalación de Dependencias') {
            steps {
                script {
                    echo 'Construyendo imagen Docker e instalando dependencias...'
                    sh 'docker build -t ml-pipeline-sdss .'
                }
            }
        }

        stage('Ejecución de Pruebas Básicas del Dataset') {
            steps {
                script {
                    echo 'Ejecutando pruebas básicas del dataset dentro del contenedor Docker...'
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
