import sys
import datetime
import orderManagement
from pymongo import MongoClient
import orderSlicer
from multiprocessing import Process
import csv

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

from tkinter import messagebox, OptionMenu, StringVar

import squareoff_support


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1(root)
    squareoff_support.init(root, top)
    root.mainloop()


w = None


def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    squareoff_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    date = datetime.date.today()

    def getClientAlgoList(self):
        client_list = []
        algo_list = []

        connection = MongoClient('localhost', 27017)
        listdb = connection['all_list']
        collection_client = listdb['client']
        collection_algo = listdb['algo']
        for i in collection_client.distinct("client"):
            client_list.append(i)
        for i in collection_algo.distinct("value"):
            algo_list.append(i)
        return client_list, algo_list

    def squareoff(self):
        collec = f'cumulative_{self.date}'
        strategyName = self.var_strategy.get()
        clientID = self.var_client.get()
        try:
            connection = MongoClient('localhost', 27017)
            cumulative_db = connection.Cumulative_symphonyorder
            cumulative_collection = cumulative_db[collec]
        except:
            messagebox.showerror("Database Connection Error",
                                 "Could not connect to database. Please check your connection.")

        if strategyName == "All" and clientID == "All":
            print(strategyName, "========", clientID)
            documents = cumulative_collection.find()
        elif strategyName == "All":
            print(strategyName, "========", clientID)
            documents = cumulative_collection.find({'clientID': clientID})
        elif clientID == "All":
            print(strategyName, "========", clientID)
            documents = cumulative_collection.find({'algoName': strategyName})
        else:
            print(strategyName, "========", clientID)
            documents = cumulative_collection.find(
                {"$and": [{"algoName": strategyName}, {"clientID": clientID}]})

        # order = orderManagement.OrderSystem()
        # order = orderManagement.OrderSystem2()
        obj = orderSlicer.OrderSystem()
        for doc in documents:
            # print("DOCS=====",doc)
            exchangeSegment = doc["exchangeSegment"]
            exchangeInstrumentID = doc["exchangeInstrumentID"]
            productType = doc["productType"]
            orderType = 'MARKET'  # doc["orderType"]
            orderQuantity = doc["quantity"]
            if orderQuantity < 0:
                orderSide = "BUY"
            else:
                orderSide = "SELL"

            algoName = doc["algoName"]
            clientID = doc['clientID']
            symbol = doc["symbol"]
            try:
                with open(rf'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\Symphony Latest API\Symphony Order Server Dealer\Allowed algos\\{algoName}.txt') as file:
                    otp = file.read()
                    # print(otp)
            except Exception as e:
                pass
            if symbol.startswith("BANKNIFTY") and orderQuantity != 0:
                if 'FUT' not in symbol:
                    # if abs(orderQuantity) > 60:
                    p1 = Process(target=obj.placeSliceOrder, args=(
                        exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, abs(
                            orderQuantity), algoName,
                        clientID, 200,
                        0.1, otp)).start()
                    # else:
                    #     order.place_order(exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide,
                    #                       abs(orderQuantity), algoName, clientID)
                else:
                    p1 = Process(target=obj.placeSliceOrder, args=(
                        exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, abs(
                            orderQuantity), algoName,
                        clientID, 100,
                        0.1, otp)).start()
            elif symbol.startswith("NIFTY") and orderQuantity != 0:
                # if abs(orderQuantity) > 225:
                p1 = Process(target=obj.placeSliceOrder, args=(
                    exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, abs(
                        orderQuantity), algoName,
                    clientID, 750,
                    0.2, otp)).start()
                # else:
                #     order.place_order(exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide,
                #                       abs(orderQuantity), algoName, clientID)
            # elif orderQuantity != 0:
            #     order.place_order(exchangeSegment, exchangeInstrumentID, productType,
            #                       orderType, orderSide, abs(orderQuantity), algoName, clientID)
            # if orderQuantity != 0:
            #     order.place_order(exchangeSegment,exchangeInstrumentID,productType,orderType,orderSide,orderQuantity,algoName,clientID)
            # ,exchangeSegment,exchangeInstrumentID,
                # 	   productType,orderType,orderSide,orderQuantity, algoName
        messagebox.showinfo("Success", "SquareOff Successfull.")
        # messagebox.showinfo("Hey Hey","Its squareoff function.")

    def squareoff_all(self):
        collec = f'cumulative_{self.date}'

        try:
            connection = MongoClient('localhost', 27017)
            cumulative_db = connection.Cumulative_symphonyorder
            cumulative_collection = cumulative_db[collec]
        except:
            messagebox.showerror("Database Connection Error",
                                 "Could not connect to database. Please check your connection.")

        documents = cumulative_collection.find()
        # order = orderManagement.OrderSystem()
        # order = orderManagement.OrderSystem2()
        obj = orderSlicer.OrderSystem()
        for doc in documents:
            # if doc['algoName'] != '1000 EMA Overnight' and doc['algoName'] != 'SpreadSell':
            if 'Overnight' not in doc['algoName']:
                exchangeSegment = doc["exchangeSegment"]
                exchangeInstrumentID = doc["exchangeInstrumentID"]
                productType = doc["productType"]
                orderType = 'MARKET'  # doc["orderType"]

                orderQuantity = doc["quantity"]
                if orderQuantity < 0:
                    orderSide = "BUY"
                else:
                    orderSide = "SELL"

                algoName = doc["algoName"]
                clientID = doc["clientID"]
                symbol = doc["symbol"]
                print("SYMBOL ======", symbol)

                try:
                    with open(rf'C:\Users\Mudraksh_Server1\Desktop\ServerCodes\Symphony Latest API\Symphony Order Server Dealer\Allowed algos\\{algoName}.txt') as file:
                        otp = file.read()
                        # print(otp)
                except Exception as e:
                    pass

                if symbol.startswith("BANKNIFTY") and orderQuantity != 0:
                    print("HEY BANK")
                    if 'FUT' not in symbol:
                        # if abs(orderQuantity) > 60:
                        p1 = Process(target=obj.placeSliceOrder, args=(
                            exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, abs(
                                orderQuantity), algoName,
                            clientID, 200,
                            0.1, otp)).start()
                        # else:
                        #     order.place_order(exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide,
                        #                       abs(orderQuantity), algoName, clientID)
                    else:
                        p1 = Process(target=obj.placeSliceOrder, args=(
                            exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, abs(
                                orderQuantity), algoName,
                            clientID, 100,
                            0.1, otp)).start()

                elif symbol.startswith("NIFTY") and orderQuantity != 0:
                    print("HEY NIF")
                    # if abs(orderQuantity) > 225:
                    p1 = Process(target=obj.placeSliceOrder, args=(
                        exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide, abs(
                            orderQuantity), algoName,
                        clientID, 750,
                        0.2, otp)).start()
                # else:
                #     order.place_order(exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide,
                #                       abs(orderQuantity), algoName, clientID)
            # elif orderQuantity != 0:
            #     print("HEY OTHER")
            #     order.place_order(exchangeSegment, exchangeInstrumentID, productType, orderType, orderSide,
            #                       abs(orderQuantity), algoName, clientID)

            # if orderQuantity != 0:
            #     order.place_order(exchangeSegment,exchangeInstrumentID,productType,orderType,orderSide,abs(orderQuantity),algoName,clientID)
            # ,exchangeSegment,exchangeInstrumentID,
                # 	   productType,orderType,orderSide,orderQuantity, algoName
        messagebox.showinfo("Success", "SquareOff Successfull.")

    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
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

        top.geometry("600x450+342+53")
        top.minsize(120, 1)
        top.maxsize(1370, 749)
        top.resizable(1, 1)
        top.title("Auto Square Off")
        top.configure(background="#d9d9d9")

        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=0.05, rely=0.067,
                          relheight=0.878, relwidth=0.908)

        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#d9d9d9")

        self.Button1 = tk.Button(self.Frame1)
        self.Button1.place(relx=0.44, rely=0.076, height=64, width=267)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#ff0000")
        self.Button1.configure(cursor="fleur")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font11)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''SquareOff All''')
        self.Button1.configure(command=self.squareoff_all)

        self.Frame2 = tk.Frame(self.Frame1)
        self.Frame2.place(relx=0.055, rely=0.38,
                          relheight=0.494, relwidth=0.89)
        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(background="#d9d9d9")

        self.Label1 = tk.Label(self.Frame2)
        self.Label1.place(relx=0.082, rely=0.103, height=27, width=150)
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font12)
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Strategy Name''')

        self.var_strategy = StringVar(self.Frame2)
        self.var_strategy.set("All")  # initial value

        client_list, strategy_list = self.getClientAlgoList()

        self.textstrategy = OptionMenu(
            self.Frame2, self.var_strategy, *strategy_list)
        # self.textalgoname.place(relx=0.142, rely=0.05, x=-2, y=2)
        self.textstrategy.place(relx=0.082, rely=0.43, height=24, width=200)
        # print(var_strategy)

        self.Label2 = tk.Label(self.Frame2)
        self.Label2.place(relx=0.68, rely=0.103, height=27, width=100)
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font=font12)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''ClientID''')

        self.var_client = StringVar(self.Frame2)
        self.var_client.set("All")  # initial value

        self.textclient = OptionMenu(
            self.Frame2, self.var_client, *client_list)
        # self.textalgoname.place(relx=0.142, rely=0.05, x=-2, y=2)
        self.textclient.place(relx=0.68, rely=0.43, height=24, width=150)

        self.Button2 = tk.Button(self.Frame2)
        self.Button2.place(relx=0.412, rely=0.667, height=44, width=87)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#0080c0")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font=font13)
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''SquareOff''')
        self.Button2.configure(command=self.squareoff)


if __name__ == '__main__':
    vp_start_gui()
