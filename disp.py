import PySimpleGUI as sg
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import matplotlib.figure as mplfig
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import *
from serial import Serial
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

portList = []

def animate(i, line):
    y = np.random.randint(10, size=len(x))
    line.set_ydata(y)
    return [line]

class Figure(tk.Frame):

    def __init__(self, parent, controller, f):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        canvas.draw()

class Calculator(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title('Temperature and Pressure Data')
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        for i, f in enumerate(figs):
            bfig = Figure(container, controller=self, f=f)
            bfig.grid(row=i, column=0, sticky="nsew")
            # give the rows equal weight so they are allotted equal size
            container.grid_rowconfigure(i, weight=1)
        # you need to give at least one row and one column a positive weight 
        # https://stackoverflow.com/a/36507919/190597 (Bryan Oakley)
        container.grid_columnconfigure(0, weight=1)

ser = serial.Serial()

for onePort in ports:
    try :
        ser = serial.Serial(onePort, 115200, timeout=10)
        ser.open()
        portList.append(str(onePort) + " - Active")
        ser.close()
    except:
        print("Serial port inactive.")

if len(portList) == 0:
    portList.append("No active ports found.")

root = Tk()
root.geometry("500x300")
root.resizable(False, False)
root.iconbitmap('Rocketry_Club_Logo.ico')
root['bg'] = '#741012'
root.title("Select a Port")

my_listbox = Listbox(root)
my_listbox['bg'] = '#af9878'
my_listbox.grid(row=1, column=0, padx=10, pady=10)
my_listbox.configure(background='#af9878', foreground='#741012', width=0)

portVar = ""

def select():
    if my_listbox.curselection() == ():
        my_label.config(text="Please Select a Port")
    elif my_listbox.curselection() != "(No active ports found.)":
        my_label.config(text=my_listbox.get(ANCHOR))
        selectVar = my_listbox.get(ANCHOR)
        a = portList.index(selectVar)
        portVar = ports[a]
        print(portVar)
        root.destroy()
    elif my_listbox.curselection() == "(No active ports found.)":
        my_label.config(text="No active ports found.")

my_text = Label(root, text="Select a Port to connect to:")
my_text.grid(row=0, column=0, padx=10, pady=10)

for i in portList:
    my_listbox.insert(END, i)

my_button = Button(root, text="Select Port", command=select)
my_button.grid(row=2, column=0, padx=10, pady=10)

photo = ImageTk.PhotoImage(file="Rocketry_Club_Logo.png")

tk.Label(root, image=photo).grid(row=1, column=2, padx=60, pady=10)


global my_label
my_label = Label(root, text="")

root.mainloop()

try:
    ser = serial.Serial('portVar', 115200, timeout=10)
    ser.open()

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    timeVals = []
    tempVals = []
    pressVals = []


    if __name__ == '__main__':

         #Aquire and parse data from serial port
        line=ser.readline()
        line = line.decode('utf-8') #convert to unicode
        packet = line[:-2]

        line_as_list = packet.split(',')
        if line_as_list[0] != "":
            timeVals.append(float(line_as_list[0]))
            tempVals.append(float(line_as_list[1]))
            pressVals.append(float(line_as_list[2]))

        figs = [mplfig.Figure(figsize=(6, 2), dpi=100),
              mplfig.Figure(figsize=(4, 2), dpi=100)]
        axs = [f.add_subplot(111) for f in figs]
        x = [timeVals]
        ys = [tempVals, pressVals]
        lines = [ax.plot(x, ys[i])[0] for i, ax in enumerate(axs)]
        for i in len(axs):
            if i == 0:
                axs[i].set_ylim([22, 28])
                axs.ylabel('Temperature (C)')
                axs.xlabel('Time (u)')
                axs[i].set(facecolor='#741012')
            else:
                axs[i].set_ylim([100, 120])
                axs.ylabel('Pressure (kPa)')
                axs.xlabel('Time (u)')
                axs[i].set(facecolor='#741012')

        app = Calculator()
        app.configure(background='#af9878')
        app.geometry('1280x720')
        anis = [animation.FuncAnimation(f, animate, interval=1000, fargs=[line])
                for f, line in zip(figs,lines)]
        app.mainloop()

except:
    print("Serial port failed to open.")