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

"""
ISSUES: 
** CSV aur plotting dono mein 0000 direct append ho
** CSV mein disconnect aur connect par number of 0000 packets not equal to ideally received packets
** What is the policy on missed packets?

1. Agar arduino se delay toh not writing to CSV ---- DONE
2. Memory Error ka safeguard --- DONE
3. Plotting ka format consistent karna hai    ----- DONE
4. Whenever I disconnect and reconnect, hamesha 1 se kyun shuru hota hai???
"""

column, current_time, figure, axes, csvList, csvCounter, isPlotChanged, csvTime, csvBuffer = None, None, None, None, None, None, None, None, None
x_lim, shownOnScreen, flag, check, y, df, plotList, timer, csvLen, readTime, plotClear, csvClear, plotBuffer = None, None, None, None, None, None, None, None, None, None, None, None, None


# def createList():
#    global plotList
#    plotList = []


def copyList(list1, list2):
    list1 = list2.copy()


def initialise():
    global column, csvLen, plotClear, csvClear, plotBuffer, csvBuffer, readTime, current_time, csvTime, figure, axes, x_lim, shownOnScreen, flag, check, y, plotList, csvList, csvCounter, timer, isPlotChanged

    plotList = []
    csvList = []
    x_lim = []
    plotBuffer = []
    csvBuffer = []
    isPlotChanged = False
    plotClear = False
    csvClear = False
    shownOnScreen = 0
    csvTime = 0
    readTime = 0
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
        yValues = plotList[current_time]
    else:
        yValues = [0, 0, 0, 0]

    y[column[index]].append(yValues[index])
    x = np.arange(timer)

    axes[index].clear()
    axes[index].plot(x, y[column[index]])
    axes[index].set_xlabel('Time (s)')


def clearPlotList():
    global shownOnScreen, current_time, df, flag, isPlotChanged, timer, plotClear, plotBuffer
    plotClear = True
    i = 0
    while current_time < len(plotList) - 1:
        plotList[i] = plotList[current_time]
        i += 1
        current_time += 1
    del plotList[i:]
    plotList.extend(plotBuffer.copy())
    plotClear = False
    plotBuffer.clear()
    current_time = 0


def animate(frame):
    global shownOnScreen, current_time, df, flag, isPlotChanged, timer, plotClear
    timer += 1
    if timer % 40 == 0:
        clearPlotList()
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
    global isPlotChanged, plotClear, csvBuffer, plotBuffer
    appendList = valueList[7:11].copy()
    valueList[1] = convertTime(valueList[1])
    print(appendList)
    if plotClear:
        plotBuffer.append(appendList)
    else:
        plotList.append(appendList)
    isPlotChanged = True
    if csvClear:
        csvBuffer.append(valueList.copy())
    else:
        csvList.append(valueList.copy())
    # print(info)


def reader():
    global readTime

    plotList.append("TEMPERATURE,ALTITUDE,AVG SPEED,PRESSURE")
    print("Reader Thread running")

    while True:
        try:
            ser = serial.Serial(port='COM9', baudrate=9600, bytesize=serial.EIGHTBITS,
                                parity=serial.PARITY_NONE, timeout=2)
        except:
            continue

        time.sleep(2)  # Logic???

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
                print("Error - Not able to read data")
        else:
            print("Cannot Open Serial Port")


def animationPlot():
    print("Animation running")
    figure.tight_layout(pad=2)
    plot = animation.FuncAnimation(figure, animate, interval=1000)
    show()


def csvMaker():
    global csvList, plotList, csvLen, csvTime, csvBuffer, csvClear
    fieldnames = ["<TEAM_ID>", "<MISSION_TIME>", "<PACKET_COUNT>", "<PACKET_TYPE>", "<MODE>", "<SP1_RELEASED>",
                  "<SP2_RELEASED>", "TEMPERATURE", "ALTITUDE", "AVG SPEED", "PRESSURE", "<GPS_LATITUDE>",
                  "<GPS_LONGITUDE>", "<GPS_ALTITUDE>", "<GPS_SATS>", "<SOFTWARE_STATE>", "<SP1_PACKET_COUNT>",
                  "<SP2_PACKET_COUNT>", "<CMD_ECHO>"]
    firstTimeCSV = True
    print("CSV Thread Running \n")

    with open('writtenData.csv', 'w', newline='') as csvFile:
        csv_writer = csv.writer(csvFile)
        csv_writer.writerow(fieldnames)
        while True:
            time.sleep(4)  # 4n seconds = 4n +- 1 packets
            csvTime += 1

            if csvLen == len(csvList):
                temp_list = csvList[-1].copy()
                temp_list[7] = 0
                temp_list[8] = 0
                temp_list[9] = 0
                temp_list[10] = 0
                csv_writer.writerow(temp_list)
                csvFile.flush()
                continue

            if csvTime % 5 == 0:
                csvClear = True
                i = 0
                while csvLen < len(csvList):
                    csvList[i] = csvList[csvLen]
                    i += 1
                    csvLen += 1
                del csvList[i:]
                csvList.extend(csvBuffer.copy())
                csvClear = False
                csvBuffer.clear()
                csvLen = i
                firstTimeCSV = True

            if firstTimeCSV:
                firstTimeCSV = False
                csv_writer.writerows(csvList)
                csvLen = len(csvList)
                csvFile.flush()
            else:
                csv_writer.writerows(csvList[csvLen:])
                csvLen = len(csvList)
                csvFile.flush()


def main():
    initialise()
    readerThread = threading.Thread(target=reader)
    csvThread = threading.Thread(target=csvMaker)  # csvWriter depending on csvList

    readerThread.start()
    time.sleep(4)
    csvThread.start()
    animationPlot()  # Plotter depending on plotList


if __name__ == '__main__':
    main()
