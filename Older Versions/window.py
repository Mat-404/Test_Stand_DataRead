import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import matplotlib.figure as mplfig
import tkinter as tk

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

if __name__ == '__main__':
    figs = [mplfig.Figure(figsize=(6, 2), dpi=100),
          mplfig.Figure(figsize=(4, 2), dpi=100)]
    axs = [f.add_subplot(111) for f in figs]
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    ys = [[3, 5, 2, 7, 3, 5, 4, 6, 2, 2],
          [6, 1, 4, 9, 4, 2, 5, 1, 2, 4]]
    lines = [ax.plot(x, ys[i])[0] for i, ax in enumerate(axs)]
    for ax in axs:
        ax.set_ylim([0, 10])

    

    app = Calculator()
    app.geometry('1280x720')
    app.configure(bg='#af9878')
    anis = [animation.FuncAnimation(f, animate, interval=1000, fargs=[line])
            for f, line in zip(figs,lines)]
    app.mainloop()