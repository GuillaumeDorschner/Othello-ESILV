import numpy as np
from tkinter import *
from Othello import *
import MinMax as MM
import time


class Interface:

  def Rejouer(self):
    """
    Fonction qui permet de rejouer une partie
    """
    self.fenetre.destroy()
    new_fenetre = Tk()
    new_interface = Interface(new_fenetre)

  def __init__(self, fenetre):
    """
    Initialisation de la fenêtre de jeu
    
    Args :
      fenetre (Tk) : Fenêtre de jeu
    """
    self.fenetre = fenetre
    self.tempsTotal = 0
    self.deepness = 4
    self.fenetre.title("Othello from 'The Board Master'")
    self.fenetre.geometry("400x200")
    self.last_x, self.last_y = None, None
    self.label = Label(self.fenetre,
                       text="Avec quel mode de jeu veux tu jouer ? :")
    self.label.place(x=10, y=10)
    self.button1 = Button(self.fenetre,
                          text="Joueur contre Joueur",
                          command=lambda: self.Joueur(2))
    self.button2 = Button(self.fenetre,
                          text="Joueur contre Ordinateur",
                          command=lambda: self.Ordi())
    self.button1.place(x=10, y=40)
    self.button2.place(x=10, y=70)
    mainloop()

  def Ordi(self):
    """
    Initialisation du jeu pour une partie 1 v IA et lance la partie
    """
    self.label.configure(text="Qui commence ?")
    self.button1.destroy()
    self.button2.destroy()
    self.buttonBotCommence = Button(self.fenetre,
                                    text="Joueur",
                                    command=lambda: self.Joueur(1, 1))
    self.buttonPlayerCommence = Button(self.fenetre,
                                       text="IA",
                                       command=lambda: self.Joueur(1, -1))
    self.buttonBotCommence.place(x=10, y=70)
    self.buttonPlayerCommence.place(x=10, y=40)
    mainloop()

  def Joueur(self, nbjoueur, joueurdep=1):
    """
    Initialisation du jeu et lance la partie
    
    Args : 
      nbjoueur (int) : Nombre de joueur
      joueurdep (int) : Joueur qui commence
    """
    if (nbjoueur == 1):
      self.buttonBotCommence.destroy()
      self.buttonPlayerCommence.destroy()
    else:
      self.button1.destroy()
      self.button2.destroy()
    self.jeu = Othello(nbjoueur, joueurdep)
    self.creer_cases()
    self.label.place(x=70 * 8 + 10, y=2)
    self.fenetre.geometry("800x600")
    self.Actualiser_plateau()

  def creer_cases(self):
    """
    Fonction qui crée les cases du plateau de jeu
    """
    nbc = len(self.jeu.plateau)  # Nombre de lignes
    nbl = len(self.jeu.plateau[0])  # Nombre de colonnes
    self.buttons = [[None for x in range(nbc)] for y in range(nbl)]
    # On crée les Labels un par un et on les stocke dans la matrice
    for x in range(nbc):
      for y in range(nbl):
        # Création et stockage d'un Label
        self.buttons[x][y] = Button(self.fenetre)
        # Affichage et placement du widget contenu dans w[y][x]
        px = y * 70  # position px en pixels
        py = x * 70  # position py en pixels
        self.buttons[x][y].place(y=py, x=px)

  def Actualiser_plateau(self,appeler = False):
    """
    Fonction qui actualise les cases du plateau de jeu
    """
    manger = self.jeu.Pose()
    if self.jeu.joueur == 1:
      couleur = "⚪️"
    else:
      couleur = "⚫️"
    self.label.configure(
      text=
      f"\nC'est aux pions {couleur} de jouer\n\ntour: {self.jeu.nbtour()} \n noir: {np.sum(self.jeu.plateau == -1)} \nblanc: {np.sum(self.jeu.plateau == 1)}"
    )
    restart = Button(self.fenetre,
                     text="Recommencer",
                     command=lambda: self.Rejouer())
    restart.place(x=600, y=130)
    rond_noir = PhotoImage(file=r"Images/rond_noir.png")
    rond_blanc_last = PhotoImage(file=r"Images/rond_blanc_last.png")
    rond_noir_last = PhotoImage(file=r"Images/rond_noir_last.png")
    rond_blanc = PhotoImage(file=r"Images/rond_blanc.png")
    possible_pion = PhotoImage(file=r"Images/rond_circle.png")
    vide = PhotoImage(file=r"./Images/empty.png")
    for i in range(len(self.jeu.plateau)):
      for j in range(len(self.jeu.plateau[i])):
        if self.jeu.plateau[i][j] == 1:
          if i == self.last_x and j == self.last_y:
            self.buttons[i][j].configure(image=rond_blanc_last,
                                         command=self.Pion_Pres)
          else:
            self.buttons[i][j].configure(image=rond_blanc,
                                         command=self.Pion_Pres)
        elif self.jeu.plateau[i][j] == -1:
          if i == self.last_x and j == self.last_y:
            self.buttons[i][j].configure(image=rond_noir_last,
                                         command=self.Pion_Pres)
          else:
            self.buttons[i][j].configure(image=rond_noir,
                                         command=self.Pion_Pres)

        elif len(manger[i][j]) > 0:
          self.buttons[i][j].configure(
            image=possible_pion,
            command=lambda x=i, y=j: self.EnterJoueur(x, y))
        else:
          self.buttons[i][j].configure(image=vide, command=self.Pas_Mange)
    self.Tour(manger,appeler)

  def Tour_IA(self):
    best_x, best_y = None, None
    temps = 0
    manger = self.jeu.Pose()
    coord = [[i, j] for i in range(8) for j in range(8)
             if len(manger[i][j]) != 0]
    if len(coord) > 0:
      # La deepness doit être paire
      best_x, best_y = MM.AlphaBetaSearch(self.jeu, manger, self.deepness)
      self.last_x, self.last_y = best_x, best_y
      temps = MM.AlphaBetaSearch.temps
      self.jeu.Change_Plateau(best_x, best_y, manger)
    self.jeu.joueur = -self.jeu.joueur  #changement de joueur

    self.tempsTotal += temps
    if not (best_y is None or best_x is None):
      self.labelCoup = Label(
        self.fenetre,
        text=f"Le coup de l'IA \nx: {best_x + 1} y: {best_y + 1}")
    self.labelCoup.place(x=600, y=200)
    self.labelTemps = Label(self.fenetre, text=f"Temps : {temps:.2f} s")
    self.labelTemps.place(x=600, y=250)
    self.labelTempsTotal = Label(self.fenetre,
                                 text=f"Temps Total : {self.tempsTotal:.2f} s")
    self.labelTempsTotal.place(x=600, y=300)

  def Fin(self):
    """
    Fonction qui affiche le gagnant de la partie
    """
    if (np.sum(self.jeu.plateau == 1) > np.sum(self.jeu.plateau == -1)):
      self.label.configure(
        text=
        f"Les blancs ont gagné :\n noir: {np.sum(self.jeu.plateau == -1)} \nblanc: {np.sum(self.jeu.plateau == 1)}"
      )
    elif (np.sum(self.jeu.plateau == 1) < np.sum(self.jeu.plateau == -1)):
      self.label.configure(
        text=
        f"Les noirs ont gagné :\n noir: {np.sum(self.jeu.plateau == -1)} \nblanc: {np.sum(self.jeu.plateau == 1)}"
      )
    else:
      self.label.configure(
        text=f"Egalité avec {np.sum(self.jeu.plateau == -1)} pour les 2 joueurs"
      )

  def Tour(self, manger, appeler=False):
    """
    Fonction qui permet de jouer un tour
    
    Args : 
      manger ((int, int)[][]): tableau qui contient des tuples définissant les coordonnées des pions que peut manger le joueur 
    """
    # si on est à la fin de la partie
    coord = [[i, j] for i in range(8) for j in range(8)
             if len(manger[i][j]) != 0]
    if len(coord) == 0:
      if appeler == False:
        self.jeu.joueur = -self.jeu.joueur
        self.Actualiser_plateau(True)
      else : 
        self.Fin()
    elif (self.jeu.nbjoueur == 1 and self.jeu.joueur == self.jeu.ordi):
      self.Tour_IA()
      self.Actualiser_plateau()
    mainloop()

  def Change_Plateau(self, i, j, manger):
    """
    Modifie le plateau de jeu en fonction du coup qui a été joué.

    Args:
      i (int): Coordonnée x du coup a joué.
      j (int): Coordonnée y du coup a joué.
      manger (list): tableau indiquant les pions mangé pour les positions qui ont été joué.

    Returns:
      None
    """
    self.jeu.plateau[i][j] = self.jeu.joueur
    for pion_mange in manger[i][j]:
      self.jeu.plateau[pion_mange[0]][pion_mange[1]] = self.jeu.joueur

  def EnterJoueur(self, i: int, j: int):
    """
    Fonction qui permet de jouer un coup
    
    Args:
        i (int): ligne
        j (int): colonne
    """
    self.Change_Plateau(i,j,self.jeu.Pose())
    self.jeu.joueur = -self.jeu.joueur
    self.Actualiser_plateau()

  def Pion_Pres(self):
    """Fonction qui préviens l'utilisateur qu'un pion est déjà présent"""
    self.label.configure(text="Un joueur est déjà présent")

  def Pas_Mange(self):
    """Fonction qui préviens qu'un pion peut être placé car il ne mange pas d'autre pion"""
    self.label.configure(text="Tu ne peux jouer ici")


if __name__ == "__main__":
  fenetre = Tk()
  interface = Interface(fenetre)
