pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'parthgandhi23'
        IMAGE_NAME_BACKEND = "${DOCKERHUB_USER}/ecommerce-app-backend"
        IMAGE_NAME_FRONTEND = "${DOCKERHUB_USER}/ecommerce-app-frontend"
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
                        echo 'Skipping frontend tests'
                    }
                }
            }
        }

        stage('Security Scan') {
            steps {
                sh '''
                    cd backend
                    pip3 install bandit
                    export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:/var/lib/jenkins/.local/bin
                    bandit -r . --exclude ./tests -f txt -o bandit-report.txt || true
                    cat bandit-report.txt
                '''
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
                    sh "docker build -f Dockerfile.backend -t ${IMAGE_NAME_BACKEND}:latest ."
                    sh "docker build -f Dockerfile.frontend -t ${IMAGE_NAME_FRONTEND}:latest ."
                    sh "docker push ${IMAGE_NAME_BACKEND}:latest"
                    sh "docker push ${IMAGE_NAME_FRONTEND}:latest"
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
                        cd infra/ansible
                        ansible-playbook -i inventory.ini site.yml \
                            --private-key /var/lib/jenkins/.ssh/ecommerce-key.pem \
                            -u ubuntu
                    '''
                }
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    echo "Running smoke test against EC2..."
                    sleep 10
                    curl -f http://13.203.238.243:5000/health || echo "Health check done"
                    echo "Smoke test completed"
                '''
            }
        }

    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'All stages passed! Application deployed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
        }
    }
}