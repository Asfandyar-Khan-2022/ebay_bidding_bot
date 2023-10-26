"""eBay bidding bot processing"""

import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime as dt
import datetime

class EbayBidding:
    """The class is used to perform bidding."""
    def __init__(
            self, chrome_user, 
            chrome_user_path,
            chrome_exe, 
            ebay_item_number):
        """Initialize the chrome path and item.

        Args:
            chrome_user (str)       : Select the profile to use.
            chrome_user_path (str)  : Path to the profile.
            chrome_exe (str)        : Path to chrome executable.   

        """
        self.chrome_user = chrome_user             
        self.chrome_user_path = chrome_user_path     
        self.chrome_exe = chrome_exe                
        self.ebay_item_number = ebay_item_number  

        #: Allows for browser settings to be selected
        self.options = Options()  

        #: Disable browser window.
        self.options.add_argument("--headless=new")
    
    def set_chrome_user_and_path(self):
        """Sets chrome path."""
        self.options.add_argument(f"--profile-directory={self.chrome_user}")
        self.options.add_argument(f"--user-data-dir={self.chrome_user_path}")
    
    def open_link_to_item(self):
        """Open chrome and go to item page."""
        self.driver = uc.Chrome(executable_path=self.chrome_exe, options=self.options)
        self.driver.get(f"https://www.ebay.co.uk/itm/{self.ebay_item_number}")
        self.driver.implicitly_wait(3)

    def correct_link(self):
        """Check if the link has an item that can be bid on."""
        if self.driver.find_element(By.CLASS_NAME, "ux-call-to-action__text").text == "Buy it now":
            self.quit()

    def bid_end_time_left(self):
        """Time difference to bid end time"""
        self.correct_link()
        self.bid_end_time_left = self.driver.find_element(
            By.CLASS_NAME,
            'ux-timer__text')
        self.current_time = self.bid_end_time_left.text
    
    def bid_end_time(self):
        """The time when the bid is due to end"""
        bid_end_time = self.driver.find_element(
            By.CLASS_NAME, 
            'ux-timer__time-left')
        self.end_time = bid_end_time.text.split()

    def new_time(self):
        """Get time just after the seconds change."""
        while True:
            new_time = self.bid_end_time_left.text
            if new_time != self.current_time:
                return new_time
    
    def bid_time_when_seconds_visible(self):
        """Get the exact time including minutes if possible."""
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
        """Get the time if bid is today and hour left is more than 0"""
        if self.end_time[0] == "Today" and self.hour - dt.now().hour != 0:
            date_now = dt.now()
            set_hour = int(self.end_time[1].split(":")[0])
            set_minutes = int(self.end_time[1].split(":")[1])
            self.date_now = date_now.replace(hour=set_hour, minute=set_minutes, second=0, microsecond=0)
        
    def bid_hours_and_minutes_more_than_week(self):
            """Get bid time when item bid requst is made for item ending in more than a week"""
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
    
    def calculate_days_before_bid(self, day_number):
        """The number of days from now when the bid will end"""
        set_hour = int(self.end_time[1].split(":")[0])
        set_minutes = int(self.end_time[1].split(":")[1])
        date_now = (dt.now() + datetime.timedelta(day_number))
        self.date_now = date_now.replace(hour=set_hour, minute=set_minutes, second=0, microsecond=0)

    def bid_hours_and_minutes_within_week(self):
            """"""
            if "/" not in self.end_time[0] and self.end_time[0] != "Today":
                i = 0
                if self.end_time[0].strip(", ") == (dt.now()).strftime("%A").strip(" "):
                    self.calculate_days_before_bid(7)

                while self.end_time[0].strip(", ") != (dt.now() + datetime.timedelta(i)).strftime("%A").strip(" "):
                    i += 1
                    self.calculate_days_before_bid(i)

    def convert_timedelta(duration):
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 60)
        return hours, minutes, seconds
    
    def minute_before_bid(self):
        return (self.date_now - datetime.timedelta(minutes=1))
    
    def seconds_before_bid(self, seconds):
        return (self.date_now - datetime.timedelta(seconds=seconds))
    
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
    
    def click_submit_bid(self):
        submid_bid = self.driver.find_element(By.CLASS_NAME, 'ux-call-to-action__text')
        submid_bid.click()
    
    def insert_bid_amount(self, amount):
        self.driver.implicitly_wait(3)
        insert_amount = self.driver.find_element(By.ID, 's0-0-1-1-3-placebid-section-offer-section-price-10-textbox')
        insert_amount.send_keys(amount)
    
    def review_inserted_amount(self, seconds):
        review_bid = self.driver.find_element(By.CSS_SELECTOR, 'button[class="btn btn--fluid btn--large btn--primary"]')
        if review_bid.is_enabled():
            review_bid.click()
            return(self.seconds_before_bid(seconds=seconds))
        self.quit()
        return False
    
    def confirm_bid(self):
        self.driver.implicitly_wait(3)
        confirm_bid = self.driver.find_element(By.ID, 'confirmBid')
        confirm_bid.click()

    def quit(self):
        self.driver.close()
        self.driver.quit()

# if __name__ == "__main__":
#     ebay_bidding = EbayBidding(
#         chrome_user="Default",
#         chrome_user_path="C:\\Users\\a_asf\\AppData\\Local\\Google\\Chrome\\User Data\\",
#         chrome_exe="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
#         ebay_item_number="204498232262")
#     print(ebay_bidding.get_minute_delayed_bid_time())
#     ebay_bidding.quit()