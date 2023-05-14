import math
import numpy as np
import copy
import time


def MinVal(jeu, A, B, profondeur):
  """
  Fonction MinVal pour l'algorithme Minimax avec élagage Alpha-Beta.
  
  Args:
    jeu (Othello Object): Le jeu Othello
    A (int): Valeur Alpha pour l'élagage
    B (int): Valeur Beta pour l'élagage
    profondeur (int): La profondeur actuelle de l'arbre de recherche
  
  Returns:
    v (int): La valeur minimale calculée pour le joueur à cette profondeur
  """

  nbCoup = np.sum(jeu.plateau != 0)

  jeu.deep += 1

  v = +math.inf
  manger = jeu.Pose()
  coord = [[i, j] for i in range(8) for j in range(8)
           if len(manger[i][j]) != 0]

  if profondeur == 0 or nbCoup > 64 or len(coord) == 0:
    return evaluate(jeu, nbCoup)

  for i in coord:
    new_jeu = copy.deepcopy(jeu)
    new_jeu.Change_Plateau(i[0], i[1], manger)
    new_jeu.joueur = -new_jeu.joueur
    v = min(v, MaxVal(new_jeu, A, B, profondeur - 1))
    if v <= A:
      return v
    B = min(B, v)
  return v


def MaxVal(jeu, A, B, profondeur):
  """
  Fonction MaxVal pour l'algorithme Minimax avec élagage Alpha-Beta.
  
  Args:
    jeu (Othello Object): Le jeu Othello
    A (int): Valeur Alpha pour l'élagage
    B (int): Valeur Beta pour l'élagage
    profondeur (int): La profondeur actuelle de l'arbre de recherche
  
  Returns:
    v (int): La valeur maximale calculée pour le joueur à cette profondeur
  """
  nbCoup = np.sum(jeu.plateau != 0)

  jeu.deep += 1

  v = -math.inf
  manger = jeu.Pose()
  coord = [[i, j] for i in range(8) for j in range(8)
           if len(manger[i][j]) != 0]

  if profondeur == 0 or nbCoup > 64 or len(coord) == 0:
    return evaluate(jeu, nbCoup)

  for i in coord:
    new_jeu = copy.deepcopy(jeu)
    new_jeu.Change_Plateau(i[0], i[1], manger)
    new_jeu.joueur = -new_jeu.joueur
    v = max(v, MinVal(new_jeu, A, B, profondeur - 1))
    if v >= B:
      return v
    A = max(A, v)
  return v


def timeur(fonction):

  def inner(*args, **kwargs):
    debut = time.perf_counter()
    res = fonction(*args, **kwargs)
    fin = time.perf_counter()
    temps = fin - debut
    inner.temps = temps
    print(f"Temps d'exécution : {temps}")
    return res

  return inner


@timeur
def AlphaBetaSearch(jeu, manger, profondeur=4):
  """
  Fonction qui retourne le coup à jouer
  
  Args:
    jeu (Othello Object): Le jeu Othello
    manger (int): liste des pions que l'on peut manger
    profondeur (int): quelle taille devra faire l'arbre de MinMax (depth)

  Returns:
    (x, y): La position a jouer
  """
  best_move = None
  best_score = -math.inf
  score = -math.inf
  A = -math.inf
  B = math.inf

  jeu.deep += 1

  coord = [[i, j] for i in range(8) for j in range(8)
           if len(manger[i][j]) != 0]
  for i in coord:
    new_jeu = copy.deepcopy(jeu)
    new_jeu.Change_Plateau(i[0], i[1], manger)
    new_jeu.joueur = -new_jeu.joueur
    score = MinVal(new_jeu, A, B, profondeur - 1)
    if score > best_score:
      best_score = score
      best_move = i
    A = max(A, best_score)

  return tuple(best_move)


def evaluate(jeu, phase):
  """
  Calcule la qualité du coup joué.

  Args:
      jeu (object): Un objet Othello.
      coordonnee (tuple): coordonnées x, y représentant la case jouée.
      phase (str): str représentant la phase du jeu ("beginning", "middle" ou "end").

  Returns:
      float: Le score calculé en fonction de plusieurs critères de notre heuristique.

  Poids répartis entre 0 et 3 en fonction de l'importance de la stratégie lors du moment de la partie
  """
  if phase < 12:
    weights = [20, 4, 2, 1, 2]
  elif phase < 52:
    weights = [25, 4, 2, 1, 1]
  else:
    weights = [25, 1, 6]

  nbPion = np.sum(jeu.plateau == jeu.joueur)

  bord = np.array([[False, False, True, True, True, True, False, False],
                   [False, False, False, False, False, False, False, False],
                   [True, False, False, False, False, False, False, True],
                   [True, False, False, False, False, False, False, True],
                   [True, False, False, False, False, False, False, True],
                   [True, False, False, False, False, False, False, True],
                   [False, False, False, False, False, False, False, False],
                   [False, False, True, True, True, True, False, False]])

  coin = np.array([[True, False, False, False, False, False, False, True],
                   [False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False],
                   [False, False, False, False, False, False, False, False],
                   [True, False, False, False, False, False, False, True]])

  zoneDanger = np.array(
    [[False, True, False, False, False, False, True, False],
     [True, True, True, True, True, True, True, True],
     [False, True, False, False, False, False, True, False],
     [False, True, False, False, False, False, True, False],
     [False, True, False, False, False, False, True, False],
     [False, True, False, False, False, False, True, True],
     [True, True, True, True, True, True, True, True],
     [False, True, False, False, False, False, True, False]])

  bord_score = np.sum(bord * (jeu.plateau == jeu.joueur))
  corner_score = np.sum(coin * (jeu.plateau == jeu.joueur))
  zoneDanger_score = -np.sum(zoneDanger * (jeu.plateau == jeu.joueur))

  coupValide = jeu.Pose()
  coupValide = [[i, j] for i in range(8) for j in range(8)
                if len(coupValide[i][j]) != 0]
  mobility = len(coupValide)

  distance_score = 0

  if phase < 12:
    distance_score = sum(
      [calculer_distance_centre(coordonne) for coordonne in coupValide])

    score = weights[0] * corner_score * jeu.deep + weights[
      1] * bord_score + weights[2] * zoneDanger_score + weights[
        3] * nbPion + weights[4] * distance_score
  elif phase < 52:
    score = weights[0] * corner_score * jeu.deep + weights[
      1] * bord_score + weights[2] * zoneDanger_score + weights[
        3] * nbPion + weights[4] * mobility
  else:
    score = weights[0] * corner_score * jeu.deep + weights[
      1] * bord_score + weights[2] * nbPion

  return score


def calculer_distance_centre(coordonne):
  ''' Pythagore distance entre la coordonnée est le centre du plateau '''
  distance = math.sqrt((coordonne[0] - 3.5)**2 + (coordonne[1] - 3.5)**2)
  return distance
