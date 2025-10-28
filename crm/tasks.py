# crm/tasks.py
from background_task import background
import datetime

@background(schedule=60)  # run 60 seconds later
def heartbeat_task():
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    with open("crm_heartbeat_log.txt", "a") as f:
        f.write(f"{now} CRM is alive\n")
    print(f"{now} CRM heartbeat logged")
