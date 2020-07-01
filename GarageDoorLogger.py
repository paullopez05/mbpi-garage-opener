import serial
from datetime import datetime
import requests

ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
ser.close()
ser.open()

log = open('log.txt', 'a')
keyfile = open('IFTTT_key', 'r')
IFTTT_key = keyfile.readline()

while True:
    statusReceived = ser.readline()
    if str(statusReceived) != "b''":
        if str(statusReceived) == "b'True\\r\\n'":
            garageDoorStatus = 'Open'
        elif str(statusReceived) == "b'False\\r\\n'":
            garageDoorStatus = 'Closed'
        else:
            garageDoorStatus = 'Unknown Status Received'
        print(str(datetime.now()), 'Garage Door ' + garageDoorStatus)
        log.write(str(datetime.now()) + ': Garage Door ' + garageDoorStatus + '\n')
        requests.post('https://maker.ifttt.com/trigger/Garage_Door/with/key/' + IFTTT_key, params={"value1":garageDoorStatus,"value2":"none","value3":"none"})
        log.flush()
