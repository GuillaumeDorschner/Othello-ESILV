import numpy as np
import string
import MinMax as MM
from colored import fg, stylize


class Othello:

  def __init__(self, nbjoueur, joueurdep=1) -> None:
    """
    Créer l'objet Othello avec un nombre de joueurs et un joueur de départ.

    Args:
      nbjoueur (int): Nombre de joueurs.
      joueurdep (int, optional): Joueur qui commence. Par défaut, c'est le joueur 1. (1 blanc / -1 noir)

    Returns:
      None
    """
    self.nbjoueur = nbjoueur
    self.plateau = np.zeros((8, 8), dtype=int)
    self.tour = 0
    self.plateau[4][4] = self.plateau[3][3] = 1
    self.plateau[3][4] = self.plateau[4][3] = -1
    self.pion = {1: 2, -1: 2}
    self.joueur = 1
    self.joueur_depart = joueurdep

  def Affichage(self, manger):
    """
    Affiche le plateau avec les positions jouable.

    Args:
      manger (list): ???

    Returns:
      None
    """
    print(
      f"\n\ntour: {self.tour} \n noir: {np.sum(self.plateau == -1)} \nblanc: {np.sum(self.plateau == 1)} \n"
    )
    for i in range(len(self.plateau)):
      if (i == 0):
        print('|   || a || b || c || d || e || f || g || h |')
        print('____________________________________________')
      for j in range(len(self.plateau[i])):
        if (j == 0):
          print(f'| {i} |', end="")
        if self.plateau[i][j] == 1:
          print(stylize(f"| 1 |", fg('white')), end='')
        elif self.plateau[i][j] == -1:
          print(stylize(f"| 2 |", fg('black')), end="")
        elif len(manger[i][j]) > 0:
          print(stylize("| . |", fg('red')), end="")
        else:
          print(stylize("|   |", fg('green')), end="")
      print()
      print('_____________________________________________')

  def Tour(self):
    """
    Jour un tour de jeu.

    Args:
      None

    Returns:
      None
    """
    manger = self.Pose()
    self.Affichage(manger)
    if (self.nbjoueur == 2 or self.joueur == self.joueur_depart):
      coord = input(
        f'joueur {self.joueur}, où souhaitez vous placer votre pion ? ex: "e5"'
      )
      j = string.ascii_lowercase.index(coord[0])
      i = int(coord[1])
      while (not len(manger[i][j]) > 0):
        coord = input(
          f'joueur {self.joueur}, où souhaitez vous placer votre pion ? ex: "e5"'
        )
        j = string.ascii_lowercase.index(coord[0])
        i = int(coord[1])
      self.Change_Plateau(i, j, manger, self.joueur)
    else:
      best_x, best_y = MM.AlphaBetaSearch(self, self.joueur, 8)
      self.Change_Plateau(best_x, best_y, manger)
    self.joueur = -self.joueur

  def Change_Plateau(self, i, j, tab, retour=False):
    """
    Modifie le plateau de jeu en fonction du coup a joué.

    Args:
      i (int): Coordonnée x du coup a joué.
      j (int): Coordonnée y du coup a joué.
      manger (list): ???
      retour (bool, optional): ???

    Returns:
      None
    """
    plateau = self.plateau
    plateau[i][j] = self.joueur
    self.pion[self.joueur] += 1
    for pion_mange in tab[i][j]:
      plateau[pion_mange[0]][pion_mange[1]] = self.joueur
      self.pion[self.joueur] += 1
      self.pion[-self.joueur] -= 1
    self.tour += 1
    if (retour):
      return plateau
    else:
      self.plateau = plateau

  def Pose(self):
    """
    Retourne un tableau indiquant tous les pions mangé pour les positions a joué.

    Args:
      None

    Returns:
      list: Liste de coordonnées des pions qui peuvent être capturés.
    """
    manger = []
    for i in range(len(self.plateau)):
      manger.append([])
      for j in range(len(self.plateau[i])):
        if self.plateau[i][j] == 0:
          manger[i].append(self.Manger(i, j))
        else:
          manger[i].append([])
    return manger

  def Manger(self, i, j):
    """
    ???

    Args:
      i (int): Coordonnée x de la position.
      j (int): Coordonnée y de la position.

    Returns:
      list: ???
    """
    output = []
    tabi = [-1, -1, -1, 0, 0, 1, 1, 1]
    tabj = [-1, 0, 1, -1, 1, -1, 0, 1]
    for index in range(len(tabi)):
      x = i + tabi[index]
      y = j + tabj[index]
      if x in range(8) and y in range(8):
        buffer = []
        while self.plateau[x][y] == -self.joueur:
          buffer.append((x, y))
          x = x + tabi[index]
          y = y + tabj[index]
          if not (0 <= x < len(self.plateau) and 0 <= y < len(self.plateau)):
            x = x - tabi[index]
            y = y - tabj[index]
            break
        if (self.plateau[x][y] == self.joueur and len(buffer) > 0):
          output += buffer
    return output


def Affichage(plateau):
  """
  Affiche le plateau de jeu avec des indications True ou False pour chaque position.

  Args:
    plateau (int[][]): plateau de Othello Object (ex: Jeu.plateau) 

  Returns:
    None
  """

  for i in range(len(plateau)):
    if (i == 0):
      print(
        '|   ||   a   ||   b   ||   c   ||   d   ||   e   ||   f   ||   g   ||   h   |'
      )
      print(
        '_____________________________________________________________________________'
      )
    for j in range(len(plateau[i])):
      if (j == 0):
        print(f'| {i} |', end="")
      if len(plateau[i][j]) > 0: print(f'\033[92m| True |', end="")
      else: print(f'\033[93m| False |', end="")
    print()
    print(
      '________________________________________________________________________________'
    )


def Game():
  """
  Fonction pour Run l'Othello.

  Args:
    None

  Returns:
    None
  """

  jeu = Othello(1, 1)
  #AlphaBetaSearch(jeu)
  while (jeu.tour < 59):
    jeu.Tour()


Game()
