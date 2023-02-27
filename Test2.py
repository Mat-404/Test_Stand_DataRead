import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial
import serial.tools.list_ports

#initialize serial port
ser = serial.Serial()
ser.port = 'COM11' #Arduino serial port
ser.baudrate = 115200
ser.timeout = 10 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
	print("\nAll right, serial port now open. Configuration:\n")
	print(ser, "\n") #print serial parameters

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
timeVals = []
tempVals = []
pressVals = []


# This function is called periodically from FuncAnimation
def animate(i, timeVals, tempVals):


    #Aquire and parse data from serial port
    line=ser.readline()
    line = line.decode('utf-8') #convert to unicode
    packet = line[:-2]
        
    line_as_list = packet.split(',')
    if line_as_list[0] != "":
        timeVals.append(float(line_as_list[0]))
        tempVals.append(float(line_as_list[1]))
    # Draw x and y lists
    ax.clear()
    ax.plot(timeVals, tempVals, label="Temperature")

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Temperature Readings')
    plt.ylabel('Temperature (C)')
    plt.xlabel('Time (u)')
    plt.legend()
    plt.axis([1, None, 23, 25]) #Use for arbitrary number of trials

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(timeVals, tempVals), interval=5)
plt.show()