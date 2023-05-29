# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 20:05:12 2023

@author: arthu
"""
import random as rnd

class plateau():
    
    def init_plat(self, diff: int, coord: tuple):
        print('diff',diff)
        self.dico = {} #dictionnaire du plateau de jeu
        self.listeb = [] #liste de bombes
        self.diff = diff #tuple de dimensions du plateau (difficulté (x,y))
        self.coord = coord #coordonnées de l'endroit cliqué
        self.difficultes = {0: ((9,9), 10), 1: ((16,16), 40), 2:((16, 30), 99)} 
        self.gen_dico() #génère le plateau de jeu
        self.gen_mines()
        self.aff_nb() #afiche le nombre de bombes situées autour d'une case
        self.liste_cases = [key for key in self.dico.keys() if self.dico[key][2]!=-1] #liste des cases à decouvrir
    
    def gen_dico(self):
        """
        Génère le plateau de jeu (fonction imposée)

        Returns
        -------
        None.

        """
        for i in range(self.difficultes[self.diff][0][0]):
            for y in range(self.difficultes[self.diff][0][1]):
                #itère sur toutes les cases du plateau
                self.dico[(i, y)] = [0,0,0,0]
    
    
    def gen_mines(self):
        """
        Génère les bombes (après le premier coup) de manière aléatoire

        Returns
        -------
        None.

        """
        xmax = max([key[0] for key in self.dico.keys()])+1 #dimension horizontale du plateau
        ymax = max([key[1] for key in self.dico.keys()])+1 #dimension verticale du plateau
        nbcases = (xmax)*(ymax) 
        liste = [i for i in range(nbcases)] #on associe à chaque case un numéro
        
        
        
        #Sécurisation 1er coup avec pas bombe dans 8 cases autour
        #On se positionne dans un repère centré sur la première case cliquée
        coinX = self.coord[0]-1 #ordonnée de la case supérieure gauche
        coinY = self.coord[1]-1 #abscisse de la case supérieure gauche

        for i in range(9):
            if (((i//3)+coinX, (i%3)+coinY) in self.dico): #(i//3) renvoie l'ordonnée correspondant à la case et (i%3) son abscisse
                liste.remove(((i//3)+coinX)*ymax + (i%3)+coinY)
        rnd.shuffle(liste)
        for _ in range(self.difficultes[self.diff][1]):
            nb = liste.pop() 
            self.dico[(nb//(ymax), nb%ymax)][2] = -1  #ligne, colonne ?
            self.listeb.append((nb//(ymax), nb%ymax)) #ajoute à listeeb les coordonnées des bombes
        
    
    def aff_nb(self):
        for bombe in self.listeb:
            #On se positionne dans un repère centré sur la première case cliquée
            coinX = self.coord[0]-1 #ordonnée de la case supérieure gauche
            coinY = self.coord[1]-1 #abscisse de la case supérieure gauche
            for i in range(9):
                if (((i//3)+coinX, (i%3)+coinY) in self.dico) and not(i==4):
                    self.dico[((i//3)+coinX, (i%3)+coinY)][3]+=1 #ajoute 1 au "nombre de bombes" de toutes les cases situés dans le repère 
    
    def log_affichage(self):
        """
        Affiche le plateau sur la console du serveur

        Returns
        -------
        None.

        """
        xmax = max([key[0] for key in self.dico.keys()])+1 #dimension horizontale du plateau
        ymax = max([key[1] for key in self.dico.keys()])+1 #dimension verticale du plateau
        for i in range(xmax):
            for y in range(ymax):
                #itère sur toutes les cases
                if self.dico[(i,y)][2]!=-1: #case!=bombe
                    print(f' {self.dico[(i,y)][3]} |', end='')
                else :
                    print(' X |', end='')
            print('')

    def affichage(self):
        """
        Affiche le plateau sur la console des clients (avec les cases non découvertes non visibles)

        Returns
        -------
        None.

        """
        xmax = max([key[0] for key in self.dico.keys()])+1 #dimension horizontale du plateau
        ymax = max([key[1] for key in self.dico.keys()])+1 #dimension verticale du plateau
        for i in range(xmax):
            for y in range(ymax):
                #itère sur toutes les cases
                if self.dico[(i,y)][0]==-2: #drapeau déposé
                    print(' 🏴󠁧󠁢󠁷󠁬󠁳󠁿 |', end='')
                else :
                    if self.dico[(i,y)][1]==0: #non découvert
                        print(' * |', end='')
                    elif self.dico[(i,y)][3] == 0: #pas de bombe autour
                        print('   |', end='')
                    else :
                        print(f' {self.dico[(i,y)][3]} |', end='')

            print('')
            
    def coup(self, coord: tuple):
        """
        

        Parameters
        ----------
        coord : tuple
            Permet de rendre compte des modifications apportées par le coup d'un joueur'

        Returns
        -------
        case_updated : list
            liste des cases ayant subies des modifications
        TYPE
            DESCRIPTION.

        """
        case_updated = [] #liste des coordonnées des cases ayant subies des modifications
        if (coord in self.dico) and (self.dico[coord][0] != -2) and (self.dico[coord][1] == 0):
            if self.dico[coord][2] == 0:
                self.dico[coord][1] = -1 #case cliquée à présent découverte
                case_updated.append(f'({coord[0]}.{coord[1]}.{self.dico[coord][3]})') #la case découverte est à présent à modifier (afficher nb bombes)
                self.liste_cases.remove((coord[0], coord[1])) #case plus à découvrir car déjà découverte               
                if self.dico[coord][3] == 0:
                    buffer = [coord]
                    while len(buffer)>0:
                        coinX = buffer[0][0]-1 #ordonnée de la case supérieure gauche
                        coinY = buffer[0][1]-1 #abscisse de la case supérieure gauche
                        for i in range(9):
                            if (((i//3)+coinX, (i%3)+coinY) in self.dico) and not(i==4):
                                if self.dico[((i//3)+coinX, (i%3)+coinY)][1] == 0: #Case affiché ?
                                    if self.dico[((i//3)+coinX, (i%3)+coinY)][0] != -2: #Drapeau sur la case ?
                                        self.dico[((i//3)+coinX, (i%3)+coinY)][1] = -1 #case à présent découverte
                                        case_updated.append(f'({(i//3)+coinX}.{(i%3)+coinY}.{self.dico[((i//3)+coinX, (i%3)+coinY)][3]})') 
                                        self.liste_cases.remove(((i//3)+coinX, (i%3)+coinY)) #case plus à découvrir car déjà découverte
                                        if self.dico[((i//3)+coinX, (i%3)+coinY)][3] == 0:
                                            buffer.append(((i//3)+coinX, (i%3)+coinY))
                        buffer.remove(buffer[0]) #Récursivité de buffer
                                    
            else: return (case_updated, 'Lost') 
        else: return False
        if len(self.liste_cases) == 0: #Toutes les cases découvertes
            return (case_updated, 'Equality')
        return (case_updated,0)
                    
    def flag(self, coord:tuple):
        """
        

        Parameters
        ----------
        coord : tuple
            Place un drapeau au bouton de coordonnées coord.

        Returns
        -------
        None.

        """
        if (coord in self.dico):
            self.dico[coord][0] = -2
            
    def unflag(self, coord:tuple):
        """
        

        Parameters
        ----------
        coord : tuple
            Retire un drapeau au bouton de coordonnées coord.

        Returns
        -------
        None.

        """
        if (coord in self.dico):
            self.dico[coord][0] = 0
        
