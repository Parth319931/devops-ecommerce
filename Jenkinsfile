pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'parthgandhi23'
        IMAGE_NAME = "${DOCKERHUB_USER}/ecommerce-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    tools {
        nodejs 'NodeJS18'
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
                        dir('frontend') {
                            sh 'CI=true npm test -- --watchAll=false --passWithNoTests'
                        }
                    }
                }
            }
        }

        stage('Security Scan') {
            steps {
                dependencyCheck additionalArguments: '''
                    --scan backend/requirements.txt
                    --scan frontend/package.json
                    --format HTML
                    --format XML
                    --out reports/
                ''', odcInstallation: 'OWASP-DC'

                dependencyCheckPublisher pattern: 'reports/dependency-check-report.xml'
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
                withCredentials([
                    string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                        cd infra/terraform
                        terraform init
                        terraform apply -auto-approve
                        terraform output -json > ../ansible/inventory.json
                    '''
                    sh '''
                        cd infra/ansible
                        python3 generate_inventory.py
                        ansible-playbook -i inventory.ini site.yml
                    '''
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**/*', allowEmptyArchive: true
            echo 'Pipeline completed.'
        }
        success {
            echo 'All stages passed. Application deployed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
        }
    }
}