import tkinter as tk
from tkinter import ttk
import openpyxl
from bidder_class import EbayBidding
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime as dt
import datetime

class EbayGui():

    def __init__(self):
        self.root = tk.Tk()
        self.style = ttk.Style(self.root)
        self.root.tk.call("source", "D:\\new_start\\personal_project\\ebay_bidding_bot\\tkinter_excel_app\\forest-dark.tcl")
        # self.root.tk.call("source", "forest-dark.tcl")
        self.style.theme_use("forest-dark")
        self.combo_list = [5, 4, 3, 2, 1]
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def set_frame(self):
        self.frame = ttk.Frame(self.root)
        self.frame.pack()
    
    def bid_border(self):
        self.widgets_frame = ttk.LabelFrame(self.frame, text="Insert Bid")
        self.widgets_frame.grid(row=0, column=0, sticky="nsew")

    def id_row(self):
        self.item_id = ttk.Entry(self.widgets_frame)
        self.item_id.insert(0, "Item ID")
        self.item_id.bind("<FocusIn>", lambda e: self.item_id.delete("0", "end"))
        self.item_id.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

    def amount_row(self):
        self.amount = ttk.Entry(self.widgets_frame)
        self.amount.insert(0, "£")
        self.amount.bind("<FocusIn>", lambda e: self.amount.delete("0", "end"))
        self.amount.grid(row=1, column=0, padx=5, pady=10, sticky="ew") 
    
    def seconds_row(self):
        self.seconds_combobox = ttk.Combobox(self.widgets_frame, values=self.combo_list)
        self.seconds_combobox.current(0)
        self.seconds_combobox.grid(row=2, column=0, padx=5, pady=10, sticky="ew")
    
    def submit_bid(self):
        button = ttk.Button(self.widgets_frame, text="Bid", command=self.insert_row)
        button.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
    
    def bid_history(self):
        self.treeFrame = ttk.Frame(self.frame)
        self.treeFrame.grid(row=0, column=1)
        self.treeScroll = ttk.Scrollbar(self.treeFrame)
        self.treeScroll.pack(side="right", fill="y")

    def load_history(self):
        cols = ("Item ID", "Amount £", "Seconds", "Bid end")
        self.treeview = ttk.Treeview(self.treeFrame, show="headings", yscrollcommand=self.treeScroll.set, columns=cols, height=13)
        self.treeview.column("Item ID", width=100)
        self.treeview.column("Amount £", width=50)
        self.treeview.column("Seconds", width=100, anchor="center")
        self.treeview.column("Bid end", width=200)
        self.treeview.pack()
        self.treeScroll.config(command=self.treeview.yview)
        self.load_data()

    def delete_row(self):
        delete_button = tk.Button(self.widgets_frame, text="Delete row", command=lambda:self.delete())
        delete_button.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

    def delete(self):
        selected_item=self.treeview.selection()[0]
        selected = self.treeview.index(self.treeview.selection())

        try:
            path = "D:\\new_start\\personal_project\\ebay_bidding_bot\\tkinter_excel_app\\bid.xlsx"
            workbook = openpyxl.load_workbook(path)
            sheet = workbook.active
            sheet.delete_rows(selected + 2, 1)
            workbook.save(path)
        except:
            pass
        self.treeview.delete(selected_item)
        self.schedule_on_start()
    
    def remove_old_bid(self):
        path = "D:\\new_start\\personal_project\\ebay_bidding_bot\\tkinter_excel_app\\bid.xlsx"
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        list_values = list(sheet.values)
        for row, item in enumerate(list_values[1:]):
            if item[-1] < dt.now():
                sheet.delete_rows(row + 2, 1)
                workbook.save(path)

    def start_gui(self):
        self.root.mainloop()
    
    def load_data(self):
        path = "D:\\new_start\\personal_project\\ebay_bidding_bot\\tkinter_excel_app\\bid.xlsx"
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active

        list_values = list(sheet.values)
        for col_name in list_values[0]:
            self.treeview.heading(col_name, text=col_name)

        for value_tuple in list_values[1:]:
            self.treeview.insert("", tk.END, values=value_tuple)

    def bid_time(self):
        item = self.item_id.get()

        ebay_bidding = EbayBidding(
            chrome_user="Default",
            chrome_user_path="C:\\Users\\a_asf\\AppData\\Local\\Google\\Chrome\\User Data\\",
            chrome_exe="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            ebay_item_number=f"{item}")
        bid_end = ebay_bidding.get_minute_delayed_bid_time()
        ebay_bidding.quit()
        return bid_end

    def bid(self, item, amount, seconds):
        ebay_bidding = EbayBidding(
            chrome_user="Default",
            chrome_user_path="C:\\Users\\a_asf\\AppData\\Local\\Google\\Chrome\\User Data\\",
            chrome_exe="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            ebay_item_number=f"{item}")
        
        seconds = int(seconds)
        ebay_bidding.get_minute_delayed_bid_time()
        seconds_before_bid = ebay_bidding.place_bid(seconds=seconds, amount=amount)
        self.scheduler.add_job(ebay_bidding.confirm_bid, "date", run_date=seconds_before_bid)
        self.scheduler.add_job(self.remove_old_bid, "date", run_date=(seconds_before_bid + datetime.timedelta(seconds=seconds)))

    def schedule_on_start(self):
        path = "D:\\new_start\\personal_project\\ebay_bidding_bot\\tkinter_excel_app\\bid.xlsx"
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        list_values = list(sheet.values)
        self.scheduler.remove_all_jobs()
        
        for item in list_values[1:]:
            self.scheduler.add_job(self.bid, "date", run_date=item[-1], args=[item[0], item[1], item[2]])
        if len(list_values[1:]) > 0:
            self.scheduler.print_jobs()

    def insert_row(self):
        item = self.item_id.get()
        bid_amount = self.amount.get()
        seconds = self.seconds_combobox.get()
        bid_end = self.bid_time()

        # Insert row into Excel sheet
        path = "D:\\new_start\\personal_project\\ebay_bidding_bot\\tkinter_excel_app\\bid.xlsx"
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        row_values = [item, bid_amount, seconds, bid_end]
        sheet.append(row_values)
        workbook.save(path)

        # Insert row into treeview
        self.treeview.insert("", tk.END, values=row_values)
        self.schedule_on_start()
    
    def start_ebay_bidding_gui(self):
        self.remove_old_bid()
        self.set_frame()
        self.bid_border()
        self.id_row()
        self.amount_row()
        self.seconds_row()
        self.submit_bid()
        self.bid_history()
        self.load_history()
        self.delete_row()
        self.schedule_on_start()
        self.start_gui()

if __name__ == "__main__":
    EbayGui().start_ebay_bidding_gui()