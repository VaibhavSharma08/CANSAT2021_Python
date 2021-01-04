import matplotlib.animation as animation
import numpy as np
from matplotlib.pyplot import show, subplots
import serial
import time
import csv
import threading
from matplotlib import style
import sys
import datetime
import largeList

"""
ISSUES: 
1. Agar arduino se delay toh not writing to CSV ---- DONE
2. Memory Error ka safeguard
3. Plotting ka format consistent karna hai    ----- DONE
4. If no file already then CSV is created after script stops
"""

column, current_time, figure, axes, csvList, csvCounter, isPlotChanged = None, None, None, None, None, None, None
x_lim, shownOnScreen, flag, check, y, df, plotList, timer, csvLen = None, None, None, None, None, None, None, None, None


# def createList():
#    global plotList
#    plotList = []


def copyList(list1, list2):
    list1 = list2.copy()


def initialise():
    global column, csvLen, current_time, figure, axes, x_lim, shownOnScreen, flag, check, y, plotList, csvList, csvCounter, timer, isPlotChanged

    plotList = []
    csvList = []
    x_lim = []
    isPlotChanged = False
    shownOnScreen = 0
    timer = 0
    csvCounter = 0
    csvLen = 0
    flag = 1
    check = []
    current_time = 0

    column = np.array(['TEMPERATURE', 'ALTITUDE', 'AVG SPEED', 'PRESSURE'])
    figure, axes = subplots(nrows=1, ncols=4, figsize=(22, 5))
    figure.suptitle('Data Plots', fontsize=24)
    style.use('fivethirtyeight')

    y = {'TEMPERATURE': [], 'ALTITUDE': [], 'AVG SPEED': [], 'PRESSURE': []}


def axesLabel(i):
    global flag, shownOnScreen, axes

    if i == 1:
        axes[0].set_xlim(flag, flag + shownOnScreen)
        axes[1].set_xlim(flag, flag + shownOnScreen)
        axes[2].set_xlim(flag, flag + shownOnScreen)
        axes[3].set_xlim(flag, flag + shownOnScreen)

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
    global shownOnScreen, current_time, df, flag, isPlotChanged, timer
    timer += 1
    shownOnScreen += 1
    if current_time < len(plotList) - 1:
        current_time += 1
    else:
        isPlotChanged = False

    try:
        for index in range(4):
            plotter(index)
    except:
        sys.exit()

    if 35 < shownOnScreen:
        axesLabel(1)
        flag += 1

    axesLabel(2)


def convertTime(unixTime):
    actualTime = datetime.datetime.fromtimestamp(unixTime).strftime('%Y-%m-%d %H:%M:%S')
    return actualTime


def transferInfo(valueList):
    global isPlotChanged
    appendList = valueList[7:11].copy()
    valueList[1] = convertTime(valueList[1])
    print(appendList)
    plotList.append(appendList)
    isPlotChanged = True
    csvList.append(valueList.copy())
    # print(info)


def reader():
    global isPlotChanged
    plotList.append("TEMPERATURE,ALTITUDE,AVG SPEED,PRESSURE")
    print("Reader Thread running")

    while True:
        try:
            ser = serial.Serial(port='COM9', baudrate=9600, bytesize=serial.EIGHTBITS,
                                parity=serial.PARITY_NONE, timeout=3)
        except:
            continue

        time.sleep(3)  # Logic???

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
                    transferInfo(valueList)
            except:
                print(csvList)
                print("Error - Not able to read data")
        else:
            print("Cannot Open Serial Port")


def animationPlot():
    print("Animation running")
    figure.tight_layout(pad=2)
    plot = animation.FuncAnimation(figure, animate, interval=1000)
    show()


def csvMaker():
    global csvList, plotList, csvLen
    fieldnames = ["<TEAM_ID>", "<MISSION_TIME>", "<PACKET_COUNT>", "<PACKET_TYPE>", "<MODE>", "<SP1_RELEASED>",
                  "<SP2_RELEASED>", "TEMPERATURE", "ALTITUDE", "AVG SPEED", "PRESSURE", "<GPS_LATITUDE>",
                  "<GPS_LONGITUDE>", "<GPS_ALTITUDE>", "<GPS_SATS>", "<SOFTWARE_STATE>", "<SP1_PACKET_COUNT>",
                  "<SP2_PACKET_COUNT>", "<CMD_ECHO>"]
    firstTimeCSV = 1
    print("CSV Thread Running \n")

    with open('writtenData.csv', 'w',  newline='') as csvFile:
        csv_writer = csv.writer(csvFile)
        csv_writer.writerow(fieldnames)
        while True:
            time.sleep(6)   # 6n seconds = 6n +- 1 packets
            if firstTimeCSV:
                firstTimeCSV = False
                csv_writer.writerows(csvList)
                csvLen = len(csvList)
                csvFile.flush()
            else:
                csv_writer.writerows(csvList[csvLen:])
                csvLen = len(csvList)
                csvFile.flush()


if __name__ == '__main__':
    initialise()
    readerThread = threading.Thread(target=reader)
    csvThread = threading.Thread(target=csvMaker)  # csvWriter depending on csvList

    readerThread.start()
    time.sleep(4)
    csvThread.start()
    animationPlot()         # Plotter depending on plotList
