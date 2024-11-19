from microbit import *

while True:
    if display.read_light_level() < 100:  
        display.show(Image("10101:01110:11111:01110:10101"))
    else:
        display.clear()
    sleep(100)  
