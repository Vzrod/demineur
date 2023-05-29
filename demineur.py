# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 20:05:12 2023

@author: arthu
"""
import random as rnd

class plateau():
    
    def init_plat(self, diff: int, coord: tuple):
        print('diff',diff)
        self.dico = {}
        self.listeb = []
        self.diff = diff
        self.coord = coord
        self.difficultes = {0: ((9,9), 10), 1: ((16,16), 40), 2:((16, 30), 99)}
        self.gen_dico()
        self.gen_mines()
        self.aff_nb()
        self.liste_cases = [key for key in self.dico.keys() if self.dico[key][2]!=-1] #à decouvrir
    
    def gen_dico(self):
        for i in range(self.difficultes[self.diff][0][0]):
            for y in range(self.difficultes[self.diff][0][1]):
                self.dico[(i, y)] = [0,0,0,0]
    
    
    def gen_mines(self):
        xmax = max([key[0] for key in self.dico.keys()])+1
        ymax = max([key[1] for key in self.dico.keys()])+1
        nbcases = (xmax)*(ymax)
        liste = [i for i in range(nbcases)]
        
        
        
        #Sécurisation 1er coup avec pas bombe dans 8 cases autour
        coinX = self.coord[0]-1
        coinY = self.coord[1]-1

        for i in range(9):
            if (((i//3)+coinX, (i%3)+coinY) in self.dico):
                liste.remove(((i//3)+coinX)*ymax + (i%3)+coinY)
        rnd.shuffle(liste)
        for _ in range(self.difficultes[self.diff][1]):
            nb = liste.pop()
            self.dico[(nb//(ymax), nb%ymax)][2] = -1  #ligne, colonne ?
            self.listeb.append((nb//(ymax), nb%ymax))
        
    
    def aff_nb(self):
        for bombe in self.listeb:
            coinX = bombe[0]-1
            coinY = bombe[1]-1
            for i in range(9):
                if (((i//3)+coinX, (i%3)+coinY) in self.dico) and not(i==4):
                    self.dico[((i//3)+coinX, (i%3)+coinY)][3]+=1
    
    def log_affichage(self):
        xmax = max([key[0] for key in self.dico.keys()])+1
        ymax = max([key[1] for key in self.dico.keys()])+1
        for i in range(xmax):
            for y in range(ymax):
                if self.dico[(i,y)][2]!=-1:
                    print(f' {self.dico[(i,y)][3]} |', end='')
                else :
                    print(' X |', end='')
            print('')

    def affichage(self):
        xmax = max([key[0] for key in self.dico.keys()])+1
        ymax = max([key[1] for key in self.dico.keys()])+1
        for i in range(xmax):
            for y in range(ymax):
                if self.dico[(i,y)][0]==-2:
                    print(' F |', end='')
                else :
                    if self.dico[(i,y)][1]==0:
                        print(' * |', end='')
                    elif self.dico[(i,y)][3] == 0:
                        print('   |', end='')
                    else :
                        print(f' {self.dico[(i,y)][3]} |', end='')

            print('')
            
    def coup(self, coord: tuple):
        case_updated = []
        if (coord in self.dico) and (self.dico[coord][0] != -2) and (self.dico[coord][1] == 0):
            if self.dico[coord][2] == 0:
                self.dico[coord][1] = -1
                case_updated.append(f'({coord[0]}.{coord[1]}.{self.dico[coord][3]})')
                self.liste_cases.remove((coord[0], coord[1]))                
                if self.dico[coord][3] == 0:
                    buffer = [coord]
                    while len(buffer)>0:
                        coinX = buffer[0][0]-1
                        coinY = buffer[0][1]-1
                        for i in range(9):
                            if (((i//3)+coinX, (i%3)+coinY) in self.dico) and not(i==4):
                                if self.dico[((i//3)+coinX, (i%3)+coinY)][1] == 0: #Case affiché ?
                                    if self.dico[((i//3)+coinX, (i%3)+coinY)][0] != -2: #Drapeau sur la case ?
                                        self.dico[((i//3)+coinX, (i%3)+coinY)][1] = -1
                                        case_updated.append(f'({(i//3)+coinX}.{(i%3)+coinY}.{self.dico[((i//3)+coinX, (i%3)+coinY)][3]})')
                                        self.liste_cases.remove(((i//3)+coinX, (i%3)+coinY))
                                        if self.dico[((i//3)+coinX, (i%3)+coinY)][3] == 0:
                                            buffer.append(((i//3)+coinX, (i%3)+coinY))
                        buffer.remove(buffer[0])
                                    
            else: return (case_updated, 'Lost') 
        else: return False
        if len(self.liste_cases) == 0:
            return (case_updated, 'Equality')
        return (case_updated,0)
                    
    def flag(self, coord:tuple):
        if (coord in self.dico):
            self.dico[coord][0] = -2
            
    def unflag(self, coord:tuple):
        if (coord in self.dico):
            self.dico[coord][0] = 0
        
