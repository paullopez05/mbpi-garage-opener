# Garage Door Sensor
The garage door sensor uses a BBC micro:bit running on batteries that will detect whether the door is open or closed based on the orientation of the board using the built-in accelerometer's gesture detection features.  When the status of the door changes, the micro:bit will transmit that event to a second micro:bit attached to a Raspberry Pi that acts as a hub for all local IoT home automation devices.  

Additionally, the micro:bit logs ambient temperature to the local filesystem of the micro:bit for testing purposes.  The temperature values may eventually be transmitted to the Raspberry Pi.

## Hardware
- BBC micro:bit
- 2 AAA batteries
- Battery holder
- Enclosure (protects the micro:bit and batteries attached to the garage door)

## Software
A MicroPython program written for the BBC micro:bit that detects board orientation which corresponds to garage door open/close status.  This app runs a continuous loop which sleeps for 500 ms every cycle to save battery power.  On each cycle, the is_gesture() method of the accelerometer will be queried to check is the board is 'face up' or 'face down' which will indicate that the garage door is open.  If the gesture value is either of these, the app will check to see if this status is different from the last known status and, if so, it will turn on the radio to send the updated status to the receiver micro:bit attached to the Raspberry Pi hub.

### Configuration Values
The following line configures the micro:bit radio so that it can reliably communicate with the receiver micro:bit attached to the Raspberry Pi hub.

`radio.config(group=13, data_rate=radio.RATE_250KBIT, power=7)`
- **group:** All micro:bits need to use the same group value in order to receive communication from each other (can be any value 0-255)
- **data_rate:** Set to the slowest possible value of `radio.RATE_250KBIT` in order to improve transmission reliability
- **power:** Set to the highest possible value to ensure that the signal travels far enough through any obstructions (i.e. walls)

Other configuation values:
- **sleep:** Set to 500 ms so that we conserve battery power by not querying the sensors too frequently
