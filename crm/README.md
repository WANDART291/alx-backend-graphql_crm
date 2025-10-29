# Celery and Celery Beat Setup for CRM Report Generation

This document outlines the steps to install and run the components for the weekly CRM report generation task.

## Prerequisites

1.  **Redis Server:** Celery requires a message broker. Ensure a Redis server is running and accessible at `localhost:6379`.

## Running the Application

### 1. Run Migrations

Apply the database migrations, which include tables needed for `django-celery-beat`.

```bash
python manage.py migrate