from time import sleep
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime as dt
import datetime


def display(msg):
    print("Message: ", msg)

scheduler = BackgroundScheduler()
scheduler.add_job(display, "date", run_date = (dt.now() + datetime.timedelta(seconds=10)), args=["Job 1"])

scheduler.start()
# scheduler.remove_all_jobs()

sleep(1000)