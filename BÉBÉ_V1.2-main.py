from microbit import *
import radio
import time

radio.on()
radio.config(group=3)

def out_of_range():
    radio.send("ping")
    sleep(1000)

def temp():
    room_temp = temperature() - 4
    radio.send("Temp: " + str(room_temp))
    
    if room_temp >= 25:
        radio.send("Alerte: Température trop élevée !")
        display.scroll(temperature(), delay=100)
    elif room_temp <= 20:
        radio.send("Alerte: Température trop basse !")
        display.scroll(temperature(), delay=100)

def micro():
    if microphone.current_event() == SoundEvent.LOUD:
        radio.send("Attention: Bruit détecté")
        display.show(Image.HAPPY, delay=3000)
        display.show(Image.HEART, delay=3000)
    """elif microphone.current_event() == SoundEvent.QUIET:
        radio.send("Aucun bruit détecté")"""

def light_lvl():
    if display.read_light_level() < 255:
        for y in range(5):
            for x in range(5):
                display.set_pixel(x,y,1)
    else:
        for y in range(5):
            for x in range(5):
                display.set_pixel(x,y,9)


while True:
    out_of_range()
    light_lvl()
    temp()
    micro()
    
