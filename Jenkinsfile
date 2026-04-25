pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'skadssagar'
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
                        }
                    }
                }
                stage('Backend Build') {
                    steps {
                        dir('backend') {
                            sh 'pip3 install -r requirements.txt'
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
                echo 'Security scan placeholder'
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

                    sh "docker build -f Dockerfile.backend -t ${DOCKERHUB_USER}/ecommerce-app-backend:latest ."
                    sh "docker build -f Dockerfile.frontend -t ${DOCKERHUB_USER}/ecommerce-app-frontend:latest ."

                    sh "docker push ${DOCKERHUB_USER}/ecommerce-app-backend:latest"
                    sh "docker push ${DOCKERHUB_USER}/ecommerce-app-frontend:latest"
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
                        export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                        export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                        terraform init
                        terraform apply -auto-approve
                        terraform output -raw public_ip > ../ansible/ec2_ip.txt
                    '''

                    sh '''
                        EC2_IP=$(cat infra/ansible/ec2_ip.txt)

                        echo "[app_servers]" > infra/ansible/inventory.ini
                        echo "ecommerce-server ansible_host=${EC2_IP} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/ecommerce-key.pem ansible_ssh_common_args='-o StrictHostKeyChecking=no'" >> infra/ansible/inventory.ini

                        cd infra/ansible
                        ansible-playbook -i inventory.ini site.yml
                    '''
                }
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    EC2_IP=$(cat infra/ansible/ec2_ip.txt)
                    sleep 10
                    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://${EC2_IP}:5000/health)
                    echo "Health check returned: $STATUS"
                    [ "$STATUS" = "200" ] && echo "PASS" || exit 1
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
        success {
            echo 'All stages passed!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
