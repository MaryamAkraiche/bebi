# Imports go at the top
from microbit import *
import radio
import music

display.show(Image.DUCK)
music.play(music.JUMP_UP)
Lait = 0
while True:
    if button_a.was_pressed() == 1:
        display.scroll('Mode Lait Active', delay= 100)
        sleep(500)
        display.scroll("Rester appuyer pendant L'Allaitement", delay= 75)
        while button_a.is_pressed:
            display.scroll("Alaitement en cours")
            if button_a.is_pressed() is False:
                continue
        Lait += 1
        display.scroll(Lait)
