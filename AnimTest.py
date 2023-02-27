import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import matplotlib.figure as mplfig
import tkinter as tk
import serial
import serial.tools.list_ports

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
        self.wm_title('Beam calculator')
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

try:
    ser = serial.Serial('COM11', 115200, timeout=10)
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
            else:
                axs[i].set_ylim([100, 120])
                axs.ylabel('Pressure (kPa)')
                axs.xlabel('Time (u)')

        app = Calculator()
        app.configure(background='#af9878')
        app.geometry('1280x720')
        anis = [animation.FuncAnimation(f, animate, interval=1000, fargs=[line])
                for f, line in zip(figs,lines)]
        app.mainloop()

except:
    print("Serial port failed to open.")