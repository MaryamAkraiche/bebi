from microbit import *
import radio
import music
import random
radio.on()
radio.config(group = 3)

def bruits_de_fonds():
    speaker.on()
    freq = random.randint(300, 600)
    music.pitch(freq, 50)

def music_mélodie():
    speaker.on()
    mélodie = [
    'C4:4', 'D4:4', 'E4:4', 'F4:2', 'E4:2',  
    'E4:4', 'F4:4', 'G4:4', 'A4:2', 'G4:2', 
    'G4:4', 'A4:4', 'B4:4', 'C5:2', 'B4:2',  
    'A4:4', 'G4:4', 'F4:4', 'E4:2', 'D4:2' 
    ]
    music.play(mélodie)
    
while True:
    if microphone.sound_level() >200: 
        radio.send("Attention, bebe pleure !") 
        
        if radio.receive() == "musique": 
            music_mélodie()
        elif radio.receive() == "bruits":  
            bruits_de_fonds()
        elif radio.receive() == "rien:" : 
            pass
    else:
        pass


    
    