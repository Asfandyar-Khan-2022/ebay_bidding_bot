import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import sched
from datetime import datetime as dt
import datetime

options = Options()
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=C:\\Users\\a_asf\\AppData\\Local\\Google\\Chrome\\User Data\\")

# Open link to item
driver = uc.Chrome(executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", options=options)
driver.get("https://www.ebay.co.uk/itm/166373384542")
driver.implicitly_wait(3)

# Get bid end time left 
bid_end_time_left = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[1]/div[3]/span[2]/span/span[1]')
current_time = bid_end_time_left.text

def new_time():
    while True:
        new_time = bid_end_time_left.text
        if new_time != current_time:
            return new_time

# Get bid end time 
bid_end_time = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[1]/div[3]/span[2]/span/span[3]')
end_time = bid_end_time.text.split()

# Check if I am able to get the time hour and seconds
hour = int(end_time[1].split(":")[0])
if end_time[0] == "Today" and hour - dt.now().hour == 0:
    minutes_seconds = new_time().split(" ")
    if len(minutes_seconds) == 2:
        set_minutes = int(minutes_seconds[0].strip("m"))
        set_seconds = int(minutes_seconds[1].strip("s"))
        date_now = (dt.now().replace(microsecond=0)) + datetime.timedelta(minutes=set_minutes, seconds=set_seconds)
    else:
        set_seconds = int(minutes_seconds[0].strip("s"))
        date_now = (dt.now().replace(microsecond=0)) + datetime.timedelta(seconds=set_seconds) 

elif end_time[0] == "Today" and hour - dt.now().hour != 0:
    date_now = dt.now()
    set_hour = int(end_time[1].split(":")[0])
    set_minutes = int(end_time[1].split(":")[1])
    date_now = date_now.replace(hour=set_hour, minute=set_minutes, second=0, microsecond=0)

elif "/" in end_time[0]:
    date = end_time[0].split("/")
    set_month = int(date[1].rstrip(", "))
    set_day = int(date[0])
    set_hour = int(end_time[1].split(":")[0])
    set_minutes = int(end_time[1].split(":")[1])
    date_now = dt.now().replace(month=set_month, day=set_day, hour=set_hour, minute=set_minutes, second=0, microsecond=0)

else:
    i = 0
    while end_time[0].strip(", ") != (dt.now() + datetime.timedelta(i)).strftime("%A").strip(" "):
        i += 1
        set_hour = int(end_time[1].split(":")[0])
        print(set_hour)
        set_minutes = int(end_time[1].split(":")[1])
        date_now = (dt.now() + datetime.timedelta(i))
        date_now = date_now.replace(hour=set_hour, minute=set_minutes, second=0, microsecond=0)

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds

minute_minute_before_bid = date_now - datetime.timedelta(minutes=1)
print(minute_minute_before_bid)

def task():
    print("i am a task")

scheduler = sched.scheduler(time.time, time.sleep)
scheduler.enterabs(minute_minute_before_bid.timestamp(), 1, task)
scheduler.run()
driver.quit()
