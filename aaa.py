import PySimpleGUI as sg
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib
import math
import time
from tkinter import *

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

matplotlib.rcParams['text.color'] = '#F6C350'
matplotlib.rcParams['axes.labelcolor'] = '#F6C350'
matplotlib.rcParams['xtick.color'] = '#F6C350'
matplotlib.rcParams['ytick.color'] = '#F6C350'

sg.theme('DarkBrown5')   # Add that fresh Florida Tech color scheme

matplotlib.use('TkAgg')


# Some example data to display
x = np.linspace(0, 2 * np.pi, 400)
y = np.sin(x ** 2)

xList = []
yList = []
yList2 = []

fig, (ax1, ax2) = plt.subplots(1,2)

ax1.plot(xList, yList)
ax2.plot(xList, yList)

column_1=[[sg.Text("Real-Time Data:"), sg.Button("Export Data", key="-EXPORT2-"), sg.Button("Close", key="-CLOSE2-", )], [sg.Canvas(key='-CANVAS2')]]

layout = [[sg.Column(column_1)]]

window2 = sg.Window("Engine Data Test", layout, finalize=True)
window2.force_focus()

fig_canvas_agg = draw_figure(window2["-CANVAS2"].TKCanvas, fig)

event, values = window2.read()

column_3=[[sg.Text("Export as:")], [sg.Button("CSV", key="-CSV-")], [sg.Button("TXT", key="-TXT-")]]
layout2 = [[sg.Column(column_3)]]
i=0
while i < 100:
    xList.append(x[i])
    yList.append(y[i])
    yList2.append(y[i]/2)
    ax1.clear()
    ax2.clear()
    ax1.plot(xList, yList, label = "1")
    ax2.plot(xList, yList2, label = "2")
    fig_canvas_agg.draw()
    time.sleep(0.1)
    i += 1


if event == "-CLOSE2-":
    window2.close()
if event == "-EXPORT2-":
    window3 = sg.Window("Export Data", layout2, finalize=True)
    window3.force_focus()
    event2, values2 = window3.read()
    if event2 == "-CSV-":
        print("Exporting as CSV...")
        window3.close()
    if event2 == "-TXT-":
        print("Exporting as TXT...")
        window3.close()