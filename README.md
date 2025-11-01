# Project Documentation: Task Scheduling and Automation

This project implements various task automation techniques in a Django/GraphQL CRM application, including system cron, django-crontab, and Celery Beat.

---

### 🛠️ I. Global Setup and Prerequisites

| Action | Command |
| :--- | :--- |
| **Activate Environment** | `source venv/Scripts/activate` |
| **Install Dependencies** | `pip install -r requirements.txt` |
| **Create Logging Dir** | `mkdir -p /c/temp` |
| **Apply Migrations** | `python manage.py migrate` |

---

### 🎯 II. Task-Specific Setup & Execution Guide

#### 0. & 1. System Cron Jobs (Tasks 0 & 1)

**Setup Command:** Install the crontab entries for system scheduling.

```bash
crontab crm/cron_jobs/customer_cleanup_crontab.txt
crontab crm/cron_jobs/order_reminders_crontab.txt

python manage.py crontab add
mkdir -p celery_queue/in celery_queue/out celery_queue/processed
python -m celery -A crm worker -l info
python manage.py shell
>>> from crm.tasks import generate_crm_report
>>> result = generate_crm_report()
>>> exit()
cat /c/temp/crm_report_log.txt
