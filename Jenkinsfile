pipeline {
    agent any
    options { timestamps(); disableConcurrentBuilds() }
    environment {
        // Replace with your Docker Hub username/repository.
        IMAGE_NAME = 'YOUR_DOCKERHUB_USERNAME/cca2-student-task-manager'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm; sh 'git rev-parse --short HEAD' }
        }
        stage('Build and Test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements-dev.txt
                    pytest -q
                '''
            }
        }
        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t "$IMAGE_NAME:$BUILD_NUMBER" .
                    docker tag "$IMAGE_NAME:$BUILD_NUMBER" "$IMAGE_NAME:latest"
                '''
            }
        }
        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    sh '''
                        echo "$DOCKERHUB_TOKEN" | docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker push "$IMAGE_NAME:$BUILD_NUMBER"
                        docker push "$IMAGE_NAME:latest"
                        docker logout
                    '''
                }
            }
        }
        stage('Deploy to Minikube') {
            steps {
                sh '''
                    sed "s|IMAGE_PLACEHOLDER|$IMAGE_NAME:$BUILD_NUMBER|g" k8s/deployment.yaml > k8s/deployment.rendered.yaml
                    kubectl apply -f k8s/deployment.rendered.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl rollout status deployment/cca2-student-task-manager --timeout=180s
                    kubectl get pods,deployments,services
                '''
            }
        }
    }
    post {
        always { sh 'rm -f k8s/deployment.rendered.yaml' }
        success { echo 'CI/CD pipeline completed successfully.' }
        failure { echo 'Pipeline failed. Review the stage console output.' }
    }
}
