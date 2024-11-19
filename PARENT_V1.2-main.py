from microbit import *
import radio
import time
import music

radio.on()
radio.config(group=3)

def out_of_range():
    last_received_time = time.ticks_ms()  # Enregistre le temps actuel
    message = radio.receive()
    
    if message == "ping":
        last_received_time = time.ticks_ms()  # Met à jour le temps du dernier message reçu

    # Vérifie si plus de 5 secondes se sont écoulées depuis le dernier message
    elif time.ticks_diff(time.ticks_ms(), last_received_time) > 5000:
        display.show("!Out Of Range!")             # Affiche un message pour signaler la perte de portée
    sleep(1000)

def temp():
    message = radio.receive()
    if message == "Alerte: Température trop élevée !":
        display.scroll("TEMPERATURE TROP ELEVEE !", delay=100)
    elif message == "Alerte: Température trop basse !":
        display.scroll("TEMPERATURE TROP BASSE !", delay=100)

"""def micro():
    if microphone.current_event() == SoundEvent.LOUD:
        radio.send("Attention: Bruit détecté")
        display.show(Image.HAPPY, delay=3000)
        display.show(Image.HEART, delay=3000)
    elif microphone.current_event() == SoundEvent.QUIET:
        radio.send("Aucun bruit détecté")

def light_lvl():
    if display.read_light_level() < 255:
        for y in range(5):
            for x in range(5):
                display.set_pixel(x,y,1)
    else:
        for y in range(5):
            for x in range(5):
                display.set_pixel(x,y,9)


while True:"""