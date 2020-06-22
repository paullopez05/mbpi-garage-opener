from microbit import *
import radio

powerLevel = 0

radio.config(group=13, power=powerLevel, data_rate=radio.RATE_250KBIT)

while True:
    if button_a.was_pressed():
        radio.on()
        display.show(Image.NO, delay=500, clear=True)
        radio.send('A')
        radio.off()
    if button_b.was_pressed():
        if powerLevel < 7:
            powerLevel += 1
        else:
            powerLevel = 0
        radio.config(power=powerLevel)
        display.show(str(powerLevel), delay=500, clear=True)