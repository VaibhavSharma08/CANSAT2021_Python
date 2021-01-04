import csv
import random
import time

temp = random.randint(1, 200)
alt =  random.randint(3, 125)
speed = random.randint(0, 150)
p = random.randint(3, 125)

fieldnames = ["TEMPERATURE", "ALTITUDE", "AVG SPEED", "PRESSURE"]


store = 0
while store < 100:

    with open('vdk_cansat_team.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "TEMPERATURE": temp,
            "ALTITUDE": alt,
            "AVG SPEED": speed,
            "PRESSURE": p
        }

        csv_writer.writerow(info)
        print(temp, alt, speed,p)

        temp = random.randint(1, 200)
        alt =  random.randint(3, 125)
        speed = random.randint(0, 150)
        p = random.randint(3, 125)

    time.sleep(1)

# DHRUV CANSAT