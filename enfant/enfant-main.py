# Imports go at the top
from microbit import *
import radio 

radio.on()
radio.config(group=3)
#identification du baby phone




#compteur de lait

#Température
while True:
    radio.send("ping")
    sleep(1000)
    
    display.scroll(temperature()-4)
    if temperature()-4 >= 25:
        radio.send("Bébé à trop chaud !")
        display.scroll("TEMPERATURE TROP ELEVEE !", delay=100)
    elif temperature()+4 <= 20:
        radio.send("Bébé à trop froid !")
        display.scroll("TEMPERATURE TROP BASSE !", delay=100)


    