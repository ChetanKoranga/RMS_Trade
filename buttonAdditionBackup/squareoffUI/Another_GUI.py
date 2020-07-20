import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, OptionMenu, StringVar
import csv
from pymongo import MongoClient
import time
import datetime

date = datetime.date.today()
client = MongoClient()
try:
    db = client["Client_Strategy_Status"]
    collec = f"Client_Strategy_Status"
    db.create_collection(collec)
    print("GUI database created")

except Exception as e:
    print(e)
   

win = tk.Tk()
win.geometry("980x500")

_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
_fgcolor = '#000000'  # X11 color: 'black'
_compcolor = '#d9d9d9'  # X11 color: 'gray85'
_ana1color = '#d9d9d9'  # X11 color: 'gray85'
_ana2color = '#ececec'  # Closest X11 color: 'gray92'
font11 = "-family {Yu Gothic UI Semibold} -size 14 -weight "  \
    "bold -slant roman -underline 0 -overstrike 0"
font12 = "-family {Segoe UI} -size 12 -weight normal -slant "  \
    "roman -underline 0 -overstrike 0"
font13 = "-family {Segoe UI} -size 9 -weight bold -slant roman"  \
    " -underline 0 -overstrike 0"
  
win.title("Clientwise Strategy Allocation (Toggler)")

Frame1 = tk.Frame(win)
Frame1.place(relx=0.05, rely=0.06,relheight=0.878, relwidth=0.908)
Frame1.configure(relief='groove')
Frame1.configure(borderwidth="2")
Frame1.configure(relief="groove")
Frame1.configure(background="#d9d9d9")

Label1 = tk.Label(Frame1)
Label1.place(relx=0.05, rely=0.103, height=25, width=85)
Label1.configure(background="#d9d9d9")
Label1.configure(disabledforeground="#a3a3a3")
Label1.configure(font=font12)
Label1.configure(foreground="#000000")
Label1.configure(text='''Algo Name: ''')

var_algo = StringVar(Frame1)
var_algo.set("All")  # initial value



with open(r'C:\Users\Mudraksh_Server1\Desktop\sparedux\squareoffUI\strategylist.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    Algo_Name = []
    for row in csv_reader:
        # print(row)
        if row:
            Algo_Name.append(row[0])

textclient = OptionMenu(Frame1, var_algo, *Algo_Name)
textclient.place(relx=0.18, rely=0.103, height=24, width=150)

Label2 = tk.Label(Frame1)
Label2.place(relx=0.4, rely=0.103, height=25, width=85)
Label2.configure(background="#d9d9d9")
Label2.configure(disabledforeground="#a3a3a3")
Label2.configure(font=font12)
Label2.configure(foreground="#000000")
Label2.configure(text='''ClientID: ''')

var_client = StringVar(Frame1)
var_client.set("All")  # initial value


# client_list = []
with open(r'C:\Users\Mudraksh_Server1\Desktop\sparedux\squareoffUI\clientlist.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    Client_ID = []
    for row in csv_reader:
        # print(row)
        if row:
            Client_ID.append(row[0])
            # client_list.append(Client_ID)


textclient1 = OptionMenu(Frame1, var_client, *Client_ID)
textclient1.place(relx=0.5, rely=0.103, height=24, width=150)

Label3 = tk.Label(Frame1)
Label3.place(relx=0.7, rely=0.103, height=25, width=85)
Label3.configure(background="#d9d9d9")
Label3.configure(disabledforeground="#a3a3a3")
Label3.configure(font=font12)
Label3.configure(foreground="#000000")
Label3.configure(text='''Start/Stop: ''')

var_start_stop = StringVar(Frame1)
var_start_stop.set("Start/Stop")  # initial value

with open(r'StartStop.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    start_stop = []
    for row in csv_reader:
        # print(row)
        if row:
            start_stop.append(row[0])

textclient2 = OptionMenu(Frame1, var_start_stop, *start_stop)
textclient2.place(relx=0.8, rely=0.103, height=24, width=150)

def action():
    get_AlgoName = var_algo.get()
    print(get_AlgoName)
    get_ClientID = var_client.get()
    print(get_ClientID)
    get_start_stop = var_start_stop.get()
    print(get_start_stop)
    
    if get_start_stop == "Start":
        get_start_stop = True

    else:
        get_start_stop = False

    if get_ClientID == "All":
        # for i in range(count):
        for i in Client_ID:
            if i != "All":
                post1 = {"AlgoName": get_AlgoName, "ClientID": i, "Start_Stop": get_start_stop}
                match1 = db[collec].find_one({"$and": [{"AlgoName": get_AlgoName, "ClientID": i}]})
                if match1:
                    db[collec].update({'_id': match1['_id']}, {"$set": post1})

                else:    
                    db[collec].insert(post1)



    if get_AlgoName == "All":
        # for i in range(count):
        for i in Algo_Name:
            if i != "All":
                post2 = {"AlgoName": i, "ClientID": get_ClientID, "Start_Stop": get_start_stop}
                match2 = db[collec].find_one({"$and": [{"AlgoName": i, "ClientID": get_ClientID}]})
                if match2:
                    db[collec].update({'_id': match2['_id']}, {"$set": post2})

                else:    
                    db[collec].insert(post2)            
               

    
    # post = {get_AlgoName: {get_ClientID: get_start_stop}}
        

    if get_ClientID != "All" and get_AlgoName != "All":
        post = {"AlgoName": get_AlgoName, "ClientID": get_ClientID, "Start_Stop": get_start_stop}

        match = db[collec].find_one({"$and": [{"AlgoName": get_AlgoName, "ClientID": get_ClientID}]})
        if match:
            db[collec].update({'_id': match['_id']}, {"$set": post})

        else:
            db[collec].insert(post)
   
    # {'Reference':{'D7730001':True}}
    # var_algo.delete(0, tk.END)
    # var_client.delete(0, tk.END)
    # var_start_stop.delete(0, tk.END)
    
    # orders = db[collec].find()
    # for order in orders:
    #     print(order)


Button1 = tk.Button(Frame1)
Button1.place(relx=0.40, rely=0.56, height=64, width=167)
Button1.configure(activebackground="#ececec")
Button1.configure(activeforeground="#000000")
Button1.configure(background="#808080")
Button1.configure(cursor="fleur")
Button1.configure(disabledforeground="#a3a3a3")
Button1.configure(font=font11)
Button1.configure(foreground="#000000")
Button1.configure(highlightbackground="#d9d9d9")
Button1.configure(highlightcolor="black")
Button1.configure(pady="0")
Button1.configure(text='''Submit''')
Button1.configure(command = action)



win.mainloop()