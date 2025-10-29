Project Documentation: Task Scheduling and Automation
This project implements various task automation techniques in a Django/GraphQL CRM application, including system cron, django-crontab, and Celery Beat.

🛠️ I. Global Setup and Prerequisites
Activate Environment & Install Packages

Bash

source venv/Scripts/activate
pip install -r requirements.txt
Prepare Global Logging Directory

Bash

mkdir -p /c/temp
Run Migrations

Bash

python manage.py migrate
🎯 II. Task-Specific Setup & Execution
0. Customer Cleanup Script (System Cron)
Objective: Schedule a shell script to delete inactive customers every Sunday at 2:00 AM.

Setup Command: Install the crontab entry for system scheduling.

Bash

crontab crm/cron_jobs/customer_cleanup_crontab.txt
Verification: Check log file /tmp/customer_cleanup_log.txt.

1. Order Reminder Script (System Cron)
Objective: Schedule a Python script to send order reminders daily at 8:00 AM via GraphQL query.

Setup Command: Install the crontab entry for system scheduling.

Bash

crontab crm/cron_jobs/order_reminders_crontab.txt
Verification: Check log file /tmp/order_reminders_log.txt.

2. & 3. Heartbeat & Stock Alerts (django-crontab)
Objective: Implement jobs for heartbeat logging and GraphQL mutation for restocking.

Setup Command: Add the tasks defined in CRONJOBS within settings.py to the system crontab.

Bash

python manage.py crontab add
Verification: Check logs /tmp/crm_heartbeat_log.txt and /tmp/low_stock_updates_log.txt.

🚀 Task 4: Celery Beat Setup for Weekly CRM Report
This guide details the setup and verification of the Celery task responsible for generating the weekly CRM report.

Objective: Schedule crm.tasks.generate_crm_report to run every Monday at 6:00 AM.

⚙️ I. Configuration and Environment Setup
This configuration uses the stable Filesystem (FS) Broker to avoid external dependencies (like Redis/RabbitMQ) for local development.

Prepare Environment & Install Packages

Bash

source venv/Scripts/activate
pip install -r requirements.txt
Create Broker and Log Directories

Bash

# Directories for the Filesystem Broker queue
mkdir -p celery_queue/in celery_queue/out celery_queue/processed

# Directory for the task log (Maps to C:\temp on Windows Git Bash)
mkdir -p /c/temp 
Run Migrations

Bash

python manage.py migrate
💻 II. Running the Celery Services
You must run the Worker and Beat Scheduler concurrently in separate terminals (Git Bash, with (venv) active).

1. Start the Celery Worker (Terminal 1) 🧑‍💻
The Worker executes the tasks. Keep this terminal running.

Bash

python -m celery -A crm worker -l info
2. Start Celery Beat Scheduler (Terminal 2) ⏰
The Beat Scheduler handles the timing and placement of the recurring task onto the queue.

Bash

python -m celery -A crm beat -l info
✅ III. Verification and Project Completion
Trigger the Task Manually

Bash

python manage.py shell
>>> from crm.tasks import generate_crm_report
>>> result = generate_crm_report()
>>> exit()
Verify Final Log Output

Bash

cat /c/temp/crm_report_log.txt
Expected Output (Successful Verification): The file must contain a line in the correct format:

YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue
