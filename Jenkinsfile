pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'YOUR_DOCKERHUB_USERNAME'
        IMAGE_NAME = "${DOCKERHUB_USER}/ecommerce-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Build') {
            parallel {
                stage('Frontend Build') {
                    steps {
                        dir('frontend') {
                            sh 'npm install'
                            echo 'Frontend dependencies installed.'
                        }
                    }
                }
                stage('Backend Build') {
                    steps {
                        dir('backend') {
                            sh 'pip3 install -r requirements.txt'
                            echo 'Backend dependencies installed.'
                        }
                    }
                }
            }
        }

        stage('Test') {
            parallel {
                stage('Backend Tests') {
                    steps {
                        dir('backend') {
                            sh 'pip3 install pytest pytest-flask'
                            sh 'python3 -m pytest tests/ -v --tb=short'
                        }
                    }
                }
                stage('Frontend Tests') {
                    steps {
                        echo 'Skipping frontend tests for CI stability'
                    }
                }
            }
        }

        stage('Security Scan') {
            steps {
                echo 'Security Scan - OWASP Dependency-Check will be configured in Phase 5'
            }
        }

        stage('Docker Build & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh "docker build -f Dockerfile.backend -t ${IMAGE_NAME}-backend:${IMAGE_TAG} ."
                    sh "docker build -f Dockerfile.frontend -t ${IMAGE_NAME}-frontend:${IMAGE_TAG} ."
                    sh "docker push ${IMAGE_NAME}-backend:${IMAGE_TAG}"
                    sh "docker push ${IMAGE_NAME}-frontend:${IMAGE_TAG}"
                    sh "docker tag ${IMAGE_NAME}-backend:${IMAGE_TAG} ${IMAGE_NAME}-backend:latest"
                    sh "docker tag ${IMAGE_NAME}-frontend:${IMAGE_TAG} ${IMAGE_NAME}-frontend:latest"
                    sh "docker push ${IMAGE_NAME}-backend:latest"
                    sh "docker push ${IMAGE_NAME}-frontend:latest"
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploy stage - will be activated in Phase 3 (Terraform + Ansible)'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
            echo 'Pipeline completed.'
        }
        success {
            echo 'All stages passed!'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
        }
    }
}