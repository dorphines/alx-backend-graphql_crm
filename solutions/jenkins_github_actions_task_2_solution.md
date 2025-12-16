# Task 2: Set Up a GitHub Actions Workflow for Testing

## Objective
The goal of this task is to configure a GitHub Actions workflow that automatically runs tests for the Django messaging application on every code push and pull request. This workflow will also include setting up a MySQL database service for the tests.

## 1. Create GitHub Actions Workflow File

Create a file named `ci.yml` in the `.github/workflows/` directory of your `messaging_app` repository (`alx-backend-python/messaging_app/.github/workflows/ci.yml`) with the following content:

```yaml
name: Django CI

on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main
      - develop

jobs:
  build:
    runs-on: ubuntu-latest

    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: ${{ secrets.MYSQL_ROOT_PASSWORD }}
          MYSQL_DATABASE: test_db
          MYSQL_USER: test_user
          MYSQL_PASSWORD: ${{ secrets.MYSQL_PASSWORD }}
        ports:
          - 3306:3306
        options: --health-cmd="mysqladmin ping --silent" --health-interval=10s --health-timeout=5s --health-retries=10

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        # Install mysqlclient for database interaction
        pip install mysqlclient

    - name: Wait for MySQL to be ready
      run: |
        sudo apt-get update
        sudo apt-get install -y default-mysql-client
        for i in $(seq 1 10); do
          mysql -h 127.0.0.1 -u test_user -p${{ secrets.MYSQL_PASSWORD }} test_db -e "SELECT 1" && break
          echo "Waiting for MySQL to start..."
          sleep 5
        done

    - name: Run Migrations
      run: |
        python manage.py migrate
      env:
        DJANGO_SETTINGS_MODULE: messaging_app.settings
        DATABASE_URL: mysql://test_user:${{ secrets.MYSQL_PASSWORD }}@127.0.0.1:3306/test_db

    - name: Run Tests
      run: |
        pytest --junitxml=test-results.xml
      env:
        DJANGO_SETTINGS_MODULE: messaging_app.settings
        DATABASE_URL: mysql://test_user:${{ secrets.MYSQL_PASSWORD }}@127.0.0.1:3306/test_db

    - name: Upload test results
      uses: actions/upload-artifact@v4
      with:
        name: test-results
        path: test-results.xml
```

## 2. Explanation of the Workflow

*   **`name: Django CI`**: The name of your GitHub Actions workflow.
*   **`on: push` and `on: pull_request`**: Defines when the workflow should run. It will trigger on pushes and pull requests to the `main` and `develop` branches.
*   **`jobs: build`**: Defines a single job named `build`.
    *   **`runs-on: ubuntu-latest`**: Specifies that the job will run on the latest Ubuntu runner.
    *   **`services: mysql`**: This block sets up a MySQL 8.0 Docker container as a service.
        *   `env`: Environment variables for the MySQL container, including root password, database name, user, and password. These should be stored as GitHub Secrets for security (e.g., `MYSQL_ROOT_PASSWORD`, `MYSQL_PASSWORD`).
        *   `ports: - 3306:3306`: Maps the container's MySQL port to the host.
        *   `options`: Health check options to ensure MySQL is fully started before tests run.
    *   **`steps`**:
        *   **`actions/checkout@v4`**: Checks out your repository code.
        *   **`actions/setup-python@v5`**: Sets up the Python environment (version 3.9).
        *   **`Install dependencies`**: Installs Python packages from `requirements.txt` and `mysqlclient` which is needed for Django to connect to MySQL.
        *   **`Wait for MySQL to be ready`**: A loop that attempts to connect to the MySQL database until it's ready. This is crucial as the MySQL service might take a moment to start up.
        *   **`Run Migrations`**: Applies Django database migrations. The `env` block sets the Django settings module and the database connection string.
        *   **`Run Tests`**: Executes `pytest` to run tests. `--junitxml=test-results.xml` generates a JUnit XML report for test results tracking.
        *   **`actions/upload-artifact@v4`**: Uploads the `test-results.xml` file as a build artifact, making it viewable in the GitHub Actions UI.

## 3. Configure GitHub Secrets

For security, the MySQL passwords should be stored as GitHub Secrets:

1.  In your GitHub repository, go to `Settings` > `Secrets and variables` > `Actions`.
2.  Click `New repository secret`.
3.  Create two new secrets:
    *   `MYSQL_ROOT_PASSWORD`: Enter a strong password for the MySQL root user.
    *   `MYSQL_PASSWORD`: Enter a strong password for the `test_user`.

## 4. Commit and Push

Commit the `ci.yml` file to your `alx-backend-python/messaging_app` repository and push it to GitHub. The workflow will automatically trigger on your next push or any new pull request, running your Django tests against a MySQL database.

This completes setting up the GitHub Actions workflow for testing.