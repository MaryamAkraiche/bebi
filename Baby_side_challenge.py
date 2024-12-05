from microbit import *
import radio
import random
import music

#Can be used to filter the communication, only the ones with the same parameters will receive messages
#radio.config(group=23, channel=2, address=0x11111111)
#default : channel=7 (0-83), address = 0x75626974, group = 0 (0-255)
flamme = Image("00000:"
               "00500:"
               "05550:"
               "55555:"
               "05550")
flocons = Image("50505:"
                "05550:"
                "55055:"
                "05550:"
                "50505")

compteur_de_lait = Image("00500:"
                         "55055:"
                         "50005:"
                         "50005:"
                         "55555:")
veilleuse = Image("00500:"
                  "05550:"
                  "55555:"
                  "05550:"
                  "00500:")
temperature = Image("00500:"
                    "05555:"
                    "00500:"
                    "00500:"
                    "00055:")
hors_de_portée = Image("00500:"
                       "00500:"
                       "00500:"
                       "00000:"
                       "00500:")
musique_bruits = Image("05555:"
                       "05005:"
                       "05005:"
                       "55055:"
                       "55055:")
musiquemode = Image("00500:"
                    "00500:"
                    "00500:"
                    "05500:"
                    "05500:")
AGITATION_FAIBLE = 2000
AGITATION_MODEREE = 3000
AGITATION_FORTE = 4000
radio.on()
radio.config(group = 3)
def generate_key(seed):
    return hashing(seed)
key = generate_key(13)
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
		value = value % (2 ** 32)
		if value >= 2**31:
			value = value - 2 ** 32
		value = int(value)
		return value

	if string:
		x = ord(string[0]) << 7
		m = 1000003
		for c in string:
			x = to_32((x*m) ^ ord(c))
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
        key_index = i % key_length
        #Letters encryption/decryption
        if char.isalpha():
            if decryption:
                modified_char = chr((ord(char.upper()) - key_as_int[key_index] + 26) % 26 + ord('A'))
            else : 
                modified_char = chr((ord(char.upper()) + key_as_int[key_index] - 26) % 26 + ord('A'))
            #Put back in lower case if it was
            if char.islower():
                modified_char = modified_char.lower()
            text += modified_char
        #Digits encryption/decryption
        elif char.isdigit():
            if decryption:
                modified_char = str((int(char) - key_as_int[key_index]) % 10)
            else:  
                modified_char = str((int(char) + key_as_int[key_index]) % 10)
            text += modified_char
        else:
            text += char
    return text
    
def send_packet(key, type, content):
    """
    Envoie de données fournie en paramètres
    Cette fonction permet de construire, de chiffrer puis d'envoyer un paquet via l'interface radio du micro:bit

    :param (str) key:       Clé de chiffrement
           (str) type:      Type du paquet à envoyer
           (str) content:   Données à envoyer
	:return none
    """
    packet = f"{type}|{len(content)}|{content}"
    encrypted_packet = vigenere(packet, key)
    radio.send(encrypted_packet)
#Decrypt and unpack the packet received and return the fields value
def unpack_data(encrypted_packet, key):
    """
    Déballe et déchiffre les paquets reçus via l'interface radio du micro:bit
    Cette fonction renvoit les différents champs du message passé en paramètre

    :param (str) encrypted_packet: Paquet reçu
           (str) key:              Clé de chiffrement
	:return (srt)type:             Type de paquet
            (int)lenght:           Longueur de la donnée en caractères
            (str) message:         Données reçues
    """
    try:
        type = str(type)
        length = int(length)
        decrypted_packet = vigenere(encrypted_packet,key,decryption=True)
        message = decrypted_packet.split('|')
        return message
        
    except:

