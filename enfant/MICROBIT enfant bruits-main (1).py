from microbit import *
import radio
import music
import random
radio.on()
radio.config(group = 3)

def bruits_de_fonds():
    speaker.on()
    freq = random.randint(300, 600)  # Fréquence aléatoire entre 300 et 600 Hz
    music.pitch(freq, 50)  # Son de courte durée

def music_mélodie():
    speaker.on()
    mélodie = ["C4:4", "E4:4", "G4:4", "C5:2"]
    music.play(mélodie)
    


while True:
    if microphone.sound_level() >200:    #les parents vont devoir choisir une option
        radio.send("Attention, bebe pleure !") 
        if radio.receive() == "musique":      #active un mélodie pour calmer le bébé
            music_mélodie()
        elif radio.receive() == "bruits":    #active les bruits de fonds rassurant le bébé
            bruits_de_fonds()
        elif radio.receive() == "rien:"               #si les parents ont envi de le réconforter  tt seuls
            pass
    else:
        pass


    
    