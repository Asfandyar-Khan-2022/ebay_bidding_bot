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
driver.get("https://www.ebay.co.uk/itm/335075200126")
driver.implicitly_wait(10)

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

# THIS NEEDS FIXING
# Check if I am able to get the time hour and seconds
hour = int(end_time[1].split(":")[0])
if end_time[0] == "Today" and hour - dt.now().hour == 0:
    print(new_time())
else:
    i = 1
    while end_time[0].strip(", ") != (dt.now() + datetime.timedelta(i)).strftime("%A").strip(" "):
        i += 1
        date_now = (dt.now() + datetime.timedelta(i))

print(date_now)


driver.quit()
