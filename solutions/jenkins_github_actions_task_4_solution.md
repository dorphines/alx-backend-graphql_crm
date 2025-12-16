# Task 4: Build and Push Docker Image using GitHub Actions

## Objective
The objective of this task is to create a new GitHub Actions workflow that automates the process of building a Docker image for the Django messaging application and pushing it to Docker Hub. This workflow will leverage GitHub Secrets for secure credential management.

## 1. Create GitHub Actions Workflow File

Create a file named `dep.yml` in the `.github/workflows/` directory of your `messaging_app` repository (`alx-backend-python/messaging_app/.github/workflows/dep.yml`) with the following content:

```yaml
name: Deploy Docker Image to Docker Hub

on:
  push:
    branches:
      - main # Trigger on push to the main branch
  workflow_dispatch: # Allows manual triggering from the GitHub UI

jobs:
  build_and_push:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout Repository
      uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Log in to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and Push Docker image
      uses: docker/build-push-action@v5
      with:
        context: ./messaging_app # Assuming your Dockerfile is in the messaging_app directory relative to the repo root
        push: true
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/messaging_app:latest
          ${{ secrets.DOCKER_USERNAME }}/messaging_app:${{ github.run_number }}
```

## 2. Explanation of the Workflow

*   **`name: Deploy Docker Image to Docker Hub`**: The name of the GitHub Actions workflow.
*   **`on: push` and `on: workflow_dispatch`**:
    *   `push`: The workflow will automatically trigger when changes are pushed to the `main` branch.
    *   `workflow_dispatch`: This allows you to manually trigger the workflow from the "Actions" tab in your GitHub repository, which is useful for controlled deployments.
*   **`jobs: build_and_push`**: Defines a single job for building and pushing the Docker image.
    *   **`runs-on: ubuntu-latest`**: Specifies that the job will run on the latest Ubuntu runner.
    *   **`Checkout Repository`**: Checks out your repository code.
    *   **`Set up Docker Buildx`**: Sets up Docker Buildx, which provides enhanced build capabilities.
    *   **`Log in to Docker Hub`**:
        *   Uses the `docker/login-action@v3` action to log in to Docker Hub.
        *   `username: ${{ secrets.DOCKER_USERNAME }}`: Retrieves the Docker Hub username from GitHub Secrets.
        *   `password: ${{ secrets.DOCKER_PASSWORD }}`: Retrieves the Docker Hub password (or Personal Access Token) from GitHub Secrets.
    *   **`Build and Push Docker image`**:
        *   Uses the `docker/build-push-action@v5` action to build and push the Docker image.
        *   `context: ./messaging_app`: Specifies the build context for the Docker image. **Ensure this path correctly points to the directory containing your `Dockerfile` and Django project.** In this case, it's relative to the `alx-backend-python` repository root.
        *   `push: true`: Instructs the action to push the built image to Docker Hub.
        *   `tags`: Defines the tags for the Docker image.
            *   `${{ secrets.DOCKER_USERNAME }}/messaging_app:latest`: Tags the image as `latest`.
            *   `${{ secrets.DOCKER_USERNAME }}/messaging_app:${{ github.run_number }}`: Tags the image with the GitHub Actions run number, providing a unique version for each build.

## 3. Configure GitHub Secrets

For secure authentication with Docker Hub, you need to create two secrets in your GitHub repository:

1.  In your GitHub repository, go to `Settings` > `Secrets and variables` > `Actions`.
2.  Click `New repository secret`.
3.  Create two new secrets:
    *   `DOCKER_USERNAME`: Enter your Docker Hub username.
    *   `DOCKER_PASSWORD`: Enter your Docker Hub password or a Personal Access Token (PAT) with push permissions. Using a PAT is recommended for security.

## 4. Commit and Push

Commit the `dep.yml` file to your `alx-backend-python/messaging_app` repository and push it to GitHub. The workflow will automatically trigger on pushes to `main`, or you can manually trigger it from the GitHub Actions UI.

This completes setting up the GitHub Actions workflow for building and pushing Docker images.