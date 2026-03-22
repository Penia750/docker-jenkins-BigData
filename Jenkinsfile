pipeline {
    agent any

    environment {
        // Define aquí variables de entorno si las necesitas, por ejemplo, la ruta al dataset
        DATASET_PATH = '/app/sdss_sample.csv' // Ruta esperada dentro del contenedor Docker
    }

    stages {
        stage('Checkout del Repositorio') {
            steps {
                script {
                    echo 'Realizando checkout del repositorio...'
                    // Asume que tu código está en un sistema de control de versiones como Git
                    // git url: 'https://github.com/tu-usuario/tu-repositorio.git', branch: 'main'
                    // Para este ejemplo, asumimos que el código ya está presente o se copiará manualmente.
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
                    // Primero, vamos a crear un script de Python para estas pruebas
                    // y lo ejecutaremos en un contenedor efímero o montando el archivo.
                    // Aquí se asume que 'basic_data_tests.py' existe y está en el repositorio.
                    // Necesitarás copiar el dataset al entorno de Jenkins o montarlo.
                    sh '''
                        docker run --rm \
                        -v $(pwd)/basic_data_tests.py:/app/basic_data_tests.py \
                        -v /path/to/your/sdss_sample.csv:/app/sdss_sample.csv \
                        ml-pipeline-sdss python /app/basic_data_tests.py
                    '''
                    // Reemplaza /path/to/your/sdss_sample.csv con la ruta real en tu servidor Jenkins
                }
            }
        }

        stage('Ejecución del Script Principal') {
            steps {
                script {
                    echo 'Ejecutando el pipeline de ML dentro del contenedor Docker...'
                    // Ejecuta el script principal 'main.py' dentro del contenedor
                    // Montamos el dataset y el directorio de outputs.
                    sh '''
                        docker run --rm \
                        -v /path/to/your/sdss_sample.csv:/content/sample_data/sdss_sample.csv \
                        -v $(pwd)/outputs:/app/outputs \
                        ml-pipeline-sdss
                    '''
                    // Reemplaza /path/to/your/sdss_sample.csv con la ruta real en tu servidor Jenkins
                }
            }
        }

        stage('Almacenamiento de Artefactos') {
            steps {
                script {
                    echo 'Archivando métricas y gráficas...'
                    // Archiva todos los archivos generados en la carpeta 'outputs'
                    archiveArtifacts artifacts: 'outputs/**/*', fingerprint: true
                    echo 'Pipeline de ML completado y artefactos archivados.'
                }
            }
        }
    }
}
