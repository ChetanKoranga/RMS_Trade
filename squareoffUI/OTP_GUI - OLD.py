import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, OptionMenu, StringVar
import csv




win = tk.Tk()
win.geometry("540x400")  



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
  
# leftframe = tk.Frame(win)  
# leftframe.pack(side = LEFT)  
  
# rightframe = tk.Frame(win)  
# rightframe.pack(side = RIGHT)
win.title("Algo wise OTP Confirmation")

Frame1 = tk.Frame(win)
Frame1.place(relx=0.05, rely=0.06,relheight=0.878, relwidth=0.908)
Frame1.configure(relief='groove')
Frame1.configure(borderwidth="2")
Frame1.configure(relief="groove")
Frame1.configure(background="#d9d9d9")


# label = tk.Label(frame, text="Algo Name: ")
Label1 = tk.Label(Frame1)
Label1.place(relx=0.082, rely=0.103, height=25, width=85)
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
textclient.place(relx=0.3, rely=0.108, height=24, width=150)


Label2 = tk.Label(Frame1)
Label2.place(relx=0.082, rely=0.275, height=25, width=85)
Label2.configure(background="#d9d9d9")
Label2.configure(disabledforeground="#a3a3a3")
Label2.configure(font=font12)
Label2.configure(foreground="#000000")
Label2.configure(text='''Enter OTP: ''')

input_var = StringVar()
input_entyBox = ttk.Entry(win, width =16, textvariable = input_var) 
input_entyBox.place(relx=0.32, rely=0.300, height=24, width=150)

def action():
    getOTP = input_var.get()
    algoName = var_algo.get()
    print(f"{getOTP}") 
    print(f"{algoName}")

    input_entyBox.delete(0, tk.END)

    with open(rf"C:\Users\Mudraksh_Server1\Desktop\ServerCodes\Symphony Order Server Dealer 2.0\Allowed algos\\{algoName}.txt", "w") as f:
        f.write(f"{getOTP}")

Button1 = tk.Button(Frame1)
Button1.place(relx=0.30, rely=0.56, height=64, width=167)
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
