from microbit import *
import radio
import time
import music

"""
Microbit Parent
"""

radio.on()
radio.config(group=3, power=7)
last_received_time = time.ticks_ms()
milk_doses = 0
flamme = Image("00000:"
               "00500:"
               "05550:"
               "55555:"
               "05550")
flocons = Image("50505:"
                "05550:"
                "55055:"
                "05550:"
                "50505")
compteur_de_lait = Image("00500:"
                         "50005:"
                         "50005:"
                         "50005:"
                         "55555:")
luminosité_auto = Image("00500:"
                        "05550:"
                        "55555:"
                        "05550:"
                        "00500:")
temperature = Image("00500:"
                    "05555:"
                    "00500:"
                    "00500:"
                    "00055:")
hors_de_portée = Image("00500:"
                       "00500:"
                       "00500:"
                       "00000:"
                       "00500:")
musique_bruits = Image("05555:"
                       "05005:"
                       "05005:"
                       "55055:"
                       "55055:")
def out_of_range():
    global last_received_time
    message = radio.receive()
    if message:
        last_received_time = time.ticks_ms()
        return False
    elif time.ticks_diff(time.ticks_ms(), last_received_time) > 5000:
        display.show(hors_de_portée, delay=90, monospace=True)
        music.play(music.DADADADUM)
        return True
def temp():
    message = radio.receive()
    if message == "Alerte: Température trop élevée !":
        display.show(flamme, delay=100)
        music.play(music.POWER_DOWN)
    elif message == "Alerte: Température trop basse !":
        display.show(flocons, delay=100)
        music.play(music.POWER_UP)
def micro():
    message = radio.receive()
    if message == "Attention: Bruit détecté":
        display.show(message)


def light_lvl():
    if display.read_light_level() < 255:
        for y in range(5):
            for x in range(5):
                display.set_pixel(x,y,1)
    else:
        for y in range(5):
            for x in range(5):
                display.set_pixel(x,y,9)

def light_lvl_menu():
    while not button_a.was_pressed() or not button_b.was_pressed():
        display.scroll("Appuyer sur A(active) ou B(desactive)", delay=90, monospace=True)
        if button_a.was_pressed():
            display.scroll("Active", delay=90, monospace=True)
            light_lvl() 
        elif button_b.was_pressed():
            display.scroll("Desactive", delay=90, monospace=True)
            break

def lait():
    global milk_doses
    while not pin_logo.is_touched():
        if button_a.is_pressed() and button_b.is_pressed():
            milk_doses = 0
            sleep(500)
            display.show("0")
        elif button_a.was_pressed():
            milk_doses += 1
            sleep(500)
            display.show(str(milk_doses))
        elif button_b.was_pressed():
            if milk_doses > 0:
                milk_doses -= 1 
            sleep(500)
            display.show(str(milk_doses))

def musique_et_bruits():
    while True:
        if radio.receive() == "Attention, bebe pleure !":
            audio.play(Sound.MYSTERIOUS)
            display.scroll("Bebe pleure !")
            if button_a.was_pressed():
                display.scroll("mode musique choisi")
                sleep(100)
                display.scroll("vous confirmez votre choix ?")
                if button_a.was_pressed():
                    display.scroll("mode musique active")
                    radio.send("musique")
                elif button_b.was_pressed():
                    pass          
            elif button_b.was_pressed():
                display.scroll("bruits de fonds choisi")
                sleep(100)
                display.scroll("vous confirmez votre choix ?")
                if button_a.was_pressed():
                    display.scroll("mode bruits de fonds active")
                    radio.send("bruits")
                elif button_b.was_pressed():
                    pass  
            elif pin_logo.is_touched():
                display.scroll("ne rien faire")
                radio.send("rien")
def menu():
    lst = [compteur_de_lait, luminosité_auto, temperature, musique_bruits]
    value = []
    stop = False
    for i in lst:
        while not button_a.was_pressed():
            display.scroll(i, delay=90, monospace=True)
            if button_b.was_pressed():
                value.clear()
                value.append(i)
                stop = True
                break
            elif button_a.is_pressed():
                stop = True
                break
        
    if value and value[0] == compteur_de_lait:
        lait()
    elif value and value[0] ==luminosité_auto: #PAS OPERATIONNEL
        light_lvl_menu()
    elif value and value[0] == temperature:
        temp()
    elif value and value[0] == musique_bruits:
        



while True:
    if pin_logo.is_touched():
        if out_of_range():
            break
        else:
            menu()