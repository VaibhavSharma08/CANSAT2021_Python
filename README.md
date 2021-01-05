# CANSAT2021_Kalpana_Python
This repository contains the code for Reading, Plotting and Writing data.

**Reading** - Reads from Arduino connected through Serial Port. Currently COM9 on my computer. (Change if needed)

**Plotting** - Plots the data read from the Arduino with matplotlib. Plots 0 if no data received. Starts plotting again when the data is again received.

**Writing** - Writes the data read from the Arduino to a CSV file. Look at writtenData.csv for sample.


**Process:** 

Data from Arduino -> Read by reader() module -> Stored in 2 lists -> plottingList and csvList (one for plotting and one for writing to CSV) 

plottingList -> Data plotted using matplotlib

csvList -> Data written to CSV file every 4 seconds


**Currently all 3 modules are fully functional and integrated.**

**For running code, download and execute "requirements.txt" and "main.py" in this order. Also download the telemetry folder and upload the .ino file to Arduino**


**Issues:**

****0. Whenever disconnect and reconnect, why does it always start from packet 1?****

1. matplotlib ke through transition and movement fix karo....  ------ DONE
2. Implement memory safeguards against Memory Errors being caused due to list becoming full ------ DONE
3. CSV aur plotting dono mein 0000 direct append ho ---- csv mein nhi karna
4. CSV mein disconnect aur connect par number of 0000 packets not equal to ideally received packets ---- append nhi karna toh np
5. What is the policy on missed packets? ---- plotting mein 0, csv mein nhi, missed packets counted by packet number


**Created By: Vaibhav Sharma**

**Created For: Team Kalpana for CANSAT 2021**
