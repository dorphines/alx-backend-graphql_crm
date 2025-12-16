# Task 3: Code Quality Checks in GitHub Actions

## Objective
This task extends the existing GitHub Actions workflow (`.github/workflows/ci.yml`) to incorporate code quality checks, specifically `flake8` for linting and code coverage reporting. The build will fail if linting errors are found.

## 1. Update the GitHub Actions Workflow File

Modify your `ci.yml` file (located at `alx-backend-python/messaging_app/.github/workflows/ci.yml`) with the following changes. The new steps will be added after installing dependencies and before running tests.

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

    - name: Install dependencies and linters
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install mysqlclient flake8 coverage pytest-cov # Add flake8, coverage, and pytest-cov

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

    - name: Run Flake8 Linting
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      # The above flake8 commands will make the job fail if errors are detected.
      # You can adjust the --exit-zero flag to fail the build based on your preference.
      # By default, flake8 exits with 1 if there are errors, causing the step to fail.

    - name: Run Tests with Coverage
      run: |
        pytest --junitxml=test-results.xml --cov=. --cov-report=xml --cov-report=html
      env:
        DJANGO_SETTINGS_MODULE: messaging_app.settings
        DATABASE_URL: mysql://test_user:${{ secrets.MYSQL_PASSWORD }}@127.00.1:3306/test_db

    - name: Upload Test Results and Coverage Report
      uses: actions/upload-artifact@v4
      with:
        name: test-and-coverage-reports
        path: |
          test-results.xml
          htmlcov/ # Path to HTML coverage report directory
          .coverage.xml # Path to XML coverage report

```

## 2. Explanation of Changes

*   **`Install dependencies and linters`**:
    *   `pip install flake8 coverage pytest-cov`: These packages are added to the dependency installation step. `flake8` is the linter, `coverage` is used for collecting coverage data, and `pytest-cov` is a `pytest` plugin for integrating coverage reporting.
*   **`Run Flake8 Linting`**:
    *   `flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`: Runs `flake8` on all Python files in the current directory.
        *   `--select=E9,F63,F7,F82`: Selects specific error codes to report (common critical errors).
        *   `--show-source`: Shows the source code of the line where the error occurred.
        *   `--statistics`: Shows a count of each error type.
    *   `flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics`: A second `flake8` command. The `--exit-zero` flag allows `flake8` to output warnings but still exit with a zero status code, preventing the step from failing immediately due to warnings. You can remove `--exit-zero` if you want the build to fail on any linting warning.
*   **`Run Tests with Coverage`**:
    *   `pytest --junitxml=test-results.xml --cov=. --cov-report=xml --cov-report=html`: This command runs `pytest` and integrates `coverage.py`.
        *   `--cov=.`: Collects coverage data for the current directory.
        *   `--cov-report=xml`: Generates a coverage report in XML format (e.g., `.coverage.xml`), which is useful for CI/CD tools.
        *   `--cov-report=html`: Generates a human-readable HTML coverage report (in the `htmlcov/` directory).
*   **`Upload Test Results and Coverage Report`**:
    *   The `path` now includes `htmlcov/` and `.coverage.xml` to upload both the HTML and XML coverage reports alongside the JUnit XML test results.

## 3. Configure GitHub Secrets

Ensure you have the `MYSQL_ROOT_PASSWORD` and `MYSQL_PASSWORD` secrets configured in your GitHub repository as described in Task 2.

## 4. Commit and Push

Commit the updated `ci.yml` file to your `alx-backend-python/messaging_app` repository and push it to GitHub. The workflow will automatically trigger, running your tests with linting and coverage checks.

This completes adding code quality checks to your GitHub Actions workflow.