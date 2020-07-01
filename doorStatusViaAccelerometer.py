from microbit import *
import radio

radio.config(group=13, data_rate=radio.RATE_250KBIT, power=7)

doorOpen = False
statusChanged = False

while True:
    # Check to see if micro:bit is either 'face down' or 'face up' 
    # Check both to ensure door status is accurate with either side attached to the door
    if accelerometer.is_gesture('face down') or accelerometer.is_gesture('face up'):
        if not doorOpen:
            doorOpen = True
            statusChanged = True
    else:
        if doorOpen:
            doorOpen = False
            statusChanged = True
    print(doorOpen)
    
    # Only send door status to Receiver if it changed 
    if statusChanged:
        radio.on()
        radio.send(str(doorOpen))
        radio.off()
        statusChanged = False
    sleep(500)
