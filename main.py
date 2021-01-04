import matplotlib.animation as animation
import numpy as np
import pandas as pd
from matplotlib.pyplot import show, subplots
import serial
import time
import csv
import threading
from matplotlib import style
import sys
import largeList

"""
ISSUES: 
1. Agar arduino se delay toh not writing to CSV


2. If no delay then pandas not reading from created CSV of reader()
3. When reader() creating CSV toh pandas cannot access
4. If no file already then CSV is created after script stops
5. TO DO: Pandas reading from stored list as a variable and plotting
6. Dynamically access CSV for read write -> tailf can be used
7. Arduino se data veryyyy inconsistent
"""

column, count_time, figure, axes, csvList, csvCounter = None, None, None, None, None, None
x_lim, store, flag, check, y, df, plotList = None, None, None, None, None, None, None


#def createList():
#    global plotList
#    plotList = []


def copyList(list1, list2):
    list1 = list2.copy()


def initialise():
    global column, count_time, figure, axes, x_lim, store, flag, check, y, plotList, csvList, csvCounter

    plotList = []
    csvList = []
    x_lim = []
    store = 0
    csvCounter = 0
    flag = 1
    check = []
    count_time = 0

    column = np.array(['TEMPERATURE', 'ALTITUDE', 'AVG SPEED', 'PRESSURE'])
    figure, axes = subplots(nrows=1, ncols=4, figsize=(22, 5))
    figure.suptitle('Data Plots', fontsize=24)
    style.use('fivethirtyeight')

    y = {'TEMPERATURE': [], 'ALTITUDE': [], 'AVG SPEED': [], 'PRESSURE': []}

    # row = ["TEMPERATURE","ALTITUDE","AVG SPEED","PRESSURE"]
    # with open('writtenData.csv', 'a') as datafile:
    #     csv_writer = csv.writer(datafile)
    #     csv_writer.writerow(row)


def axesLabel(i):
    global flag, store, axes

    if i == 1:
        axes[0].set_xlim(flag, flag + store)
        axes[1].set_xlim(flag, flag + store)
        axes[2].set_xlim(flag, flag + store)
        axes[3].set_xlim(flag, flag + store)

    if i == 2:
        axes[0].set_ylabel('Temperature (C)')
        axes[1].set_ylabel('Altitude (m)')
        axes[2].set_ylabel('Avg Speed (m/s)')
        axes[3].set_ylabel('Pressure (Pa)')


def plotter(index):
    global y, df, column, count_time, axes, plotList

    l = plotList[-1]

    y[column[index]].append(l[index])
    x = np.arange(count_time)

    axes[index].clear()
    axes[index].plot(x, y[column[index]])
    axes[index].set_xlabel('Time (s)')


def animate(frame):
    global store, count_time, df, flag
    count_time += 1
    store += 1

    try:
        for index in range(4):
            plotter(index)
    except:
        sys.exit()

    if 35 < store < 100:
        axesLabel(1)
        flag += 1
    # elif store > 100:  # Logic
    #    sys.exit()

    axesLabel(2)


def reader():
    ser = serial.Serial(port='COM9', baudrate=9600, bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE, timeout=3)

    time.sleep(3)
    # datafile1 = open('writtenData.csv', 'w')
    # datafile1.write("TEMPERATURE,ALTITUDE,AVG SPEED,PRESSURE\n")
    plotList.append("TEMPERATURE,ALTITUDE,AVG SPEED,PRESSURE")
    csvList.append("TEMPERATURE,ALTITUDE,AVG SPEED,PRESSURE")

    try:
        ser.isOpen()
        print("Serial port is open")
    except:
        print("Error - Serial Port not Open")
        exit()

    t = 1

    if ser.isOpen():
        try:
            while True:
                time.sleep(1)
                data = ser.readline().decode('ascii')
                valueList = list(map(int, data[:-2].split(',')))
                print(valueList)
                plotList.append(valueList)
                csvList.append(valueList)
                info = {
                    "TEMPERATURE": valueList[0],
                    "ALTITUDE": valueList[1],
                    "AVG SPEED": valueList[2],
                    "PRESSURE": valueList[3],
                }
                print(info)
                # print("abcdef")
                # print(dataWrite[:-1])
                # datafile.writerow(dataWrite)
        except Exception:
            print(plotList)
            print("Error - Not able to write data")
    else:
        print("Cannot Open Serial Port")


def animationPlot():
    plot = animation.FuncAnimation(figure, animate, interval=1000)
    figure.tight_layout(pad=2)
    show()


def csvMaker():
    fieldnames = ["TEMPERATURE", "ALTITUDE", "AVG SPEED", "PRESSURE"]
    with open('writtenData.csv', 'a') as datafile1:
        csv_writer = csv.DictWriter(datafile1, fieldnames=fieldnames)


if __name__ == '__main__':
    initialise()
    readerThread = threading.Thread(target=reader)
    readerThread.start()
#    print("abc")
    time.sleep(7)
    plotterThread = threading.Thread(target=animationPlot())  # Plotter depending on plotList
    plotterThread.start()
    csvThread = threading.Thread(target=csvMaker())  # Plotter depending on csvList
    csvThread.start()
