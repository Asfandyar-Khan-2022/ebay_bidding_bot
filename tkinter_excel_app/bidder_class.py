import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
import sched
from datetime import datetime as dt
import datetime

options = Options()
class EbayBidding:
    def __init__(
            self, chrome_user, 
            chrome_user_path,
            chrome_exe, 
            ebay_item_number, 
            seconds_before_bid = 5):
        self.chrome_user = chrome_user
        self.chrome_user_path = chrome_user_path
        self.chrome_exe = chrome_exe
        self.ebay_item_number = ebay_item_number
        self.seconds_before_bid = seconds_before_bid
    
    def set_chrome_user_and_path(self):
        options.add_argument(f"--profile-directory={self.chrome_user}")
        options.add_argument(f"--user-data-dir={self.chrome_user_path}")
    
    def open_link_to_item(self):
        self.driver = uc.Chrome(executable_path=self.chrome_exe, options=options)
        self.driver.get(f"https://www.ebay.co.uk/itm/{self.ebay_item_number}")
        self.driver.implicitly_wait(3)

    def bid_end_time_left(self):
        self.bid_end_time_left = self.driver.find_element(
            By.XPATH,
            '//*[@id="mainContent"]/div[1]/div[3]/span[2]/span/span[1]')
        self.current_time = self.bid_end_time_left.text
    
    def new_time(self):
        while True:
            new_time = self.bid_end_time_left.text
            if new_time != self.current_time:
                return new_time
    
    def bid_end_time(self):
        bid_end_time = self.driver.find_element(
            By.XPATH, 
            '//*[@id="mainContent"]/div[1]/div[3]/span[2]/span/span[3]')
        self.end_time = bid_end_time.text.split()
    
    def bid_time_when_seconds_visible(self):
        self.hour = int(self.end_time[1].split(":")[0])
        if self.end_time[0] == "Today" and self.hour - dt.now().hour == 0:
            minutes_seconds = self.new_time().split(" ")
            if len(minutes_seconds) == 2:
                set_minutes = int(minutes_seconds[0].strip("m"))
                set_seconds = int(minutes_seconds[1].strip("s"))
                self.date_now = (dt.now().replace(microsecond=0)) + datetime.timedelta(minutes=set_minutes, seconds=set_seconds)
            else:
                set_seconds = int(minutes_seconds[0].strip("s"))
                self.date_now = (dt.now().replace(microsecond=0)) + datetime.timedelta(seconds=set_seconds) 

    def bid_hours_and_minutes_same_day(self):
        if self.end_time[0] == "Today" and self.hour - dt.now().hour != 0:
            date_now = dt.now()
            set_hour = int(self.end_time[1].split(":")[0])
            set_minutes = int(self.end_time[1].split(":")[1])
            self.date_now = date_now.replace(hour=set_hour, minute=set_minutes, second=0, microsecond=0)
        
    def bid_hours_and_minutes_more_than_week(self):
            if "/" in self.end_time[0]:
                date = self.end_time[0].split("/")
                set_month = int(date[1].rstrip(", "))
                set_day = int(date[0])
                set_hour = int(self.end_time[1].split(":")[0])
                set_minutes = int(self.end_time[1].split(":")[1])
                self.date_now = dt.now().replace(
                    month=set_month,
                    day=set_day,
                    hour=set_hour,
                    minute=set_minutes,
                    second=0,
                    microsecond=0)

    def bid_hours_and_minutes_within_week(self):
            if "/" not in self.end_time[0] and self.end_time[0] != "Today":
                i = 0
                while self.end_time[0].strip(", ") != (dt.now() + datetime.timedelta(i)).strftime("%A").strip(" "):
                    i += 1
                    set_hour = int(self.end_time[1].split(":")[0])
                    set_minutes = int(self.end_time[1].split(":")[1])
                    date_now = (dt.now() + datetime.timedelta(i))
                    self.date_now = date_now.replace(hour=set_hour, minute=set_minutes, second=0, microsecond=0)

    def convert_timedelta(duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 60)
        return hours, minutes, seconds
    
    def minute_before_bid(self):
        return (self.date_now - datetime.timedelta(minutes=1))
    
    def get_minute_delayed_bid_time(self):
        self.set_chrome_user_and_path()
        self.open_link_to_item()
        self.bid_end_time_left()
        self.bid_end_time()
        self.bid_time_when_seconds_visible()
        self.bid_hours_and_minutes_same_day()
        self.bid_hours_and_minutes_more_than_week()
        self.bid_hours_and_minutes_within_week()
        return self.minute_before_bid()

    def quit(self):
        self.driver.quit()

# if __name__ == "__main__":
#     ebay_bidding = EbayBidding(
#         chrome_user="Default",
#         chrome_user_path="C:\\Users\\a_asf\\AppData\\Local\\Google\\Chrome\\User Data\\",
#         chrome_exe="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
#         ebay_item_number="204498232262")
#     print(ebay_bidding.get_minute_delayed_bid_time())
#     ebay_bidding.quit()