📑 Project Documentation: Task Scheduling and AutomationThis project implements various task automation techniques in a Django/GraphQL CRM application, including system cron, django-crontab, and Celery Beat.🛠️ I. Global Setup and PrerequisitesActionCommandActivate Environmentsource venv/Scripts/activateInstall Dependenciespip install -r requirements.txtCreate Logging Dirmkdir -p /c/tempApply Migrationspython manage.py migrate🎯 II. Task-Specific Setup & Execution Guide0. & 1. System Cron Jobs (Tasks 0 & 1)Setup Command: Install the crontab entries for system scheduling.Bashcrontab crm/cron_jobs/customer_cleanup_crontab.txt
crontab crm/cron_jobs/order_reminders_crontab.txt
2. & 3. Django Crontab Jobs (Tasks 2 & 3)Setup Command: Add the jobs defined in the CRONJOBS setting to the system crontab.Bashpython manage.py crontab add
🚀 III. Task 4: Celery Report Generation (Celery Beat)1. Create Broker DirectoriesBashmkdir -p celery_queue/in celery_queue/out celery_queue/processed
2. Start the Celery Worker (Terminal 1) 🧑‍💻Bashpython -m celery -A crm worker -l info
3. Start Celery Beat Scheduler (Terminal 2) ⏰Bashpython -m celery -A crm beat -l info
4. VerificationExecute the task directly and check the log file.Bashpython manage.py shell
>>> from crm.tasks import generate_crm_report
>>> result = generate_crm_report()
>>> exit()
cat /c/temp/crm_report_log.txt
