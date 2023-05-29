# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 21:27:10 2023

@author: kamdoum alex, haas zoe, clot arthur
"""

import tkinter as tk
import time





class GUI(tk.Tk):
    
    def __init__(self, client):
        tk.Tk.__init__(self)
        self.client = client
        
        self.geometry("520x570")
        self.title("Partie de démineur")
        self.resizable(False, False)
        
        self.is_turn = False
        
        
        self.dico = {}
        
        self.bind("<Button-1>",self.mouse)
        self.bind("<Button-3>",self.flag)
        
        
        self.game_state = 0
        
        self.main_menu()
    
    
    
    def update(self, case):
        if case[2]!=-1:
            self.dico[case[0],case[1]].configure(text=case[2],fg=self.color(case[2]), bg='#f0f0f0')
        else:
            self.dico[case[0],case[1]].configure(text=case[2],fg=self.color(case),bg="red")
        
        
    def gui_timer_up(self, time):
        self.timer_label.configure(text=f'Timer : {time}')
        
        
    def timer(self):
        
        self.timer_label=tk.Label(self,text='Timer :',fg="black")
        self.timer_label.grid(row=self.taille[0]+1)
    
                
    def color(self, case):
        l=["white","#56ea62","green","sienna1","red","turquoise4","#ff7700","purple","VioletRed"]
        return l[case]

    
    def restart(self):
        for coords in list(self.dico.keys()):
            self.dico[coords].destroy()
        self.retry_button.destroy()
        self.lost_label.destroy()
        self.plage.destroy()
        game_state=0
        self.main_menu()
        
    def mouse(self, event):
        try:
            grid_info = event.widget.grid_info()
            if self.dico[grid_info["row"], grid_info["column"]]['text'] == '':
                self.client.client_update((grid_info["row"], grid_info["column"]))
        except :
            print("Endroit hors de la grille")
    
                
    def flag(self, event):
        global grid_sources
        grid_sources=event.widget.grid_info()
        if self.game_state==0:
            if self.dico[grid_sources["row"], grid_sources["column"]]['text'] == '':
                self.dico[grid_sources["row"], grid_sources["column"]].configure(text=chr(9872),fg="black",bg='#f0f0f0' )
            elif self.dico[grid_sources["row"], grid_sources["column"]]['text'] == chr(9872):
                self.dico[grid_sources["row"], grid_sources["column"]].configure(text="", bg='#f0f0f0')
    
    def dico_button(self):
        for i in range(self.taille[0]):
            for j in range(self.taille[1]):
                self.dico[(i, j)] = tk.Button(self.plage, height=1, width=3, font=("Helvetica", "20"),text=None)
                self.dico[i, j].bind("<Enter>", self.on_enter)
                self.dico[i, j].bind("<Leave>", self.on_leave)
                self.dico[i, j].grid(row=i,column=j)
                
    
    
    def main_menu(self):
        self.menu=tk.Frame(self)
        self.menu.grid()
        
        
        ip_label = tk.Label(self.menu, text="Server IP :")
        ip_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        
        self.ip_entry = tk.Entry(self.menu)
        self.ip_entry.insert(-1,'localhost')
        self.ip_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)
        
        port_label = tk.Label(self.menu, text="Port :")
        port_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        
        self.port_entry = tk.Entry(self.menu)
        self.port_entry.insert(-1,'2500')
        self.port_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)
        
        pseudo_label = tk.Label(self.menu, text="Pseudo :")
        pseudo_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        
        self.pseudo_entry = tk.Entry(self.menu)
        self.pseudo_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)
        
        
        self.join_server_btn = tk.Button(self.menu, text="Join Server", command=lambda: self.client.init_conn(self.ip_entry.get(), int(self.port_entry.get()), self.pseudo_entry.get()), height=2,width=10)
        self.join_server_btn.grid(column=1, row=3)
        
        
    def att_joueur(self):
        self.join_server_btn.destroy()
        
        self.quit_server_btn = tk.Button(self.menu, text="Quit Server", command=lambda: self.client.close_conn(), height=2,width=10)
        self.quit_server_btn.grid(column=1, row=3)
        
        self.att_j_label = tk.Label(self.menu, text="Connexion de l'adversaire en attente...")
        self.att_j_label.grid(column=1, row=4)
        
    def close_conn(self):
        self.quit_server_btn.destroy()
        self.att_j_label.destroy()
        
        
        self.join_server_btn = tk.Button(self.menu, text="Join Server", command=lambda: self.client.init_conn(self.ip_entry.get(), int(self.port_entry.get()), self.pseudo_entry.get()), height=2,width=10)
        self.join_server_btn.grid(column=1, row=3)
        
        
    #!!! CHANGER LA DEF ==> LE BTN DOIT APPELER UNE DEF EN THREAD SUR LE CLIENT
    def connect_server(self, ip, port, pseudo):
        if pseudo != "" and port != "" and ip != "":
            print(ip, port, pseudo)
    
    def start(self, taille):
        self.menu.destroy()
        
        self.plage=tk.Frame(self,height=200,width=300)
        self.plage.grid()
        
        self.taille = taille
        self.dico_button()
        
        self.timer()
        
    def on_enter(self, event):
        if self.is_turn == True:
            try:
                grid_info = event.widget.grid_info()
                if self.dico[grid_info["row"], grid_info["column"]]['text'] == '':
                    self.dico[grid_info["row"], grid_info["column"]].configure(bg='#d7ff12')
            except : pass
        
    def on_leave(self, event):
        
        try:
            grid_info = event.widget.grid_info()
            if self.dico[grid_info["row"], grid_info["column"]]['text'] == '':
                self.dico[grid_info["row"], grid_info["column"]].configure(bg='#f0f0f0')
        except : pass


    def start_turn(self):
        self.is_turn = True

    def losemsg(self, pseudo):
        """
        global game_state, retry_button, lost_label
        for case in list(plat.keys()):
            if plat[case][1]==0 and plat[case][2]==-1 and plat[case][0]==0:
                dico[case].configure(text="X", bg="#d33",fg="black")
            elif plat[case][1]==0 and plat[case][2]==-1 and plat[case][0]==-2:
                dico[case].configure(bg="#d33",fg="black")
        game_state=2
        """
        
        self.timer_label.destroy()
        
        self.lost_label=tk.Label(self,text=f'{pseudo} has lost the game, click on the button retry in order to restart the game.',fg="black")
        self.lost_label.grid(row=self.taille[0]+1)
        
        self.retry_button=tk.Button(self.plage,text="Retry",command=self.restart,height=2,width=5)
        self.retry_button.grid(row=self.taille[0]+5,column=int(self.taille[1]/2))

    def equalitymsg(self):
        
        self.timer_label.destroy()

        self.lost_label=tk.Label(self,text='Equality, click on the button retry in order to restart the game.',fg="black")
        self.lost_label.grid(row=self.taille[0]+1)
        
        self.retry_button=tk.Button(self.plage,text="Retry",command=self.restart,height=2,width=5)
        self.retry_button.grid(row=self.taille[0]+5,column=int(self.taille[1]/2))











