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
2. Memory Error ka safeguard
3. Plotting ka format consistent karna hai
4. If no file already then CSV is created after script stops
"""

column, current_time, figure, axes, csvList, csvCounter, isPlotChanged = None, None, None, None, None, None, None
x_lim, store, flag, check, y, df, plotList, isCSVChanged, timer = None, None, None, None, None, None, None, None, None


# def createList():
#    global plotList
#    plotList = []


def copyList(list1, list2):
    list1 = list2.copy()


def initialise():
    global column, current_time, figure, axes, x_lim, store, flag, check, y, plotList, csvList, csvCounter, isCSVChanged, timer, isPlotChanged

    plotList = []
    csvList = []
    x_lim = []
    isCSVChanged = False
    isPlotChanged = False
    store = 0
    timer = 0
    csvCounter = 0
    flag = 1
    check = []
    current_time = 0

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
    global y, df, column, current_time, axes, plotList, isPlotChanged, timer
    if isPlotChanged:
        l = plotList[current_time]
    else:
        l = [0, 0, 0, 0]

    y[column[index]].append(l[index])
    x = np.arange(timer)

    axes[index].clear()
    axes[index].plot(x, y[column[index]])
    axes[index].set_xlabel('Time (s)')


def animate(frame):
    global store, current_time, df, flag, isPlotChanged, timer
    timer += 1
    store += 1
    if current_time < len(plotList) - 1:
        current_time += 1
    else:
        isPlotChanged = False

    try:
        for index in range(4):
            plotter(index)
    except:
        sys.exit()

    if 35 < store:
        axesLabel(1)
        flag += 1

    axesLabel(2)


def transferInfo(valueList):
    global isCSVChanged, isPlotChanged
    print(valueList)
    plotList.append(valueList)
    isPlotChanged = True
    info = {
        "TEMPERATURE": valueList[0],
        "ALTITUDE": valueList[1],
        "AVG SPEED": valueList[2],
        "PRESSURE": valueList[3],
    }
    csvList.append(info)
    isCSVChanged = True
    print(info)


def reader():
    global isPlotChanged
    plotList.append("TEMPERATURE,ALTITUDE,AVG SPEED,PRESSURE")

    while True:
        try:
            ser = serial.Serial(port='COM9', baudrate=9600, bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE, timeout=3)
        except:
            continue

        time.sleep(3)   # Logic???

        try:
            ser.isOpen()
            print("Serial port is open")
        except:
            print("Error - Serial Port not Open")
            exit()

        if ser.isOpen():
            try:
                while True:
                    time.sleep(1)
                    data = ser.readline().decode('ascii')
                    valueList = list(map(int, data[:-2].split(',')))
                    valueList = valueList[7:11]
                    transferInfo(valueList)
            except:
                print(csvList)
                print("Error - Not able to read data")
        else:
            print("Cannot Open Serial Port")


def animationPlot():
    plot = animation.FuncAnimation(figure, animate, interval=1000)
    figure.tight_layout(pad=2)
    show()


def csvMaker():
    global isCSVChanged, csvList
    fieldnames = ["TEMPERATURE", "ALTITUDE", "AVG SPEED", "PRESSURE"]
    t = 1
    with open('writtenData.csv', 'a') as datafile1:
        csv_writer = csv.DictWriter(datafile1, fieldnames=fieldnames)
        while True:
            if isCSVChanged:
                isCSVChanged = False
                if t:
                    csv_writer.writerows(csvList)
                else:
                    csv_writer.writerow(csvList[-1])


if __name__ == '__main__':
    initialise()
    readerThread = threading.Thread(target=reader)
    readerThread.start()
    time.sleep(4)
    plotterThread = threading.Thread(target=animationPlot())  # Plotter depending on plotList
    plotterThread.start()
#    csvThread = threading.Thread(target=csvMaker())  # csvWriter depending on csvList
#    csvThread.start()
