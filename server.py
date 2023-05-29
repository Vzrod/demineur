# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:41:37 2023

@author: aclot

(b'<GAME_TURN>,350,(1.2.4),(2.3.6)').decode('utf-8').split(',')

"""

import random as rnd
import socket
from demineur import plateau
from threading import Thread
import time
import queue

class threadedServer(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ''
        port = 2500
        domain = 'demineur.ddns.net'
        self.serversocket.bind((host, port))
        ip_address = socket.gethostbyname(domain)
        print(ip_address)
        print(socket.gethostname())
        self.serversocket.listen(5)
        self.lobby()
            
    def lobby(self):
        self.game_state = True
        self.cons_socket = []
        self.players = {}
        while len(self.cons_socket) != 2:
            print('Att co')
            self.serversocket.settimeout(None)
            clientsocket, addr = self.serversocket.accept()
            data = clientsocket.recv(1024).decode('utf-8')
            print('receive', data)
            if data[:8] == '<PSEUDO>':
                self.players[addr] = data[8:]
                self.players[clientsocket] = data[8:]
                self.cons_socket.append(clientsocket)
                if len(self.cons_socket) == 2:
                    for client in self.cons_socket:
                        try : client.send(b'bonsoir')
                        except socket.error: self.cons_socket.remove(client)
                print(len(self.cons_socket))
        print('Debut game')
        self.start_game()

        


    def start_game(self):
        self.game = plateau()
        self.game.init_plat(0)
        self.timeplayer = 10.1
        self.game.log_affichage()
        self.data_queue = queue.Queue()
        print()
        for client in self.cons_socket:
            try : 
                client.send(b'<GAME_INIT>')
                print('Send GAME INIT')
            except socket.error: 
                client.send(b'<SERVER_ERROR>')
                self.lobby()
                break
        time.sleep(1) #Prévenir le temps de chargement des clients / A changer :==> Attendre rep pour launch mais flemme
        while self.game_state:
            for client in self.cons_socket:
                cur_player = self.players[client]
                self.reponse = False
                client.send(b'<GAME_TURN>')
                
                l1_thread = Thread(target=self.listening, args=(client,))
                l1_thread.start()                
                
                l2_thread = Thread(target=self.is_data, args=(client,))
                l2_thread.start()
                l2_thread.join(timeout=int(self.timeplayer)+1)
                
                if self.data == 'Lost':
                    print('PLayer Timeout')
                    for client in self.cons_socket:
                        client.send(b'<CLIENT_LOST>'+cur_player.encode('utf-8'))
                    self.game_state = False
                    break
                
                else:
                    d = (self.data).decode('utf-8')
                    plate_update = self.game.coup(eval(d))
                    
                    self.game.affichage()
                    print()
                    com = b'<CLIENT_UPDATE>'
                    for up in plate_update[0]:
                        com+=b','+up.encode('utf-8')
                    for client in self.cons_socket:
                        client.send(com)
                        
                        
                        
                        
                        
                    if plate_update[1] == 'Equality':
                        for client in self.cons_socket:
                            client.send(b'<CLIENT_EQUALITY>')
                            print('client equality')
                        self.game_state = False
                        break
                    
                    if plate_update[1] == 'Lost':
                        for client in self.cons_socket:
                            client.send(b'<CLIENT_LOST>'+cur_player.encode('utf-8'))
                        self.game_state = False
                        break
                        
        print("New server Game started")
        self.lobby()
            


    def listening(self, client):
        try:
            self.serversocket.settimeout(float(self.timeplayer)+0.1)
            data = client.recv(1024)
            if self.game_state == True:
                self.data_queue.put_nowait((data))
        except : pass  #Timeout
        
    
    def is_data(self, client):
        print("Attente data")
        timer = self.timeplayer
        for _ in range(int(self.timeplayer/0.1)):
            if not self.data_queue.empty():
                self.data = self.data_queue.get()
                print("Received :", self.data)
            
                break
            com = b'<TIMER>'
            timer -= 0.1
            timer = round(timer,1)
            msg = com + str(timer).encode('utf-8')
            
            client.send(msg)
            time.sleep(0.1)
        else : 
            print("END CHRONO")
            self.data = 'Lost'
                
                
        
s = threadedServer()                    
                    
                
        
        
    