import random
import music
import radio
from microbit import *


icons_flamme = Image("00000:" "00800:" "08880:" "88888:" "08880")
icons_flocons = Image("80808:" "08880:" "88088:" "08880:" "80808")
icons_milk = Image("00800:" "08080:" "08080:" "08080:" "08880:")
icons_light = Image("00800:" "08880:" "88888:" "08880:" "00800:")
icons_temperature = Image("00800:" "08888:" "00800:" "00800:" "00088:")
icons_sound = Image("08888:" "08008:" "08008:" "88088:" "88088:")
icons_musiquemode = Image("00800:" "00800:" "00800:" "08800:" "08800:")
icons_state = Image("88888:" "88888:" "88888:" "88888:" "88888:")


milk_quantity = "0"
listening_mode = 0
menu_mode = 1




def hashing(string):
    """
    Hachage d'une chaîne de caractères fournie en paramètre.
    Le résultat est une chaîne de caractères.
    Attention : cette technique de hachage n'est pas suffisante (hachage dit cryptographique) pour une utilisation en dehors du cours.
    :param (str) string: la chaîne de caractères à hacher
    :return (str): le résultat du hachage
    """

    def to_32(value):
        """
        Fonction interne utilisée par hashing.
        Convertit une valeur en un entier signé de 32 bits.
        Si 'value' est un entier plus grand que 2 ** 31, il sera tronqué.


        :param (int) value: valeur du caractère transformé par la valeur de hachage de cette itération
        :return (int): entier signé de 32 bits représentant 'value'
        """
        value = value % (2**32)
        if value >= 2**31:
            value = value - 2**32
        value = int(value)
        return value

    if string:
        x = ord(string[0]) << 7
        m = 1000003
        for c in string:
            x = to_32((x * m) ^ ord(c))
        x ^= len(string)
        if x == -1:
            x = -2
        return str(x)
    return ""


def vigenere(message, key, decryption=False):
    text = ""
    key_length = len(key)
    key_as_int = [ord(k) for k in key]

    for i, char in enumerate(str(message)):
        # Letters encryption/decryption
        if char.isalpha():
            key_index = i % key_length
            if decryption:
                modified_char = chr((ord(char.upper()) - key_as_int[key_index] + 26) % 26 + ord("A"))
            else:
                modified_char = chr((ord(char.upper()) + key_as_int[key_index] - 26) % 26 + ord("A"))
            # Put back in lower case if it was
            if char.islower():
                modified_char = modified_char.lower()
            text += modified_char
        # Digits encryption/decryption
        elif char.isdigit():
            key_index = i % key_length
            if decryption:
                modified_char = str((int(char) - key_as_int[key_index]) % 10)
            else:
                modified_char = str((int(char) + key_as_int[key_index]) % 10)
            text += modified_char
        else:
            text += char
    return text


def send_packet(key, message_type, message):
    """
    Envoi de données fournies en paramètres
    Cette fonction permet de construire, de chiffrer puis d'envoyer un paquet via l'interface radio du micro:bit


    :param (str) key:       Clé de chiffrement
           (str) type:      Type du paquet à envoyer
           (str) content:   Données à envoyer
        :return none
    """
    packet = "{}|{}|{}".format(message_type, str(len(message)), message)  # format T|L|V
    encrypted_packet = vigenere(packet, key)
    radio.send(str(encrypted_packet))


def unpack_data(encrypted_packet, key):
    """
    Déballe et déchiffre les paquets reçus via l'interface radio du micro:bit
    Cette fonction renvoit les différents champs du message passé en paramètre


    :param (str) encrypted_packet: Paquet reçu
           (str) key:              Clé de chiffrement
        :return (srt)type:             Type de paquet
            (int)length:           Longueur de la donnée en caractères
            (str) message:         Données reçue
    """
    return vigenere(encrypted_packet, key, decryption=True)


def receive_packet(packet_received, key):
    """
    Traite les paquets reçus via l'interface radio du micro:bit
    Cette fonction utilise la fonction unpack_data pour renvoyer les différents champs du message passé en paramètre
    Si une erreur survient, les 3 champs sont retournés vides


    :param (str) packet_received: Paquet reçue
           (str) key:              Clé de chiffrement
        :return (srt)type:             Type de paquet
            (int)lenght:           Longueur de la donnée en caractère
            (str) message:         Données reçue
    """
    decrypted_packet = unpack_data(packet_received, key)
    return decrypted_packet.split("|")


