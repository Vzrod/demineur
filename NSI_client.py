# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:07:31 2023

@author: arthu

pyinstaller client.py --onefile --windowed --collect-submodules solar-system


!!!!!!!!!!!!!!!! close file when window close


!!! reload server apres fin + close socket car socket.close marche pas a cause de thread listening

"""

import socket
from threading import Thread

import tkinter as tk
import tkinter.messagebox
import time
from NSI_GUI import *
            
class threadedClient(Thread):
    def __init__(self):
        Thread.__init__(self)
        
        tgui = Thread(target = self.affichage_fen) #Démarre la connection de la fonction conn sur un thread afin de ne pas freeze le gui
        tgui.start()
        
        
        self.game_init = [False, b'GAME_INIT', self.start_game]
        self.turn_cond = [False, b'GAME_TURN', self.is_turn]
        self.listen_update = [False, b'CLIENT_UPDATE', self.gui_update]
        self.client_lost = [False, b'CLIENT_LOST', self.lose_game]
        self.timerup = [False, b'TIMER', self.update_timer]
        self.equality = [False, b'CLIENT_EQUALITY', self.client_equality]
        self.dic = {self.game_init[1]:self.game_init, self.turn_cond[1]:self.turn_cond, self.listen_update[1]:self.listen_update, self.client_lost[1]:self.client_lost, self.timerup[1]:self.timerup, self.equality[1]:self.equality}
        
        
    def init_conn(self, host, port, pseudo):
        self.client_lost[0] = False
        
        self.pseudo = pseudo
        self.host = host
        self.port = port
        
        
        print("Init client")
        # Thread affichage GUI
        #tfen = Thread(target = self.affichage_fen, args=(2,))
        #tfen.start()
        #self.conn()
        
        tconn = Thread(target = self.conn) #Démarre la connection de la fonction conn sur un thread afin de ne pas freeze le gui
        tconn.start()
        
    def close_conn(self):
        print("Closing client socket")
        self.clientsocket.close()
        print(self.clientsocket)
        
        
    def conn(self):
        """Démarre la connction avec le serveur et transmet le pseudo"""
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.settimeout(5) #Timeout de 5s
        print("Socket crée")
        try:
            print("Démarrage connection socket")
            self.clientsocket.connect((self.host, self.port))
            self.start_listen()
            self.clientsocket.send(('<PSEUDO>'+self.pseudo).encode('utf-8'))
            self.fen.att_joueur()
        except socket.error as msg:
            print(f'Socket error : {msg}')
        except ConnectionRefusedError:
            print("Server fermé")
            self.clientsocket.close()
        
        
    def client_update(self, coord):
        """Fonct appelée par le gui lorsqu'une case est cliquée, envoie au serveur la case cliqué si c'est le tour du client"""
        print("client", coord)
        print(self.game_init[0], self.dic[b'GAME_TURN'][0])
        if self.game_init[0] == True and self.dic[b'GAME_TURN'][0] == True:
            self.clientsocket.send(str((coord)).encode('utf-8'))
            self.dic[b'GAME_TURN'][0] = False # Termine le tour du client
    
    
    
    def listen(self):
        """Fonct lancée en thread pour écouter msg du serv et call fonct correspondante"""
        #print('Client sur écoute')
        
        
        try:
            self.clientsocket.settimeout(None)
            data = self.clientsocket.recv(2048)
            #print(data)
            header = data[data.find(b'<')+1 : data.find(b'>')]
            if header in self.dic:
                #print('data', data, ' == cond[1]', self.dic[header][1])
                self.dic[header][2](data)
                self.dic[header][0] = True
            else : pass
        except socket.timeout: pass
        except : pass
        finally:
            self.start_listen()
           
            
           
            
    def is_turn(self, data):
        self.fen.is_turn = True
        
        
    def gui_update(self, data):
        """Communique au GUI les cases à modifier"""
        self.fen.is_turn = False
        undata = data.decode('utf-8').split(',')[1:]
        self.fen.gui_timer_up(10.0)
        for coord in undata:
            self.fen.update(eval(coord.replace('.',',')))
    
    def start_listen(self):
        """Fonct démarre le thread d'écoute"""
        if self.client_lost[0] != True:
            #print("start thread listen")
            t = Thread(target = self.listen)
            t.start()
        
    def start_game(self, data):
        """Fonct appelée par serveur depuis listen lors du démarrage de la game/ synchro clients"""
        print('Game started')
        self.fen.start((9,9))
    
    def lose_game(self, data):
        print('game lost')
        pseudo = data[data.find(b'>')+1:]
        print(pseudo)
        self.clientsocket.close()
        del self.clientsocket
        self.fen.losemsg(pseudo.decode('utf-8'))
        
        
    def client_equality(self, data):
        print('game equality')
        self.clientsocket.close()
        del self.clientsocket
        self.fen.equalitymsg()
        

    def update_timer(self, data):
        undata = data.decode('utf-8')[7:]
        self.fen.gui_timer_up(undata)

        
    def affichage_fen(self):
        self.fen = GUI(self)
        self.fen.mainloop()
        
a = threadedClient()