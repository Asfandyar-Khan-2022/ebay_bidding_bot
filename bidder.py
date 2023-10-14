import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import sched
from datetime import datetime


# options = Options()

# options.add_argument("--profile-directory=Default")

# options.add_argument("--user-data-dir=C:\\Users\\a_asf\\AppData\\Local\\Google\\Chrome\\User Data\\")

# driver = uc.Chrome(executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe", options=options)

# driver.get("https://www.ebay.co.uk/itm/394928895804")
# driver.implicitly_wait(10)

# bid = driver.find_element(By.XPATH, '//*[@id="bidBtn_btn"]')
# bid.click()

# place_bid = driver.find_element(By.XPATH, '//*[@id="s0-0-1-1-3-placebid-section-offer-section-price-10-textbox"]')
# place_bid.send_keys("0.3")

# review_bid = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[2]/div[1]/div[2]/div/div[2]/div[3]/section[1]/div/marko-destroy-when-detached/div/div/div[1]/div[3]/div/div/span/div/div/div/button')
# review_bid.click()

# confirm_bid = driver.find_element(By.XPATH, '//*[@id="confirmBid"]')

def task():
    print("TEST")

s = sched.scheduler(time.time, time.sleep)
s.enterabs(datetime(2023, 10, 14, 6, 42, 0, 0).timestamp(), 1, task)
s.run()

# time.sleep(100)

