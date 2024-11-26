from microbit import *
import radio
import music

radio.on()


while True:
    message = radio.receive()

    if message == 'endormi':
        display.show(Image.ASLEEP)  
    elif message == 'agité':
        display.show(Image.MEH)  
    elif message == 'très agité':
        music.play(music.POWER_DOWN)
        display.show(Image.NO)

    sleep(200)