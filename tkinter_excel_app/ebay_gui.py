import tkinter as tk
from tkinter import ttk
import openpyxl
from bidder_class import EbayBidding
import sched
import time 

def load_data():
    path = "bid.xlsx"
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active

    list_values = list(sheet.values)
    for col_name in list_values[0]:
        treeview.heading(col_name, text=col_name)

    for value_tuple in list_values[1:]:
        treeview.insert("", tk.END, values=value_tuple)

def print_excel():
    path = "bid.xlsx"
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active

    list_values = list(sheet.values)
    for i in list_values[1:]:
        if i[-1] == None:
            ebay_bidding = EbayBidding(
                chrome_user="Default",
                chrome_user_path="C:\\Users\\a_asf\\AppData\\Local\\Google\\Chrome\\User Data\\",
                chrome_exe="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                ebay_item_number=f"{i[0]}")
            bid_end = ebay_bidding.get_minute_delayed_bid_time()
            ebay_bidding.quit()
        return bid_end
    return None

def place_bid():
    print("BID!!")

def schedule(bid_end):
    path = "bid.xlsx"
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active
    list_values = list(sheet.values)
    
    for count, item in enumerate(list_values[1:], 1):
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enterabs(bid_end.timestamp(), count, place_bid)
    
    scheduler.run()

def insert_row():
    item = item_id.get()
    bid_amount = amount.get()
    seconds = seconds_combobox.get()
    bid_end = print_excel()

    # Insert row into Excel sheet
    path = "bid.xlsx"
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active
    row_values = [item, bid_amount, seconds, bid_end]
    sheet.append(row_values)
    workbook.save(path)

    # Insert row into treeview
    treeview.insert("", tk.END, values=row_values)


root = tk.Tk()

style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

combo_list = [5, 4, 3, 2, 1]

frame = ttk.Frame(root)
frame.pack()

widgets_frame = ttk.LabelFrame(frame, text="Insert Bid")
widgets_frame.grid(row=0, column=0, sticky="nsew")

# Item ID row
item_id = ttk.Entry(widgets_frame)
item_id.insert(0, "Item ID")
item_id.bind("<FocusIn>", lambda e: item_id.delete("0", "end"))
item_id.grid(row=0, column=0, padx=5, pady=10, sticky="ew")

# Amount row
amount = ttk.Entry(widgets_frame)
amount.insert(0, "£")
amount.bind("<FocusIn>", lambda e: amount.delete("0", "end"))
amount.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

# Seconds row
seconds_combobox = ttk.Combobox(widgets_frame, values=combo_list)
seconds_combobox.current(0)
seconds_combobox.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

# Submit bid
button = ttk.Button(widgets_frame, text="Bid", command=insert_row)
button.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")

# Bid history
treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1)
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

cols = ("Item ID", "Amount £", "Seconds", "Bid end")
treeview = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=13)
treeview.column("Item ID", width=100)
treeview.column("Amount £", width=50)
treeview.column("Seconds", width=100, anchor="center")
treeview.column("Bid end", width=100)
treeview.pack()
treeScroll.config(command=treeview.yview)
load_data()

# Delete row
delete_button = tk.Button(widgets_frame, text="Delete row", command=lambda:delete())
delete_button.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")

def delete():
    selected_item=treeview.selection()[0]
    selected = treeview.index(treeview.selection())
    print(treeview.index(treeview.selection()))

    try:
        path = "bid.xlsx"
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active
        sheet.delete_rows(selected + 2, 1)
        workbook.save(path)
    except:
        print(selected_item)

    treeview.delete(selected_item)

root.mainloop()

# ebay_bidding = EbayBidding(
#     chrome_user="Default",
#     chrome_user_path="C:\\Users\\a_asf\\AppData\\Local\\Google\\Chrome\\User Data\\",
#     chrome_exe="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
#     ebay_item_number="186118426817")
# ebay_bidding.get_minute_delayed_bid_time()
# ebay_bidding.quit()