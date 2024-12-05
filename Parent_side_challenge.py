from microbit import *
import radio
import random
import music

#Can be used to filter the communication, only the ones with the same parameters will receive messages
#radio.config(group=23, channel=2, address=0x11111111)
#default : channel=7 (0-83), address = 0x75626974, group = 0 (0-255)

pin0.set_touch_mode(pin0.CAPACITIVE)     #activation des 3 pin en tant que touche
pin1.set_touch_mode(pin1.CAPACITIVE)
pin2.set_touch_mode(pin2.CAPACITIVE)

def generate_key(seed):                  
    return hashing(seed)                   #grace au hashing on génére une key différente a partir d'une seed identique aux 2 microbit 

"""
Type des messages

0 = challenge
1 = lait
2 = bruits 
3 = température
4 = veilleuse
5 = état d'éveil

"""






#Initialisation des variables du micro:bit
radio.on()
radio.config(group=3)
connexion_established = False
key = generate_key(13)
connexion_key = None
nonce_list = set()
baby_state = 0
set_volume(100)

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
        #Letters encryption/decryption
        if char.isalpha():
            key_index = i % key_length
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
            key_index = i % key_length
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
    Envoi de données fournies en paramètres
    Cette fonction permet de construire, de chiffrer puis d'envoyer un paquet via l'interface radio du micro:bit

    :param (str) key:       Clé de chiffrement
           (str) type:      Type du paquet à envoyer
           (str) content:   Données à envoyer
	:return none
    """
    packet = f"{type}|{len(content)}|{content}"             #le packet est initialisé sous format T|L|V
    encrypted_packet = vigenere(packet, key)               #on chiffre le packet 
    radio.send(str(encrypted_packet))                     #le packet chiffré est envoyé 
#Unpack the packet, check the validity and return the type, length and content
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
    decrypted_packet = vigenere(encrypted_packet, key)                   #decrypter le message recu
    decrypted_packet.split("|")                                  #on sépare et remet au format T|L|V
    for type, length, message in decrypted_packet:            #on crée une boucle pour pouvoir ensuite renvoyer les éléments du decrypted_packet
        return f"type: {type}"
        return f"length: {int(length)}"
        return f"message: {message}"
    
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
    Calcule la réponse au challenge initial de connection envoyé par l'autre micro:bit

    :param (str) challenge:            Challenge reçu
	:return (srt)challenge_response:   Réponse au challenge
    """
    challenge = vigenere("tentative de connexion", key)         #décryptage du challenge recu 
    if challenge == "connexion":
         challenge_response = "réussie"
    send_packet(key, 0, challenge_response)                   #reponse au challenge crypté 

#Respond to a connexion request by sending the hash value of the number received
def respond_to_connexion_request(key):
    """
    Réponse au challenge initial de connection avec l'autre micro:bit
    Si il y a une erreur, la valeur de retour est vide

    :param (str) key:                   Clé de chiffrement
	:return (srt) challenge_response:   Réponse au challenge
    """

    send_packet(key, 0, key )   #la clé de base est deja hachée donc on va juste l'envoyer ???
    

def musique_et_bruits():
    if button_a.was_pressed():
        display.show(musiquemode)
        sleep(100)
        send_packet(key, 2, "musique")         
    elif button_b.was_pressed():
        display.show(Image.HEART_SMALL)
        sleep(100)
        send_packet(key, 2, "bruits")
    elif pin_logo.is_touched():
        display.show("X")
        sleep(200)
        menu()
        

def menu():
    lst = [compteur_de_lait, veilleuse, temperature, musique_bruits]
    value = []
    stop = False
    ALERT_RECEIVED()
    for image in lst:
            display.show(image)
            sleep(2000)
            if button_a.was_pressed():
                value.clear()
                value.append(image)
                stop = True
                break
            elif button_b.is_pressed():
                stop = True
                break
        
    if value and value[0] == compteur_de_lait:
        compteur_de_lait_menu()
    elif value and value[0] ==veilleuse: #PAS OPERATIONNEL
        veilleuse_menu()
    elif value and value[0] == temperature:
        temp()
    elif value and value[0] == musique_bruits:
        musique_et_bruits()

doses = 0
def compteur_de_lait_menu():
    send_packet(key, 1, doses)
    while True:
        if pin0.is_touched():
            doses = 0  
            display.show(str(doses)) 
            sleep(500) 
        if pin1.is_touched():
            doses += 1 
            display.show(str(doses))
            sleep(500)
        if pin2.is_touched():
            doses += 2
            display.show(str(doses))
            sleep(500)
        if button_a.was_pressed():
            if doses > 0:
                doses -= 1
            display.show(str(doses))
            sleep(500)
        if pin_logo.is_touched():
            menu()
        
def temp():
    temperature = receive_packet(radio.receive(), key)[2]
    if temperature == "Alerte: Température trop élevée !":
        display.show(flamme, delay=100)
        music.play(music.POWER_DOWN)
    elif temperature == "Alerte: Température trop basse !":
        display.show(flocons, delay=100)
        music.play(music.POWER_UP)    
def ALERT_RECEIVED():
    if radio.receive():
        message = receive_packet(radio.receive(), key)
        if message[0] == 3:
            temp()
        if message[0] == 4:
            veilleusee()
        if message[0] == 5:
            if message[2] == 'endormi':
                display.show(Image.ASLEEP)  
            elif message[2] == 'agité':
                display.show(Image.MEH)  
            elif message[2] == 'très agité':
                music.play(music.POWER_DOWN)
                display.show(Image.NO)
                if button_a.was_pressed():
                    musique_et_bruits()
        sleep(200)  
                
 
def veilleusee():
    message = receive_packet(radio.receive(), key)
    if message[2] == "luminosité_faible":
        display.scroll("low")
        if button_a.is_pressed():
            send_packet(key, 4,"activé" )
        if pin_logo.is_touched():
            menu()
        
def veilleuse_menu():
    if button_a.is_pressed():
        send_packet(key, 4,"activé")
    if pin_logo.is_touched():
        menu()


    

def main():
    while True:
        if pin_logo.is_touched():
            menu()

