# Imports go at the top
from microbit import *
import radio
import music


radio.on()
radio.config(group=3)

def length(message):
    if message:
        nb_de_carctère = len(message)

 
# Code in a 'while True:' loop repeats forever
while True:
    message = radio.receive()
    if message == "jouer":
        display.show(Image.HAPPY)
    elif message == "lait":
        display.show(Image.SAD)

        
        

        
