# Celery and Celery Beat Setup for Weekly CRM Report

This module implements Task 4: **Configuring Celery and Celery Beat** to schedule a weekly CRM report generation and log the output to a file.

We use the **Filesystem (FS) Broker** for stability, as it avoids external service dependencies like Redis or RabbitMQ for this local project.

## 🚀 Setup and Installation

### 1. Prerequisites

Ensure your Python virtual environment is active. All necessary dependencies (Celery, django-celery-beat, etc.) are included in `requirements.txt`.

```bash
# If using Git Bash on Windows, run this in the project root:
source venv/Scripts/activate

# Install all dependencies
pip install -r requirements.txt