def send_temperature():
    room_temperature = str(temperature())
    send_packet(key=hashing("1"), message_type="0", message=room_temperature)
    display.scroll(room_temperature)


def get_temperature():
    room_temperature = str(temperature())
    return room_temperature


def send_continuous_temperature():
    while True:
        send_temperature()
        sleep(10000)


def activate_light():
    if display.read_light_level() < 100:
        display.show(Image("80808:08880:88888:08880:80808"))
    else:
        display.clear()


def deactivate_light():
    display.clear()


def play_noise():
    # speaker.on()
    # freq = random.randint(300, 600)
    # music.pitch(freq, 50)
    music.pitch(130, duration=100)
    sleep(100)
    music.pitch(85, duration=200)
    sleep(800)


def play_music(melody):
    speaker.on()
    melody1 = [
        "C4:4",
        "D4:4",
        "E4:4",
        "F4:2",
        "E4:2",
        "E4:4",
        "F4:4",
        "G4:4",
        "A4:2",
        "G4:2",
        "G4:4",
        "A4:4",
        "B4:4",
        "C5:2",
        "B4:2",
        "A4:4",
        "G4:4",
        "F4:4",
        "E4:2",
        "D4:2",
    ]
    melody2 = [
        "A5:2",
        "B5:2",
        "C6:6",
        "G5:2",
        "G5:2",
        "D6:4",
        "R:4",
        "C6:2",
        "A5:2",
        "A5:2",
        "A5:4",
        "A5:1",
        "B5:2",
        "C6:4",
        "R:3",
        "A5:2",
        "B5:2",
        "C6:4",
        "R:2",
        "A5:4",
        "E6:2",
        "D6:4",
        "R:2",
        "C6:2",
        "D6:2",
        "E6:2",
        "E6:4",
        "F6:4",
        "D6:4",
        "R:2",
        "C6:2",
        "R:2",
        "G6:6",
        "E6:6",
        "D6:6",
        "R:2",
        "C6:3",
        "C6:4",
        "G6:6",
        "E6:6",
        "C6:6",
        "R:4",
        "C6:4",
        "C6:4",
        "B5:4",
        "G5:6",
        "G5:4",
        "R:4",
        "F5:2",
        "F5:2",
        "F5:2",
        "E5:2",
        "F5:2",
        "E5:2",
        "F5:2",
        "F5:2",
        "E5:4",
        "C5:4",
    ]
    melody3 = [
        "A#5:6",
        "G6:6",
        "R:2",
        "F6:4",
        "R:2",
        "G6:4",
        "F6:4",
        "D#6:3",
        "R:2",
        "A#5:4",
        "G6:4",
        "C#6:1",
        "C6:1",
        "B5:1",
        "C6:1",
        "C7:6",
        "G6:4",
        "R:1",
        "A#6:10",
        "G#6:8",
        "G6:2",
        "R:1",
        "F6:6",
        "G6:6",
        "D6:4",
        "D#6:6",
        "R:2",
        "C6:6",
        "A#5:6",
        "R:2",
        "D7:6",
        "C7:4",
        "R:1",
        "A#6:2",
        "G#6:2",
        "G6:2",
        "G#6:2",
        "C6:2",
        "D6:2",
        "D#6:8",
        "A#5:8",
        "G6:8",
        "F6:2",
        "G6:2",
        "F6:2",
        "E6:2",
        "F6:2",
        "G6:2",
        "F6:4",
        "D#6:6",
        "R:1",
        "F6:2",
        "D#6:2",
        "D6:2",
        "D#6:2",
        "F6:2",
        "F#6:2",
        "B5:2",
        "C6:2",
        "C#6:2",
        "C6:2",
        "F6:2",
        "E6:2",
        "G#6:2",
        "G6:2",
        "C#7:2",
        "C7:2",
        "G6:4",
        "A#6:6",
        "G#6:6",
        "G6:6",
        "F6:6",
        "G6:6",
        "D6:6",
        "D#6:6",
        "C6:8",
        "A#5:6",
        "D7:2",
        "C7:2",
        "A#6:2",
        "G#6:2",
        "G6:2",
        "G#6:2",
        "C6:2",
        "D6:2",
        "D#6:6",
    ]

    melodies = {
        "melody_1": melody1,
        "melody_2": melody2,
        "melody_3": melody3,
    }
    music.play(melodies[melody])


