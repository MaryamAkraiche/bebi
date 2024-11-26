from microbit import *
import radio

radio.on()
AGITATION_FAIBLE = 2000
AGITATION_MODEREE = 3000
AGITATION_FORTE = 4000

while True:
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()

    mouvement = abs(x) + abs(y) + abs(z)

    if mouvement < AGITATION_FAIBLE:
        radio.send('endormi')
    elif mouvement < AGITATION_MODEREE:
        radio.send('agité')
    elif mouvement > AGITATION_FORTE:
        radio.send('très agité')

    sleep(200)