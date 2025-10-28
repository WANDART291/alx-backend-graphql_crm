import datetime
from django_cron import CronJobBase, Schedule

class HeartbeatCronJob(CronJobBase):
    RUN_EVERY_MINS = 5  # every 5 minutes
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'crm.heartbeat_cron'

    def do(self):
        now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        with open("crm_heartbeat_log.txt", "a") as f:
            f.write(f"{now} CRM is alive\n")
        print(f"{now} CRM is alive")


