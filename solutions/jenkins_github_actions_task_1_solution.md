# Task 1: Build Docker Image with Jenkins

## Objective
This task extends the Jenkins CI pipeline to build a Docker image for the Django messaging application and push it to Docker Hub.

## 1. Configure Docker Hub Credentials in Jenkins

Before proceeding, you need to add your Docker Hub credentials to Jenkins.

1.  In Jenkins, navigate to `Manage Jenkins` > `Manage Credentials`.
2.  Click on `Jenkins` > `Global credentials (unrestricted)`.
3.  Click `Add Credentials`.
4.  Select `Username with password` for Kind.
5.  Enter your Docker Hub **Username** and **Password**.
6.  Provide an **ID** (e.g., `docker-hub-credentials`) and an optional **Description**.
7.  Click `Create`.

## 2. Update the Jenkins Pipeline Script (Jenkinsfile)

Modify your `Jenkinsfile` (located at `alx-backend-python/messaging_app/Jenkinsfile`) to include new stages for building and pushing the Docker image.

**Important**: Replace `your_dockerhub_username` with your actual Docker Hub username in the `Jenkinsfile` content below.

```groovy
pipeline {
    agent {
        docker {
            image 'python:3.9-slim-buster' // Use a Python image as the agent
            args '-u 0:0' // Run as root to avoid permission issues during setup
        }
    }
    environment {
        // Set Python executable path if not in default PATH
        PYTHON_PATH = '/usr/local/bin/python'
        PATH = "${PYTHON_PATH}:${PATH}"
        DJANGO_SETTINGS_MODULE = 'messaging_app.settings' // Assuming your Django project is named messaging_app
        DATABASE_URL = 'sqlite:///db.sqlite3' // Use SQLite for simplicity in CI, or configure for MySQL
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials') // Jenkins credential ID for Docker Hub
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', credentialsId: 'github-credential', url: 'https://github.com/alx-backend-python/messaging_app.git' // Replace with your actual repo URL if different
            }
        }
        stage('Install Dependencies') {
            steps {
                script {
                    sh 'pip install --no-cache-dir -r requirements.txt'
                }
            }
        }
        stage('Run Migrations') {
            steps {
                script {
                    sh 'python manage.py migrate'
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    sh 'pytest --junitxml=test-results.xml'
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh "docker build -t your_dockerhub_username/messaging_app:${env.BUILD_NUMBER} ."
                    // Tag the image as 'latest'
                    sh "docker tag your_dockerhub_username/messaging_app:${env.BUILD_NUMBER} your_dockerhub_username/messaging_app:latest"
                }
            }
        }
        stage('Push Docker Image') {
            steps {
                script {
                    // Login to Docker Hub
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo \"$DOCKER_PASS\" | docker login -u \"$DOCKER_USER\" --password-stdin"
                        // Push the tagged images
                        sh "docker push your_dockerhub_username/messaging_app:${env.BUILD_NUMBER}"
                        sh "docker push your_dockerhub_username/messaging_app:latest"
                    }
                }
            }
        }
        stage('Archive Test Results') {
            steps {
                archiveArtifacts artifacts: 'test-results.xml', fingerprint: true
            }
        }
    }
    post {
        always {
            script {
                echo 'Cleaning up any potentially lingering Docker resources if needed...'
                // Clean up the Docker image locally to save space
                sh "docker rmi your_dockerhub_username/messaging_app:${env.BUILD_NUMBER} || true"
                sh "docker rmi your_dockerhub_username/messaging_app:latest || true"
            }
        }
        success {
            echo 'Pipeline finished successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
```

## 3. Trigger the Jenkins Pipeline

1.  After updating the `Jenkinsfile` in your GitHub repository, commit and push the changes.
2.  In the Jenkins dashboard, navigate to your job (`MessagingApp-CI`).
3.  Click "Build Now" to manually trigger a new build.

## 4. Monitor Build Logs

Monitor the "Console Output" of the build. You should see output indicating:
*   The pipeline checking out the code.
*   Dependencies being installed.
*   Tests running.
*   The Docker image being built.
*   Successful login to Docker Hub.
*   The Docker images being pushed to Docker Hub.

Verify that the build completes successfully and that the Docker images are visible in your Docker Hub repository.

This completes the setup for building and pushing Docker images with Jenkins.
