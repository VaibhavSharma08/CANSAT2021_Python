import serial
import time
ser = serial.Serial(port='/dev/tty.usbmodem141301',baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, timeout=2)
time.sleep(3)
datafile = open('datafile1.csv', 'w')

# To get data upon request
# def getvalues():
#     ser.write(b'g')
#     arduinodata = ser.readline().decode('ascii')
#     return arduinodata

try:
    ser.isOpen()
    print("Serial port is open")
except:
    print("Error")
    exit()

if ser.isOpen():
    try:
        while True:
            data = ser.readline().decode('ascii')
            print(data)
            datafile.write(data)
            # datafile.write('\n ')
    except Exception:
        print("Error")

else:
    print("cannot open serial port")

datafile.close()


# while 1:
#     userInput = input("Press Y to Start").lower()
#
#     if userInput == "y":
#         print(getvalues())