# CRM Reporting with Celery

This module includes a Celery task to generate weekly CRM reports.

## Setup

1.  **Install Redis and Dependencies:**
    Ensure Redis is installed and running on your system (default `localhost:6379`).
    Install the Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run Migrations:**
    Apply database migrations for `django-celery-beat`:
    ```bash
    python manage.py migrate
    ```

3.  **Start Celery Worker:**
    Run the worker to process tasks:
    ```bash
    celery -A crm worker -l info
    ```

4.  **Start Celery Beat:**
    Run the beat scheduler to trigger periodic tasks:
    ```bash
    celery -A crm beat -l info
    ```

5.  **Verify Logs:**
    The report will be logged to `/tmp/crm_report_log.txt`.
    You can check it with:
    ```bash
    cat /tmp/crm_report_log.txt
    ```
