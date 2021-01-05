import matplotlib.animation as animation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import csv
from matplotlib import style
import sys

column = np.array(['TEMPERATURE', 'ALTITUDE', 'AVG SPEED', 'PRESSURE'])

style.use('fivethirtyeight')

figure, axes = plt.subplots(nrows=1, ncols=4,figsize=(22,5))
figure.suptitle('Data Plots', fontsize=24)
style.use('fivethirtyeight')
x_lim = []
store = 0
flag = 1
check = []
y = {
    'TEMPERATURE' : [],
    'ALTITUDE' : [],
    'AVG SPEED' : [],
    'PRESSURE' : []
}

count_time = 0
def animate(i):
    df = pd.read_csv('vdk_cansat_team.csv')
    rows = df.shape[0]
    # print(rows)
    
    global count_time
    # print(df[column[0]][count_time])
    count_time += 1
    
    # print(x)
    global store
    
    store += 1
    global flag
    global y
    try:
        for index in range(4):   
            y[column[index]].append(df[column[index]][count_time])    
           
            x = np.arange(count_time)
            
            axes[index].clear()
            axes[index].plot(x,y[column[index]])
            axes[index].set_xlabel('Time (s)')
    except:
        sys.exit()

    if store > 25:
        axes[0].set_xlim(flag,flag+30)
        axes[1].set_xlim(flag,flag+30)
        axes[2].set_xlim(flag,flag+30)
        axes[3].set_xlim(flag,flag+30)
    flag += 1
    # elif store > 100:
    #     sys.exit()
            

    axes[0].set_ylabel('Temperature (C)')
    axes[1].set_ylabel('Altitude (m)')
    axes[2].set_ylabel('Avg Speed (m/s)')
    axes[3].set_ylabel('Pressure (Pa)')


    
ani = animation.FuncAnimation(figure, animate, interval=1000)
figure.tight_layout(pad=2)
plt.show()
