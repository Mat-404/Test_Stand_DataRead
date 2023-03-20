
import PySimpleGUI as sg
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import matplotlib
from tkinter import *

import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

serialInst = serial.Serial()

portList = []

for port in ports:
    portList.append(str(port))

print (portList)

#Define functions
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def select():
    if my_listbox.curselection() == ():
        my_label.config(text="Please Select a Port")
    else:
        my_label.config(text=my_listbox.get(ANCHOR))
        selectVar = my_listbox.get(ANCHOR)
        a = portList.index(selectVar)
        portVar = ports[a]
        root.destroy()

root = Tk()
root.geometry("500x300")
root['bg'] = '#741012'
root.title("Select a Port")

#Window Element Code
my_listbox = Listbox(root)
my_listbox['bg'] = '#af9878'
my_listbox.grid(row=1, column=1, padx=10, pady=10)
my_listbox.configure(background='#af9878', foreground='#741012', width=0)

for i in portList:
    my_listbox.insert(END, i)

my_text = Label(root, text="Select a Port to connect to:")
my_text.grid(row=0, column=1, padx=10, pady=10)

my_button = Button(root, text="Select Port", command=select)
my_button.grid(row=2, column=1, padx=10, pady=10)

portVar = ""

global my_label
my_label = Label(root, text="")

root.mainloop()

print(portVar)

serialInst.baudrate = 115200
serialInst.port = 'COM11'
serialInst.open()

timeVals = []
tempVals = []
forceVals = []

fig, (ax1, ax2) = plt.subplots(1,2)
matplotlib.rcParams['text.color'] = '#F6C350'
matplotlib.rcParams['axes.labelcolor'] = '#F6C350'
matplotlib.rcParams['xtick.color'] = '#F6C350'
matplotlib.rcParams['ytick.color'] = '#F6C350'

sg.theme('DarkBrown5')   # Add that fresh Florida Tech color scheme

matplotlib.use('TkAgg')

column_1=[[sg.Text("Real-Time Data:"), sg.Button("Export Data", key="-EXPORT2-"), sg.Button("Close", key="-CLOSE2-", )], [sg.Canvas(key='-CANVAS2')]]

layout = [[sg.Column(column_1)]]

column_3=[[sg.Text("Export as:")], [sg.Button("CSV", key="-CSV-")], [sg.Button("TXT", key="-TXT-")]]
layout2 = [[sg.Column(column_3)]]

ax1.plot(timeVals, tempVals, label = "Temperature vs Time")
ax1.set_title("Temperature vs Time")
ax1.set_ylim(0, 500)
ax1.set(xlabel='Time (s)', ylabel='Temperature (C)')
ax2.plot(timeVals, forceVals, label = "Load vs Time")
ax2.set_title("Load vs Time")
ax2.set_ylim(0, 200)
ax2.set(xlabel='Time (s)', ylabel='Load (kg)')

window2 = sg.Window("Engine Data Test", layout, finalize=True)
window2.force_focus()

fig_canvas_agg = draw_figure(window2["-CANVAS2"].TKCanvas, fig)

i = 0
while(i < 500):
    if serialInst.in_waiting:
        packet = serialInst.readline()
        # b'24.21,22.23,102.30\r\n'
        packet = packet.decode()
        packet = packet[:-2]
        # 24.21,22.23,102.30
        packetList = packet.split(",")
        # ['24.21', '22.23', '102.30']
        if i > 10:
            print(packetList)
            print(timeVals)
            print(tempVals)
            print(forceVals)
        i += 1

        # Take in data sequentially
        if  len(packetList) == 3 and float(packetList[1]) > 20:
            
            timeVals.append(float(packetList[0]))
            tempVals.append(float(packetList[1]))
            forceVals.append(float(packetList[2]))

        # Update the graph
        ax1.clear()
        ax2.clear()
        ax1.plot(timeVals, tempVals, label = "Temperature vs Time")
        ax1.set_title("Temperature vs Time")
        ax1.set_ylim(25, 55)
        ax1.set(xlabel='Time (s)', ylabel='Temperature (C)')
        ax2.plot(timeVals, forceVals, label = "Load vs Time")
        ax2.set_title("Load vs Time")
        ax2.set_ylim(0, 200)
        ax2.set(xlabel='Time (s)', ylabel='Load (kg)')
        fig_canvas_agg.draw()

        if i%2 == 0:
            window2.refresh()


event, values = window2.read()

if event == "-CLOSE2-":
    window2.close()
if event == "-EXPORT2-":
    window3 = sg.Window("Export Data", layout2, finalize=True)
    window3.force_focus()
    event2, values2 = window3.read()
    if event2 == "-CSV-":
        print("Exporting as CSV...")        
        file = open("data.csv", "w")
        file.truncate(0)
        for i in range(timeVals):
            file.write(str(timeVals[i]) + "," + str(tempVals[i]) + "," + str(forceVals[i]) + "\n")
        file.close()
        window3.close()
    if event2 == "-TXT-":
        print("Exporting as TXT...")
        file = open("data.txt", "w")
        file.truncate(0)
        for i in range(timeVals):
            file.write(str(timeVals[i]) + "," + str(tempVals[i]) + "," + str(forceVals[i]) + "\n")
        file.close()
        window3.close()
