# Task 0: Install Jenkins and Set Up a Pipeline

## Objective
The objective of this task is to install Jenkins in a Docker container and set up a basic CI pipeline. This pipeline will pull source code from a GitHub repository, install dependencies, run tests using `pytest`, and generate a test report.

## 1. Run Jenkins in a Docker Container

To start Jenkins, execute the following Docker command in your terminal:

```bash
docker run -d -v jenkins_home:/var/jenkins_home --name jenkins -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
```

This command will:
- `docker run -d`: Run the Jenkins container in detached mode (in the background).
- `-v jenkins_home:/var/jenkins_home`: Create a Docker volume named `jenkins_home` and mount it to `/var/jenkins_home` inside the container. This persists Jenkins data across container restarts.
- `--name jenkins`: Assign the name `jenkins` to the container.
- `-p 8080:8080`: Map port 8080 of the host to port 8080 of the container, allowing access to the Jenkins web UI.
- `-p 50000:50000`: Map port 50000 of the host to port 50000 of the container. This is used for Jenkins agent communication.
- `jenkins/jenkins:lts`: Use the official Long-Term Support (LTS) Jenkins image.

## 2. Initial Jenkins Setup and Configuration

1.  **Access Jenkins Dashboard**: Open your web browser and navigate to `http://localhost:8080`.
2.  **Unlock Jenkins**: Follow the instructions on the screen to unlock Jenkins. You will need to retrieve the initial admin password from the Jenkins container logs. You can get this by running:
    ```bash
    docker logs jenkins
    ```
    Look for a line similar to `Jenkins initial setup is required. An admin user has been created and a password generated.`.
3.  **Install Plugins**: When prompted, choose "Install suggested plugins." If you need to install them manually, ensure the following plugins are installed:
    *   **Git**
    *   **Pipeline**
    *   **ShiningPandaPlugin** (for Python integration) - *Note: Depending on Jenkins version, Python integration might be handled differently or not strictly require ShiningPandaPlugin. Ensure Python is available in your agent.*
4.  **Create Admin User**: After plugin installation, create an admin user.

## 3. Configure GitHub Credentials in Jenkins

1.  In Jenkins, go to `Manage Jenkins` > `Manage Credentials`.
2.  Click on `Jenkins` > `Global credentials (unrestricted)`.
3.  Click `Add Credentials`.
4.  Select `Username with password` for Kind.
5.  Enter your GitHub **Username** and a **Personal Access Token (PAT)** as the password. The PAT should have `repo` permissions. Generate one from your GitHub settings under `Developer settings` > `Personal access tokens`.
6.  Provide an **ID** (e.g., `github-credential`) and an optional **Description**.
7.  Click `Create`.

## 4. Create a Jenkins Pipeline Script (Jenkinsfile)

Create a `Jenkinsfile` in the root of your `messaging_app` repository (`alx-backend-python/messaging_app/Jenkinsfile`) with the following content:

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
        stage('Archive Test Results') {
            steps {
                archiveArtifacts artifacts: 'test-results.xml', fingerprint: true
            }
        }
    }
    post {
        always {
            // Clean up Docker container if it was started by Jenkins (optional)
            script {
                // Assuming the container might be named messaging_app_test or similar if spun up for tests
                // This is a placeholder and might need adjustment based on how the Docker agent is configured
                // to clean up after itself or how external services are managed.
                // For a Docker agent, Jenkins typically cleans up the container automatically after the job.
                // This block is more relevant if you were starting separate containers within stages.
                echo 'Cleaning up any potentially lingering Docker resources if needed...'
                // Example: sh "docker stop \$(docker ps -aq --filter ancestor=my_test_db_image || true)"
                // Example: sh "docker rm \$(docker ps -aq --filter ancestor=my_test_db_image || true)"
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

## 5. Configure Jenkins Job

1.  In Jenkins dashboard, click "New Item" or "New Job".
2.  Enter an item name (e.g., `MessagingApp-CI`) and select "Pipeline". Click "OK".
3.  In the job configuration page:
    *   Under the "Pipeline" section, select "Pipeline script from SCM".
    *   **SCM**: Choose `Git`.
    *   **Repository URL**: Enter the URL of your GitHub repository (e.g., `https://github.com/alx-backend-python/messaging_app.git`).
    *   **Credentials**: Select the GitHub credential you configured earlier (e.g., `github-credential`).
    *   **Branches to build**: `*/main` (or the branch you want to build from).
    *   **Script Path**: Enter `messaging_app/Jenkinsfile` (or the path to your Jenkinsfile within the repository).
4.  Click "Save".

## 6. Trigger the Pipeline

1.  On the job's page, click "Build Now" to manually trigger the pipeline.
2.  Monitor the "Console Output" of the build to see the progress and verify that the tests run successfully and the report is generated.

This completes the setup for automated testing with Jenkins.
