from microbit import *
import radio
import time
import music

radio.on()
radio.config(group=3, power=7)
last_received_time = time.ticks_ms()
milk_doses = 0

def out_of_range():
    global last_received_time
    message = radio.receive()
    if message == "ping":
        last_received_time = time.ticks_ms()
    elif time.ticks_diff(time.ticks_ms(), last_received_time) > 5000:
        display.scroll("!Hors de porte!", delay=90, monospace=True)
        #METTRE UN SON D'ALERTE

def temp():
    message = radio.receive()
    if message == "Alerte: Température trop élevée !":
        display.scroll("TEMPERATURE TROP ELEVEE !", delay=100)
    elif message == "Alerte: Température trop basse !":
        display.scroll("TEMPERATURE TROP BASSE !", delay=100)

def micro():
    message = radio.receive()
    if message == "Attention: Bruit détecté":
        display.show(message)

#FONCTION PAS OPERATIONNEL
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
            light_lvl() #NE MARCHE PAS
        elif button_b.was_pressed():
            display.scroll("Desactive", delay=90, monospace=True)
            #BESOIN DE COMPLETER
        break

def lait():
    global milk_doses
    while not pin_logo.is_touched():
        if button_a.is_pressed() and button_b.is_pressed():
            milk_doses = 0
            sleep(500)
            display.show("0")
        elif button_a.is_pressed():
            milk_doses += 1
            sleep(500)
            display.show(str(milk_doses))
        elif button_b.is_pressed():
            if milk_doses > 0:
                milk_doses -= 1 
            sleep(500)
            display.show(str(milk_doses))

def menu():
    lst = ["Compteur de lait", "Luminosite auto.", "Regl. Temperature"]
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
        if stop:
            break
    if value and value[0] == "Compteur de lait":
        lait()
    elif value and value[0] == "Luminosite auto.": #PAS OPERATIONNEL
        light_lvl_menu()
    elif value and value[0] == "Regl. Temperature":
        ... #METTRE LA FONCTION CORRESPONDANTE PAS ENCORE CREER



while True:
    """out_of_range()""" #Désactivé temporairement dû à l'absence de l'autre microbit
    if pin_logo.is_touched():
        menu()