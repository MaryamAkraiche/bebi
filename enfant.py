from microbit import *
import radio

radio.on()
radio.config(group=1)

while True:
    room_temp = temperature() - 4
    radio.send("Temp: " + str(room_temp))
    
    if room_temp >= 25:
        radio.send("Alerte: bebe a trop chaud !")
        display.scroll("TEMPERATURE TROP ELEVEE !", delay=100)
    elif room_temp <= 20:
        radio.send("Alerte: bebe a trop froid !")
        display.scroll("TEMPERATURE TROP BASSE !", delay=100)
    else:
        display.clear()
    
    sleep(600000)

