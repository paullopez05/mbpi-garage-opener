from microbit import *
import radio

def logTemperature(ms, temp):
    # Read contents from existing file (if it exists) so that the new value can be appended before rewriting file
    # This needs to be done because MicroPython does not support appending to an existing file natively
    try:
        with open('temperature.log', 'r') as file:
            contents = file.read()
    except:
        contents = ''

    # Append time of temperature read (in milliseconds since micro:bit reboot) and temperature in Celsius
    contents = contents + str(ms) + '|' + str(temp) + '\n'
    
    # Rewrite entire temperature log including new reading
    with open('temperature.log', 'w') as file:
        file.write(contents)
        
# Initialize temperature logging variable so that we only log temperature every 30 minutes
logTempInterval_min = 30
logTempInterval_ms = logTempInterval_min * 60 * 1000
lastLogTemp_ms = -logTempInterval_ms
        
# Configure radio to ensure reliable communication with receiver micro:bit
radio.config(group=13, data_rate=radio.RATE_250KBIT, power=7)

doorOpen = False
statusChanged = False

while True:
    current_ms = running_time()

    # Determine if it's time to log current temperature
    if current_ms - lastLogTemp_ms > logTempInterval_ms:
        logTemperature(current_ms, temperature())
        lastLogTemp_ms = current_ms        

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
    
    # Only send door status to Receiver if it changed 
    if statusChanged:
        radio.on()
        radio.send(str(doorOpen))
        radio.off()
        statusChanged = False

    sleep(500)
