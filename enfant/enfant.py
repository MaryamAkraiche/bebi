# Imports go at the top
from microbit import *
import radio 

radio.on()
radio.config(group=3)



while True:
    radio.send("ping")
    sleep(1000)
    
    display.scroll(temperature()-4)
    if temperature()-4 >= 25:
        display.scroll("TEMPERATURE TROP ELEVE !")
    elif temperature()+4 <= 20:
        display.scroll("TEMPERATURE TROP BASSE !")
    
    