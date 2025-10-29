Here is the complete and consolidated setup guide for Task 4: Celery Task for Generating CRM Reports, presented on one page with the necessary steps for your successful submission.

📄 Final Project Setup: Celery Task (Task 4)
This guide covers the necessary steps to set up and verify the Celery Worker and Celery Beat Scheduler using the stable Filesystem (FS) Broker configuration.

🛠️ I. Configuration and Environment Setup
This configuration bypasses the complex installation of Redis and avoids the django_celery_results conflict.

Install Dependencies: Ensure your virtual environment is active and all packages are installed.

Bash

source venv/Scripts/activate
pip install -r requirements.txt
Create Broker and Log Directories: The Filesystem Broker and the task itself require specific directories to exist.

Bash

# Directories for the Filesystem Broker queue
mkdir -p celery_queue/in celery_queue/out celery_queue/processed

# Directory for the task output log (Windows compatibility)
mkdir -p /c/temp 
Run Migrations: Apply migrations for django-celery-beat.

Bash

python manage.py migrate
🚀 II. Running the Celery Services
You must run the Worker and Beat Scheduler simultaneously in two separate terminals (Git Bash, with (venv) active).

1. Start the Celery Worker (Terminal 1)
This process executes the tasks. It must be running for any task to start.

Bash

python -m celery -A crm worker -l info
(Expected: Worker connects to filesystem://localhost// and shows celery@DESKTOP-LD3S0N6 ready.)

2. Start Celery Beat Scheduler (Terminal 2)
This process reads the schedule (settings.py) and places the task onto the queue every Monday at 6:00 AM.

Bash

python -m celery -A crm beat -l info
✅ III. Verification of Task Output
To prove the task logic is correct and working, we manually execute the function and check the final log file output.

1. Trigger the Task (Terminal 3)
Open a third terminal and execute the function directly.

Bash

python manage.py shell
>>> from crm.tasks import generate_crm_report
>>> result = generate_crm_report()
>>> exit()
2. Check the Log File (Final Project Requirement)
The task must have successfully written the report to the absolute path.

Bash

cat /c/temp/crm_report_log.txt
Expected Output (Successful Verification):

YYYY-MM-DD HH:MM:SS - Report: 1250 customers, 450 orders, 52345.89 revenue
💾 IV. Final Submission
Stop all services (Ctrl+C in Terminal 1 & 2).

Commit and Push your verified code to your repository:

Bash

git add . 
git commit -m "feat: FINAL SUBMISSION - Completed Celery Beat Task 4 and verified log file output."
git push origin main
