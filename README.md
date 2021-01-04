# CANSAT2021_Kalpana_Python
This repository contains the code for Reading, Plotting and Writing data.

**Reading** - Reads from Arduino connected through Serial Port. Currently COM9 on my computer. (Change if needed)

**Plotting** - Plots the data read from the Arduino with matplotlib. Plots 0 if no data received. Starts plotting again when the data is again received.

**Writing** - Writes the data read from the Arduino to a CSV file. Look at writtenData.csv for sample.


**Process:** 

Data from Arduino -> Read by reader() module -> Stored in 2 lists -> plottingList and csvList (one for plotting and one for writing to CSV) 

plottingList -> Data plotted using matplotlib

csvList -> Data written to CSV file every 6 seconds


**Currently all 3 modules are fully functional and integrated.**

**For running code, download and execute "requirements.txt" and "main.py" in this order. Also download the telemetry folder and upload the .ino file to Arduino**


**TO DO:**

1. Implement memory safeguards against Memory Errors being caused due to list becoming full. ------ DONE
2. 0000 packet should be automatically appended to csvList and plotList instead of having seperate conditions.
3. Policy on Missed/0000 packets?
4. Whenever disconnect and reconnect, why does it always start from packet 1?


**Created By: Vaibhav Sharma**

**Created For: Team Kalpana for CANSAT 2021**
