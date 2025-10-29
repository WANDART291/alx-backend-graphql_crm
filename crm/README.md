📑 Project Documentation: Task Scheduling and AutomationThis project implements various task automation techniques in a Django/GraphQL CRM application, including system cron, django-crontab, and Celery Beat.🛠️ I. Global Setup and PrerequisitesCommandDescriptionsource venv/Scripts/activateActivate the Python virtual environment.pip install -r requirements.txtInstall all necessary dependencies (Celery, django-crontab, etc.).mkdir -p /c/tempCreate the global logging directory (/tmp) for Windows stability.python manage.py migrateApply migrations for all scheduler apps.chmod +x crm/cron_jobs/*.shGrant execution permissions to shell scripts.🎯 II. Task-Specific Setup & Execution Guide0. & 1. System Cron Jobs (Scripts: Tasks 0 & 1)These tasks use Linux-native scheduling (crontab) to run scripts directly.TaskObjectiveCrontab File0Cleanup Inactive Customerscrm/cron_jobs/customer_cleanup_crontab.txt1Send GraphQL Order Reminderscrm/cron_jobs/order_reminders_crontab.txtSetup Command: Install the crontab entries.Bashcrontab crm/cron_jobs/customer_cleanup_crontab.txt
crontab crm/cron_jobs/order_reminders_crontab.txt
2. & 3. Django Crontab Jobs (Tasks 2 & 3)These tasks use django-crontab to register Python functions (crm/cron.py) with the system scheduler.Setup Command: Add the jobs defined in the CRONJOBS setting to the system crontab.Bashpython manage.py crontab add
🚀 III. Task 4: Celery Report Generation (Celery Beat)This task uses the Filesystem (FS) Broker for local stability, as configured in crm/settings.py.1. Create Broker DirectoriesThe FS Broker requires specific directories to function as the queue.Bashmkdir -p celery_queue/in celery_queue/out celery_queue/processed
2. Start the Celery Worker (Terminal 1) 🧑‍💻The Worker executes the tasks. Keep this terminal running.Bashpython -m celery -A crm worker -l info
3. Start Celery Beat Scheduler (Terminal 2) ⏰The Beat Scheduler places the weekly report task onto the queue. Run this in a separate terminal.Bashpython -m celery -A crm beat -l info
4. VerificationTo verify the task logic and required log output:Bash# Execute the task function directly
python manage.py shell
>>> from crm.tasks import generate_crm_report
>>> result = generate_crm_report()
>>> exit()

# Check the final log output
cat /c/temp/crm_report_log.txt
