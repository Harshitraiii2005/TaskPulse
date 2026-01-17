pipeline {
    agent any

    environment {
        VENV_NAME       = "venv"
        PYTHON_VERSION  = "python3.10"
        DOCKER_USERNAME = "harshitrai20"
        IMAGE_NAME      = "taskpulse-app"
        IMAGE_TAG       = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                set -e
                ${PYTHON_VERSION} -m venv ${VENV_NAME}
                . ${VENV_NAME}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

    

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${DOCKER_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                    docker tag ${DOCKER_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} \
                               ${DOCKER_USERNAME}/${IMAGE_NAME}:latest

                    docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Please check the logs.'
        }
        always {
            echo 'ℹ️ CI run completed'
        }
    }
}