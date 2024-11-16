from microbit import *
import radio
import music

radio.on()
radio.config(group=1)

while True:
    incoming = radio.receive()
    if incoming:
        if "Alerte" in incoming:
            if "bebe a trop chaud" in incoming:
                music.play(music.POWER_DOWN)
            elif "bebe a trop froid" in incoming:
                music.play(music.POWER_UP)
        display.scroll(incoming, delay=100)
