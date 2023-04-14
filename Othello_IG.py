import numpy as np
from tkinter import *
from Othello_project import *

class Interface :
    def __init__(self,fenetre):
        self.fenetre = fenetre
        self.fenetre.title('Othello')
        self.fenetre.geometry("400x200")
        self.label = Label(self.fenetre,text="Avec quel mode de jeu veux tu jouer ? :")
        self.label.place(x=10,y=10)
        self.button1 = Button(self.fenetre,text="Joueur contre Joueur",command=lambda : self.Joueur(2))
        self.button2 = Button(self.fenetre,text="Joueur contre Ordinateur",command=lambda : self.Ordi())
        self.button3 = Button (self.fenetre,text="Ordinateur contre Ordinateur",command=lambda : self.Joueur(0))
        self.button1.place(x=10,y=40)
        self.button2.place(x=10,y=70)
        self.button3.place(x=10,y=100)
        mainloop()
    def Ordi(self):
        self.button1.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.buttonBotCommence = Button(self.fenetre,text="Joueur commence",command=lambda : self.Joueur(1, 1))
        self.buttonPlayerCommence = Button(self.fenetre,text="IA commence",command=lambda : self.Joueur(1, -1))
        self.buttonBotCommence.place(x=10,y=70)
        self.buttonPlayerCommence.place(x=10,y=40)
        mainloop()
    def Joueur(self,nbjoueur, joueurdep=1):
        if(nbjoueur==1):
            self.buttonBotCommence.destroy()
            self.buttonPlayerCommence.destroy()
        else:
            self.button1.destroy()
            self.button2.destroy()
            self.button3.destroy()
        self.jeu = Othello(nbjoueur, joueurdep)
        self.creer_cases()
        self.label.place(x = 70*8+10,y = 2)
        self.fenetre.geometry("800x600")
        self.Affichage()
    def creer_cases(self):
        nbc = len(self.jeu.plateau)  # Nombre de lignes
        nbl = len(self.jeu.plateau[0])  # Nombre de colonnes
        self.buttons = [ [None for x in range(nbc)] for y in range(nbl) ]
        # On crée les Labels un par un et on les stocke dans la matrice
        for x in range(nbc):
            for y in range(nbl):
                # Création et stockage d'un Label
                self.buttons[x][y] = Button(self.fenetre)
                # Affichage et placement du widget contenu dans w[y][x]
                px = y*70  # position px en pixels      
                py = x*70 # position py en pixels             
                self.buttons[x][y].place(y=py, x=px)

    def acutaliser_case(self,manger):
        rond_noir = PhotoImage(file=r"Images/rond_noir.png")
        rond_blanc = PhotoImage(file=r"Images/rond_blanc.png")
        possible_pion = PhotoImage(file=r"Images/rond_circle.png")
        vide = PhotoImage(file=r"./Images/empty.png")   
        peut_jouer  = False
        for i in range(len(self.jeu.plateau)):
            for j in range(len(self.jeu.plateau[i])):
                if self.jeu.plateau[i][j]==1:
                    self.buttons[i][j].configure(image=rond_blanc,command=self.Pion_Pres)
                elif self.jeu.plateau[i][j]==-1:
                    self.buttons[i][j].configure(image=rond_noir,command=self.Pion_Pres)
                elif len(manger[i][j])>0:
                    self.buttons[i][j].configure(image=possible_pion,command=lambda x = i,y=j :self.Nouv_Pion(x,y))
                    peut_jouer = True
                else :
                    self.buttons[i][j].configure(image=vide,command=self.Pas_Mange)
        if np.sum(self.jeu.plateau != 0)==64:
            if(self.jeu.pion[1]>self.jeu.pion[-1]):
                self.label.configure(text="Le joueur 1 a gagné :\nJoueur 1 "+str(self.jeu.pion[1])+" pions\nJoueur 2 "+str(self.jeu.pion[-1])+" pions")
            elif(self.jeu.pion[1]<self.jeu.pion[-1]):
                self.label.configure(text="Le joueur 2 a gagné :\nJoueur 2 : "+str(self.jeu.pion[-1])+" pions\nJoueur 1 "+str(self.jeu.pion[1])+" pions")    
            else :
                self.label.configure(text="Egalité avec "+str(self.jeu.pion[1])+" pour les 2 joueurs")
            #self.fenetre.destroy()
            restart = Button(self.fenetre,text="Recommencer",command=lambda : Restart())
            restart.place(x=600,y=130)
        elif not peut_jouer : 
            self.label.configure(text= "le joueur ne peux jouer")
            self.jeu.tour+=1
            self.jeu.joueur=-self.jeu.joueur
            self.Affichage()
        mainloop()
    def EnterJoueur(self,i,j):
        manger = self.jeu.Pose()
        self.jeu.pion[self.jeu.joueur]+=1
        self.jeu.plateau[i][j]=self.jeu.joueur
        for pion_mange in manger[i][j]:
            self.jeu.plateau[pion_mange[0]][pion_mange[1]] = self.jeu.joueur
            self.jeu.pion[self.jeu.joueur]+=1
            self.jeu.pion[-self.jeu.joueur]-=1
        self.jeu.tour+=1
        self.jeu.joueur=-self.jeu.joueur
        self.Affichage()
    def Nouv_Pion(self,i,j):        
        self.EnterJoueur(i,j)
    def Pion_Pres(self):
        self.label.configure(text="Un joueur est déjà présent")
    def Pas_Mange(self):
        self.label.configure(text="Tu ne peux jouer ici")
    def Affichage(self):
        manger = self.jeu.Pose()
        if self.jeu.joueur==1 :
            self.label.configure(text="C'est aux pions blancs de jouer")
        else :             
            self.label.configure(text="C'est aux noirs de jouer")
        self.acutaliser_case(manger)
        
def Restart():
    for child in fenetre.winfo_children(): child.destroy()
    interface = Interface(fenetre)


if __name__ == "__main__":
    fenetre = Tk()
    interface = Interface(fenetre)