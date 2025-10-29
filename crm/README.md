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
1. Trigger the Task Manually
Open a third terminal and execute the function directly for immediate log generation.

Bash

python manage.py shell
>>> from crm.tasks import generate_crm_report
>>> result = generate_crm_report()
>>> exit()
2. Verify Final Log Output
Check the contents of the final log file to confirm successful task execution.

Bash

cat /c/temp/crm_report_log.txt
Expected Output (Successful Verification): The file must contain a line in the correct format:

YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue
