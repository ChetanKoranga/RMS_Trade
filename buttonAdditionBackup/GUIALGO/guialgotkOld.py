#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.20
#  in conjunction with Tcl version 8.6
#    Oct 03, 2019 05:54:13 AM IST  platform: Windows NT

import sys
import random
import json
import csv

import tkinter as tk
from tkinter import messagebox, OptionMenu, StringVar

import guialgotk_support


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1(root)
    guialgotk_support.init(root, top)
    root.mainloop()


w = None


def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    guialgotk_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class CsvToDict:
    optionIDSymname = {}
    reader = csv.reader(open(r'OptionIds.txt', 'r'))
    for row in reader:
        k, v1 = row
        optionIDSymname[v1] = k

    futIDSymname = {}
    reader = csv.reader(open(r'FuturesIds.txt', 'r'))
    for row in reader:
        k, v1 = row
        futIDSymname[v1] = k

    commodityIDSymname = {}
    reader = csv.reader(open(r'MCXIds.txt', 'r'))
    for row in reader:
        k, v1 = row
        commodityIDSymname[v1] = k

    stocksIDSymname = {}
    reader = csv.reader(open(r'stocksIds.txt', 'r'))
    for row in reader:
        k, v1 = row
        stocksIDSymname[v1] = k


obj = CsvToDict()
stocksMap = obj.stocksIDSymname
optionMap = obj.optionIDSymname
futureMap = obj.futIDSymname
commodityMap = obj.commodityIDSymname


# print(stocksMap)


