import serial
from datetime import datetime

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
ser.close()
ser.open()

log = open('log.txt', 'a')

while True:
    statusReceived = ser.readline()
    if str(statusReceived) != "b''":
        if str(statusReceived) == "b'True\\r\\n'":
            garageDoorStatus = 'Garage Door Open'
        elif str(statusReceived) == "b'False\\r\\n'":
            garageDoorStatus = 'Garage Door Closed'
        else:
            garageDoorStatus = 'Unknown Status Received'
        print(str(datetime.now()), garageDoorStatus)
        log.write(str(datetime.now()) + ': ' + garageDoorStatus + '\n')
        log.flush()
