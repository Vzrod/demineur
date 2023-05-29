# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:41:37 2023

@author: aclot

(b'<GAME_TURN>,350,(1.2.4),(2.3.6)').decode('utf-8').split(',')

"""

#Imporation bibliothèques necessaires
import random as rnd
import socket
from demineur import plateau
from threading import Thread
import time
import queue

class threadedServer(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Création socket du serveur
        host = ''
        port = 2500
        domain = 'demineur.ddns.net'
        self.serversocket.bind((host, port)) #Assignation port et ip de connexion pour accéder au serveur
        ip_address = socket.gethostbyname(domain) #Assigne nom de domaine pour se connecter
        print(ip_address)
        print(socket.gethostname())
        self.serversocket.listen(5) #Nombre de "connections" simultanées (data.recv)
        self.lobby()
            
    def lobby(self):
        self.game_state = True
        self.cons_socket = [] #Stocke socket respectif des connexions des clients
        self.players = {} #Association socket client et son pseudo
        while len(self.cons_socket) != 2: #Tant qu'il n'y a pas 2 joueurs (gère les problèmes en cas de déconnexion)
            print('Att co')
            self.serversocket.settimeout(None)
            clientsocket, addr = self.serversocket.accept() #Accepte connexion entrante et l'associe à clientsocket
            data = clientsocket.recv(1024).decode('utf-8') #Récupère le pseudo du joueur
            print('Player : ', data)
            if data[:8] == '<PSEUDO>': #Vérifie si le header de l'info récupée est bien un pseudo
                self.players[addr] = data[8:]
                self.players[clientsocket] = data[8:]
                self.cons_socket.append(clientsocket)
                if len(self.cons_socket) == 2: # Test de vérification si les deux joueurs sont encore connectés
                    for client in self.cons_socket:
                        try : client.send(b'bonsoir')
                        except socket.error: self.cons_socket.remove(client)
        print('Debut game')
        self.start_game()

        


    def start_game(self):
        
        self.timeplayer = 10.1 #Temps pour chaque tour
        self.data_queue = queue.Queue() #Queue utilisé pour recevoir les données
        self.first_coup = True
        for client in self.cons_socket: #Annonce démarrage de la partie aux clients
            try : 
                client.send(b'<GAME_INIT>')
                print('Send GAME INIT')
            except socket.error: 
                client.send(b'<SERVER_ERROR>')
                self.lobby()
                break
        time.sleep(2) #Prévenir le temps de chargement des clients / A changer :==> Attendre rep pour launch mais flemme
        while self.game_state:
            for client in self.cons_socket: #Itération tour par tour sur chaque socket de client
                cur_player = self.players[client]
                self.reponse = False
                client.send(b'<GAME_TURN>') #Communique au client correspondant que c'est son tour
                
                #Lancement threads d'écoute
                l1_thread = Thread(target=self.listening, args=(client,))
                l1_thread.start()                
                
                l2_thread = Thread(target=self.is_data, args=(client,))
                l2_thread.start()
                l2_thread.join(timeout=int(self.timeplayer)+1) #Bloque l'exectuion du reste du code tant que thread non fini
                
                if self.data == 'Lost': #Vérifie si le joueur n'a pas dépassé le temps
                    print('PLayer Timeout')
                    for client in self.cons_socket:
                        client.send(b'<CLIENT_LOST>'+cur_player.encode('utf-8'))
                    self.game_state = False
                    break
                else:
                    if self.first_coup == True: #Gen plat pour 1er coup sécurisé
                        d = (self.data).decode('utf-8') #Décodage data recue
                        self.game = plateau() #Création plateau
                        self.game.init_plat(0, (eval(d))) #Initialise avec coord 1er coup ==> Empeche gen mines sur coord et cases voisines
                        plate_update = self.game.coup(eval(d)) #Update le plateau avec le 1er coup
                        self.game.log_affichage() #Affiche le debug mode du plateau
                        self.first_coup = False
                    else: #Déroulement normal
                        d = (self.data).decode('utf-8')
                        plate_update = self.game.coup(eval(d)) #Update plateau et récupère liste des cases à changer
                        
                    com = b'<CLIENT_UPDATE>'
                    for up in plate_update[0]: #Encodage cases à update sur les clients
                        com+=b','+up.encode('utf-8')
                    for client in self.cons_socket:
                        client.send(com)
                        
                    if plate_update[1] == 'Equality': #Communique aux clients si égalité
                        for client in self.cons_socket:
                            client.send(b'<CLIENT_EQUALITY>')
                            print('client equality')
                        self.game_state = False
                        break
                    
                    if plate_update[1] == 'Lost': #Communique aux clients si un joueur à perdu + pseudo du perdant
                        for client in self.cons_socket:
                            client.send(b'<CLIENT_LOST>'+cur_player.encode('utf-8'))
                        self.game_state = False
                        break
                        
        print("New server Game started")
        self.lobby() #Relance le lobby
            


    def listening(self, client): #Lancé en parallèle de is_data
        try:
            self.serversocket.settimeout(float(self.timeplayer)+0.1) #Applique timeout du tour du joueur à la fonction recv
            data = client.recv(1024)
            if self.game_state == True:
                self.data_queue.put_nowait((data)) #Ajoute coordonnées du coup recu à la queue
        except : pass  #Timeout
        
    
    def is_data(self, client): #Lancé en parallèle de listening
        print("Attente data")
        timer = self.timeplayer
        for _ in range(int(self.timeplayer/0.1)): #Test toutes les 0.1s si le joueur à envoyé les coordonnées de son coup
            if not self.data_queue.empty():
                self.data = self.data_queue.get()
                print("Received :", self.data)
            
                break
            com = b'<TIMER>'
            timer -= 0.1
            timer = round(timer,1)
            msg = com + str(timer).encode('utf-8')
            
            client.send(msg) #Envoi au client la durée restante du timer
            time.sleep(0.1)
        else : 
            print("END CHRONO")
            self.data = 'Lost' #Assigné si joueur en dépassement de temps ==> Perdu
                
                
        
s = threadedServer()                    
                    
                
        
        
    