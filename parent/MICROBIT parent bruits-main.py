from microbit import *
import music
import radio

radio.on()
radio.config(group = 3)

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
            
            
        
