from microbit import *
import radio

radio.config(group=13, power=7, data_rate=radio.RATE_250KBIT)
radio.on()

counter = 0

while True:
    message = radio.receive()
    if message is not None:
        counter += 1
        display.show(Image.NO, delay=500, clear=True)
    if button_a.was_pressed():
        display.scroll(str(counter))
    if button_b.was_pressed():
        counter = 0