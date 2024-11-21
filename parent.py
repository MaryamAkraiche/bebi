from microbit import *

milk_doses = 0
while True:
    if button_a.is_pressed() and button_b.is_pressed():
        milk_doses = 0  
        display.show("0") 
        sleep(500) 
    elif button_a.is_pressed():
        milk_doses += 1 
        display.show(str(milk_doses))
        sleep(500)
    elif button_b.is_pressed():
        if milk_doses > 0:
            milk_doses -= 1  
        display.show(str(milk_doses))
        sleep(500)