def send_state():
    AGITATION_FAIBLE = 2000
    AGITATION_MODEREE = 3000
    AGITATION_FORTE = 4000

    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()

    mouvement = abs(x) + abs(y) + abs(z)

    if mouvement <= AGITATION_FAIBLE:
        send_packet(key=hashing("1"), message_type="0", message="asleep")
    elif mouvement <= AGITATION_MODEREE:
        send_packet(key=hashing("1"), message_type="0", message="agitated")
    elif mouvement > AGITATION_FORTE:
        send_packet(key=hashing("1"), message_type="0", message="very agitated")


def get_state():
    AGITATION_FAIBLE = 2000
    AGITATION_MODEREE = 3000
    AGITATION_FORTE = 4000

    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()

    mouvement = abs(x) + abs(y) + abs(z)

    if mouvement <= AGITATION_FAIBLE:
        return "asleep"
    elif mouvement <= AGITATION_MODEREE:
        return "agitated"
    elif mouvement > AGITATION_FORTE:
        return "very agitated"


def set_milk_quantity(message):
    global milk_quantity

    milk_quantity = message
    display.show(milk_quantity)
    sleep(1000)


def get_milk_quantity():
    global milk_quantity

    return milk_quantity


def handle_night_light():
    while True:
        if button_a.was_pressed():
            activate_light()
            sleep(1000)
        if button_b.was_pressed():
            deactivate_light()
            display.show(Image.NO)
            sleep(1000)
        if pin_logo.is_touched():
            break
    return


def play_sound():
    display.show(Image.YES)
    sleep(500)
    display.clear()
    while True:
        if button_a.was_pressed():
            display.show("M")
            sleep(1000)
            while True:
                sleep(100)
                if pin0.is_touched():
                    display.show("1")
                    play_music(melody="melody_1")
                    display.clear()
                    sleep(500)
                if pin1.is_touched():
                    display.show("2")
                    play_music(melody="melody_2")
                    display.clear()
                    sleep(500)
                if pin2.is_touched():
                    display.show("3")
                    play_music(melody="melody_3")
                    display.clear()
                    sleep(500)
                if button_a.was_pressed():
                    display.show("<")
                    sleep(500)
                    display.clear()
                    break
                sleep(100)
        if button_b.was_pressed():
            display.show("B")
            while True:
                sleep(100)
                play_noise()
                if button_a.was_pressed():
                    display.show("<")
                    sleep(500)
                    display.clear()
                    break
                sleep(100)
        if pin_logo.is_touched():
            break
    return


def menu():
    display.show("M")
    sleep(1000)
    images = [icons_milk, icons_light, icons_temperature, icons_sound, icons_state]
    value = ""
    current_index = 0

    # Generate a key
    key = hashing("1")

    while True:
        image = images[current_index]
        display.show(image)
        if button_a.was_pressed():
            value = image
            select_option(value)

        if button_b.was_pressed():
            current_index += 1
            sleep(100)

        if current_index >= len(images):
            current_index = 0

        if pin_logo.is_touched():
            sleep(1000)
            return listening_mode

        sleep(100)


def select_option(value):
    if value == icons_milk:
        milk_quantity = get_milk_quantity()
        display.show(milk_quantity)
        sleep(1000)
    elif value == icons_light:
        handle_night_light()
    elif value == icons_temperature:
        room_temperature = get_temperature()
        display.scroll(room_temperature)
    elif value == icons_sound:
        play_sound()
    return


def alert():
    room_temperature = int(get_temperature())
    baby_state = get_state()
    if room_temperature < 25 or room_temperature >= 30:
        return True, "TEMPERATURE"

    if baby_state == "very agitated":
        return True, "STATE"

    return False, ""


def listen():
    display.show("E")
    while True:
        sleep(100)
        if pin_logo.is_touched():
            sleep(1000)
            return menu_mode

        is_alert, alert_code = alert()
        if is_alert:
            send_packet(key=hashing("1"), message_type="9", message=alert_code)

        packet = receive_packet(radio.receive(), hashing("1"))
        if len(packet) < 3:
            sleep(1000)
            continue
        message_type, message_length, message = packet
        if message == "send_temperature":
            send_temperature()
        if message == "activate_light":
            activate_light()
        if message == "deactivate_light":
            deactivate_light()
        if message_type == "2":
            play_music(message)
        if message == "play_noise":
            play_noise()
        if message == "send_state":
            send_state()
        if message_type == "1":
            set_milk_quantity(message)

        sleep(100)


def main():
    radio.on()
    radio.config(group=3)
    display.show("E")

    current_state = listening_mode

    while True:
        if current_state == listening_mode:
            current_state = listen()
        elif current_state == menu_mode:
            current_state = menu()


main()