#Unpack the packet, check the validity and return the type, length and content
def receive_packet(packet_received, key):
    """
    Traite les paquets reçue via l'interface radio du micro:bit
    Cette fonction permet de construire, de chiffrer puis d'envoyer un paquet via l'interface radio du micro:bit
    Si une erreur survient, les 3 champs sont retournés vides

    :param (str) packet_received: Paquet reçue
           (str) key:              Clé de chiffrement
	:return (srt)type:             Type de paquet
            (int)lenght:           Longueur de la donnée en caractère
            (str) message:         Données reçue
    """
    packet_received = unpack_data(radio.received(), key)  
    try:    
        if packet_received:
            for i in packet_received :
                real_packet =  f"{i}|{i+1}|{i+2}"
            return real_packet
    except:
        return " | | "
    
#Calculate the challenge response
def calculate_challenge_response(challenge):
    """
    Calcule la réponse au challenge initial de connection avec l'autre micro:bit

    :param (str) challenge:            Challenge reçu
	:return (srt)challenge_response:   Réponse au challenge
    """
    
#Ask for a new connection with a micro:bit of the same group
def establish_connexion(key):
    """
    Etablissement de la connexion avec l'autre micro:bit
    Si il y a une erreur, la valeur de retour est vide

    :param (str) key:                  Clé de chiffrement
	:return (srt)challenge_response:   Réponse au challenge
    """
def agitation():


    while True:
        x = accelerometer.get_x()
        y = accelerometer.get_y()
        z = accelerometer.get_z()

        mouvement = abs(x) + abs(y) + abs(z)

        if mouvement < AGITATION_FAIBLE:
            send_packet(key, 5, 'endormi')
        elif mouvement < AGITATION_MODEREE:
            send_packet(key, 5, 'agité')
        elif mouvement > AGITATION_FORTE:
            send_packet(key, 5, 'très agité')

    sleep(200)
def musique_et_bruits_menu():
    while True: 
        if button_a.is_pressed():
            if pin0.is_touched():
                rick_roll()
            if pin1.is_touched():
                classical()
        if button_b.is_pressed():
            bruits_de_fonds()


def musique_et_bruits_alerte():
    while True: 
        message = receive_packet(radio.receive(),key )
        if message[2] == "rick_roll" :
            rick_roll()
        if message[2] == "classical" :    
            classical()
        if message[2] == "bruits" :
            bruits_de_fonds()
def compteur_lait():
    message = receive_packet(radio.receive(), key)
    display.show(message[2])

def veilleusee():
    while True:
        if display.read_light_level() < 100:  
            send_packet(key, 4, "luminosité_faible")  
            
def veilleuse_activé():
    if receive_packet(radio.receive(), key) == "activé":
        display.show(Image("10101:01110:11111:01110:10101"))
    else:
        display.clear()
        

def veilleuse_activation():
    if button_a.was_pressed():
        display.show(Image("10101:01110:11111:01110:10101"))
    if pin_logo.is_touched():
        main()

def instructions():
    if radio.receive():
        message = receive_packet(radio.receive(), key)
        if message[0] == 4:
            veilleuse_activé()  
        if message[0] == 2:
            musique_et_bruits_alerte()

def temp():
    while True:
        room_temp = temperature() - 4
        display.show(room_temp)
        if room_temp >= 25:
            send_packet(key, 3, "Alerte: Température trop élevée !")
        elif room_temp <= 20:
            send_packet(key, 3, "Alerte: Température trop basse !")
        else:
            display.clear()
    
    sleep(600000)

def menu():
    lst = [compteur_de_lait, veilleuse, temperature, musique_bruits]
    value = []
    stop = False
    for image in lst:
        while not button_a.was_pressed():
            display.show(image)
            sleep(500)
            if button_b.was_pressed():
                value.clear()
                value.append(image)
                stop = True
                break
            elif button_a.is_pressed():
                stop = True
                break
        
    if value and value[0] == compteur_de_lait:
        lait()
    elif value and value[0] ==luminosite_auto: #PAS OPERATIONNEL
        veilleuse_activation()
    elif value and value[0] == temperature:
        temp()
    elif value and value[0] == musique_bruits:
        musique_et_bruits()

def main():
    while True:
        veilleusee()
        if radio.receive():
            instructions()
        if pin_logo.is_touched():
            menu()