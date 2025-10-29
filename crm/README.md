## 🚀 Task 4: Celery Beat Setup for Weekly CRM Report

This guide details the setup and verification of the Celery task responsible for generating the **weekly CRM report**.

**Objective:** Schedule crm.tasks.generate_crm_report to run every Monday at 6:00 AM.

---

### ⚙️ I. Configuration and Environment Setup

This configuration uses the stable **Filesystem (FS) Broker** to avoid external dependencies (like Redis/RabbitMQ) for local development.

1.  **Prepare Environment & Install Packages**

    ```bash
    source venv/Scripts/activate
    pip install -r requirements.txt
    ```

2.  **Create Broker and Log Directories**

    ```bash
    # Directories for the Filesystem Broker queue
    mkdir -p celery_queue/in celery_queue/out celery_queue/processed

    # Directory for the task log (Maps to C:\temp on Windows Git Bash)
    mkdir -p /c/temp 
    ```

3.  **Run Migrations**

    ```bash
    python manage.py migrate
    ```

---

### 💻 II. Running the Celery Services

You must run the **Worker** and **Beat Scheduler** concurrently in separate terminals (Git Bash, with (venv) active).

#### 1. Start the Celery Worker (Terminal 1) 🧑‍💻
The **Worker** executes the tasks. Keep this terminal running.

```bash
python -m celery -A crm worker -l info