class Toplevel1:

    def UpdateButton(self):
        import pymongo
        from pymongo import MongoClient
        import datetime
        date = datetime.date.today()

        collec = f'orders_{date}'
        try:
            mongocl = MongoClient()
            db = mongocl['symphonyorder_raw']
            db.create_collection(collec)
            print("Collection created successfully.")
        except Exception:
            if db[collec]:
                pass
            else:
                print("ERROR: Mongo Connection Error")

        algoname = self.textalgoname.get("1.0", 'end-1c')
        exchangesegment = self.seg_var.get()
        print(exchangesegment)

        symbol = self.textsymbol.get("1.0", 'end-1c').upper()
        # print(symbol)
        if symbol in futureMap.keys():
            exchangeinstrumentID = futureMap[symbol]

        elif symbol in optionMap.keys():
            exchangeinstrumentID = optionMap[symbol]

        elif symbol in commodityMap.keys():
            exchangeinstrumentID = commodityMap[symbol]

        elif symbol in stocksMap.keys():
            exchangeinstrumentID = stocksMap[symbol]

        else:
            exchangeinstrumentID = symbol

        producttype = "MIS"
        orderside = self.buysell_var.get()
        print(orderside)
        ordertype = "MARKET"
        try:
            orderquantity = int(self.textorderquantity.get("1.0", 'end-1c'))
        except Exception:
            messagebox.showerror("Input Error", "Please provide valid Order quantity")
            return
        timeInForce = "DAY"
        disclosedQuantity = 0
        limitPrice = 0
        stopPrice = 0
        clientID = self.var_client.get()
        orderUniqueIdentifier = str(random.randint(10000, 1000000))

        # if orderside not "BUY" or "SELL" :
        if clientID and algoname and exchangesegment and exchangeinstrumentID and (
                orderside == "BUY" or orderside == "SELL") and orderquantity:
            post = {
                "exchangeSegment": exchangesegment,
                "exchangeInstrumentID": exchangeinstrumentID,
                "productType": producttype,
                "orderType": ordertype,
                "orderSide": orderside,
                "timeInForce": timeInForce,
                "disclosedQuantity": disclosedQuantity,
                "orderQuantity": orderquantity,
                "limitPrice": limitPrice,
                "stopPrice": stopPrice,
                "clientID": clientID,
                "orderUniqueIdentifier": orderUniqueIdentifier,
                "algoName": algoname,
            }
            db[collec].insert_one(post)
            messagebox.showinfo("Success", "Database Updated Successfully.")

        else:
            messagebox.showerror("Updation Error", "Recheck your inputs.")

    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        font12 = "-family {Segoe UI} -size 10 -weight bold -slant " \
                 "roman -underline 0 -overstrike 0"

        top.geometry("750x700+252+59")
        top.title("Order Updater")
        top.configure(background="#d9d9d9")

        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=0.02, rely=0.04, relheight=0.95, relwidth=0.95)

        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(width=715)

        # self.restartall = tk.Button(self.Frame1)
        # self.restartall.place(relx=0.643, rely=0.063, height=44, width=94)
        # self.restartall.configure(activebackground="#ececec")
        # self.restartall.configure(activeforeground="#000000")
        # self.restartall.configure(background="#1dd609")
        # self.restartall.configure(disabledforeground="#a3a3a3")
        # self.restartall.configure(foreground="#000000")
        # self.restartall.configure(highlightbackground="#d9d9d9")
        # self.restartall.configure(highlightcolor="#000000")
        # self.restartall.configure(pady="0")
        # self.restartall.configure(text='''Restart All''')
        # self.restartall.configure(width=94)

        # self.stopall = tk.Button(self.Frame1)
        # self.stopall.place(relx=0.797, rely=0.063, height=44, width=97)
        # self.stopall.configure(activebackground="#ececec")
        # self.stopall.configure(activeforeground="#000000")
        # self.stopall.configure(background="#f42b0c")
        # self.stopall.configure(disabledforeground="#a3a3a3")
        # self.stopall.configure(foreground="#000000")
        # self.stopall.configure(highlightbackground="#d9d9d9")
        # self.stopall.configure(highlightcolor="black")
        # self.stopall.configure(pady="0")
        # self.stopall.configure(text='''Stop All''')
        # self.stopall.configure(width=97)

        self.Frame2 = tk.Frame(self.Frame1)
        self.Frame2.place(relx=0.05, rely=0.050, relheight=0.85, relwidth=0.888)
        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief='groove')
        self.Frame2.configure(background="#d9d9d9")
        self.Frame2.configure(width=635)

        self.Label2 = tk.Label(self.Frame2)
        self.Label2.place(relx=0.132, rely=0.03, height=31, width=200)
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font=font12)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''ClientID''')


        self.var_client = StringVar(self.Frame2)
        self.var_client.set("All")  # initial value

        self.textclient = OptionMenu(self.Frame2, self.var_client, "All", "D7730001", "D7730002", "D7730003", "D18138",
                                     "V7410004")
        # self.textalgoname.place(relx=0.142, rely=0.05, x=-2, y=2)
        self.textclient.place(relx=0.504, rely=0.03, height=31, width=150)

        self.algoname = tk.Label(self.Frame2)
        self.algoname.place(relx=0.142, rely=0.15, height=31, width=150)
        self.algoname.configure(background="#d9d9d9")
        self.algoname.configure(disabledforeground="#a3a3a3")
        self.algoname.configure(font=font12)
        self.algoname.configure(foreground="#000000")
        self.algoname.configure(text='''Algo Name''')
        self.algoname.configure(width=64)

        self.textalgoname = tk.Text(self.Frame2)
        self.textalgoname.place(relx=0.504, rely=0.15, height=24, width=200)
        self.textalgoname.configure(background="#d5b673")
        self.textalgoname.configure(pady="0")
        self.textalgoname.configure(width=97)

        # var = StringVar(self.Frame2)
        # var.set("one") # initial value

        # self.textalgoname = OptionMenu(self.Frame2, var, "one", "two", "three", "four")
        # self.textalgoname.place(relx=0.142, rely=0.05, x=-2, y=2)
        # self.textalgoname.pack()

        self.exchangesegment = tk.Label(self.Frame2)
        self.exchangesegment.place(relx=0.142, rely=0.24, height=31, width=150)
        self.exchangesegment.configure(background="#d9d9d9")
        self.exchangesegment.configure(disabledforeground="#a3a3a3")
        self.exchangesegment.configure(font=font12)
        self.exchangesegment.configure(foreground="#000000")
        self.exchangesegment.configure(text='''Exchange Segment''')
        self.exchangesegment.configure(width=64)

        # self.textexchangesegment = tk.Text(self.Frame2)
        # self.textexchangesegment.place(relx=0.504, rely=0.192, height=24, width=200)
        # self.textexchangesegment.configure(background="#d5b673")
        # self.textexchangesegment.configure(pady="0")
        # # self.textexchangeSegment.configure(placeholder='''Write Exchange Segment Here...''')
        # self.textexchangesegment.configure(width=97)

        self.seg_var = StringVar(self.Frame2)
        self.seg_var.set("NSEFO")  # initial value

        self.textexchangesegment = OptionMenu(self.Frame2, self.seg_var, "NSECM", "NSEFO", "NSECD", "MCXFO")
        self.textexchangesegment.place(relx=0.504, rely=0.24, height=24, width=200)
        # print(seg_var)

        self.symbol = tk.Label(self.Frame2)
        self.symbol.place(relx=0.04, rely=0.40, height=78, width=300)
        self.symbol.configure(activebackground="#f9f9f9")
        self.symbol.configure(activeforeground="black")
        self.symbol.configure(background="#d9d9d9")
        self.symbol.configure(disabledforeground="#a3a3a3")
        self.symbol.configure(font=font12)
        self.symbol.configure(foreground="#000000")
        self.symbol.configure(highlightbackground="#d9d9d9")
        self.symbol.configure(highlightcolor="black")
        self.symbol.configure(
            text='''Symbol\n(eg.- Stocks:"COALINDIA",\nMCX:"CRUDEOIL-I",\nFutures:"TATAGLOBAL19OCTFUT",\nOptions:"BANKNIFTY03OCT1926300PE")''')

        self.textsymbol = tk.Text(self.Frame2)
        self.textsymbol.place(relx=0.504, rely=0.40, height=24, width=200)
        self.textsymbol.configure(background="#d5b673")
        self.textsymbol.configure(pady="0")
        self.textsymbol.configure(width=97)

        # self.producttype = tk.Label(self.Frame2)
        # self.producttype.place(relx=0.142, rely=0.476, height=31, width=150)
        # self.producttype.configure(activebackground="#f9f9f9")
        # self.producttype.configure(activeforeground="black")
        # self.producttype.configure(background="#d9d9d9")
        # self.producttype.configure(disabledforeground="#a3a3a3")
        # self.producttype.configure(font=font12)
        # self.producttype.configure(foreground="#000000")
        # self.producttype.configure(highlightbackground="#d9d9d9")
        # self.producttype.configure(highlightcolor="black")
        # self.producttype.configure(text='''Product Type''')

        # self.textproducttype = tk.Text(self.Frame2)
        # self.textproducttype.place(relx=0.504, rely=0.476, height=24, width=200)
        # self.textproducttype.configure(background="#d5b673")
        # self.textproducttype.configure(pady="0")
        # self.textproducttype.configure(width=97)

        # self.ordertype = tk.Label(self.Frame2)
        # self.ordertype.place(relx=0.142, rely=0.618, height=31, width=150)
        # self.ordertype.configure(activebackground="#f9f9f9")
        # self.ordertype.configure(activeforeground="black")
        # self.ordertype.configure(background="#d9d9d9")
        # self.ordertype.configure(disabledforeground="#a3a3a3")
        # self.ordertype.configure(font=font12)
        # self.ordertype.configure(foreground="#000000")
        # self.ordertype.configure(highlightbackground="#d9d9d9")
        # self.ordertype.configure(highlightcolor="black")
        # self.ordertype.configure(text='''Order Type''')

        # self.textordertype = tk.Text(self.Frame2)
        # self.textordertype.place(relx=0.504, rely=0.618, height=24, width=200)
        # self.textordertype.configure(background="#d5b673")
        # self.textordertype.configure(pady="0")
        # self.textordertype.configure(width=97)

        self.orderside = tk.Label(self.Frame2)
        self.orderside.place(relx=0.142, rely=0.650, height=31, width=150)
        self.orderside.configure(activebackground="#f9f9f9")
        self.orderside.configure(activeforeground="black")
        self.orderside.configure(background="#d9d9d9")
        self.orderside.configure(disabledforeground="#a3a3a3")
        self.orderside.configure(font=font12)
        self.orderside.configure(foreground="#000000")
        self.orderside.configure(highlightbackground="#d9d9d9")
        self.orderside.configure(highlightcolor="black")
        self.orderside.configure(text='''Order Side''')

        # self.textorderside = tk.Text(self.Frame2)
        # self.textorderside.place(relx=0.504, rely=0.650, height=24, width=200)
        # self.textorderside.configure(background="#d5b673")
        # self.textorderside.configure(pady="0")
        # self.textorderside.configure(width=97)

        self.buysell_var = StringVar(self.Frame2)
        self.buysell_var.set("BUY")

        sides = [
            "BUY",
            "SELL"
        ]

        # def ShowChoice(self):
        #     buysell_var = buysell_var.get()
        #     print(buysell_var)

        tk.Label(self.Frame2,
                 justify=tk.LEFT,
                 padx=20).pack()

        relx = 0.500
        for side in sides:
            tk.Radiobutton(self.Frame2,
                           text=side,
                           padx=20,
                           variable=self.buysell_var,
                           #   command = setorderside,
                           value=side).place(relx=relx, rely=0.650, relheight=0.056
                                             , relwidth=0.16)
            relx += 0.170

        # buysell_var.get()

        #

        # self.buyrad = tk.Radiobutton(self.Frame2)
        # self.buyrad.place(relx=0.500, rely=0.650, relheight=0.056
        #         , relwidth=0.097)
        # self.buyrad.configure(activebackground="#ececec")
        # self.buyrad.configure(activeforeground="#000000")
        # self.buyrad.configure(background="#d9d9d9")
        # self.buyrad.configure(disabledforeground="#a3a3a3")
        # self.buyrad.configure(foreground="#000000")
        # self.buyrad.configure(highlightbackground="#d9d9d9")
        # self.buyrad.configure(highlightcolor="black")
        # self.buyrad.configure(justify='left')
        # self.buyrad.configure(text='''BUY''')
        # self.buyrad.configure(variable="BUY")
        # self.buyrad.configure(command=self.,value="BUY")

        # self.sellrad = tk.Radiobutton(self.Frame2)
        # self.sellrad.place(relx=0.700, rely=0.650, relheight=0.056
        #         , relwidth=0.097)
        # self.sellrad.configure(activebackground="#ececec")
        # self.sellrad.configure(activeforeground="#000000")
        # self.sellrad.configure(background="#d9d9d9")
        # self.sellrad.configure(disabledforeground="#a3a3a3")
        # self.sellrad.configure(foreground="#000000")
        # self.sellrad.configure(highlightbackground="#d9d9d9")
        # self.sellrad.configure(highlightcolor="black")
        # self.sellrad.configure(justify='left')s
        # self.sellrad.configure(text='''SELL''')
        # self.sellrad.configure(variable="SELL")

        self.orderquantity = tk.Label(self.Frame2)
        self.orderquantity.place(relx=0.142, rely=0.792, height=31, width=150)
        self.orderquantity.configure(activebackground="#f9f9f9")
        self.orderquantity.configure(activeforeground="black")
        self.orderquantity.configure(background="#d9d9d9")
        self.orderquantity.configure(disabledforeground="#a3a3a3")
        self.orderquantity.configure(font=font12)
        self.orderquantity.configure(foreground="#000000")
        self.orderquantity.configure(highlightbackground="#d9d9d9")
        self.orderquantity.configure(highlightcolor="black")
        self.orderquantity.configure(text='''Order Quantity''')

        self.textorderquantity = tk.Text(self.Frame2)
        self.textorderquantity.place(relx=0.504, rely=0.792, height=24, width=200)
        self.textorderquantity.configure(background="#d5b673")
        self.textorderquantity.configure(pady="0")
        self.textorderquantity.configure(width=97)

        self.updatebutton = tk.Button(self.Frame1)
        self.updatebutton.place(relx=0.400, rely=0.93, height=24, width=97)
        self.updatebutton.configure(activebackground="#ececec")
        self.updatebutton.configure(activeforeground="#000000")
        self.updatebutton.configure(background="#05ad27")
        self.updatebutton.configure(disabledforeground="#a3a3a3")
        self.updatebutton.configure(foreground="#000000")
        self.updatebutton.configure(highlightbackground="#d9d9d9")
        self.updatebutton.configure(highlightcolor="black")
        self.updatebutton.configure(pady="0")
        self.updatebutton.configure(text='''Update''')
        self.updatebutton.configure(width=97)
        self.updatebutton.configure(command=self.UpdateButton)

        # self.algo2 = tk.Label(self.Frame2)
        # self.algo2.place(relx=0.142, rely=0.200, height=31, width=64)
        # self.algo2.configure(activebackground="#f9f9f9")
        # self.algo2.configure(activeforeground="black")
        # self.algo2.configure(background="#d9d9d9")
        # self.algo2.configure(disabledforeground="#a3a3a3")
        # self.algo2.configure(font=font12)
        # self.algo2.configure(foreground="#000000")
        # self.algo2.configure(highlightbackground="#d9d9d9")
        # self.algo2.configure(highlightcolor="black")
        # self.algo2.configure(text='''Algo 2''')

        # self.restartalgo2 = tk.Button(self.Frame2)
        # self.restartalgo2.place(relx=0.504, rely=0.200, height=24, width=97)
        # self.restartalgo2.configure(activebackground="#ececec")
        # self.restartalgo2.configure(activeforeground="#000000")
        # self.restartalgo2.configure(background="#05ad27")
        # self.restartalgo2.configure(disabledforeground="#a3a3a3")
        # self.restartalgo2.configure(foreground="#000000")
        # self.restartalgo2.configure(highlightbackground="#d9d9d9")
        # self.restartalgo2.configure(highlightcolor="black")
        # self.restartalgo2.configure(pady="0")
        # self.restartalgo2.configure(text='''Button''')
        # self.restartalgo2.configure(width=97)

        # self.algo3 = tk.Label(self.Frame2)
        # self.algo3.place(relx=0.142, rely=0.300, height=31, width=64)
        # self.algo3.configure(activebackground="#f9f9f9")
        # self.algo3.configure(activeforeground="black")
        # self.algo3.configure(background="#d9d9d9")
        # self.algo3.configure(disabledforeground="#a3a3a3")
        # self.algo3.configure(font=font12)
        # self.algo3.configure(foreground="#000000")
        # self.algo3.configure(highlightbackground="#d9d9d9")
        # self.algo3.configure(highlightcolor="black")
        # self.algo3.configure(text='''Algo 3''')

        # self.restartalgo3 = tk.Button(self.Frame2)
        # self.restartalgo3.place(relx=0.504, rely=0.300, height=24, width=97)
        # self.restartalgo3.configure(activebackground="#ececec")
        # self.restartalgo3.configure(activeforeground="#000000")
        # self.restartalgo3.configure(background="#05ad27")
        # self.restartalgo3.configure(disabledforeground="#a3a3a3")
        # self.restartalgo3.configure(foreground="#000000")
        # self.restartalgo3.configure(highlightbackground="#d9d9d9")
        # self.restartalgo3.configure(highlightcolor="black")
        # self.restartalgo3.configure(pady="0")
        # self.restartalgo3.configure(text='''Button''')
        # self.restartalgo3.configure(width=97)


if __name__ == '__main__':
    vp_start_gui()




