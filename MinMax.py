import math
import numpy as np
import copy
import time


def MinVal(jeu, A, B, profondeur, playeur):
  nbCoup = np.sum(jeu.plateau != 0)

  if profondeur == 0 or nbCoup > 63:
    return evaluate(jeu, playeur, nbCoup)

  v = +math.inf
  tab = jeu.Pose()
  coord = [[i, j] for i in range(8) for j in range(8) if len(tab[i][j]) != 0]
  for i in coord:
    new_jeu = copy.deepcopy(jeu)
    new_jeu.Change_Plateau(i[0], i[1], tab, False)
    v = min(v, MaxVal(new_jeu, A, B, profondeur - 1, -playeur))
    if v <= A:
      return v
    B = min(B, v)
  return v


def MaxVal(jeu, A, B, profondeur, playeur):
  nbCoup = np.sum(jeu.plateau != 0)

  if profondeur == 0 or nbCoup > 63:
    return evaluate(jeu, playeur, nbCoup)
  tab = jeu.Pose()
  coord = [[i, j] for i in range(8) for j in range(8) if len(tab[i][j]) != 0]
  v = -math.inf
  for i in coord:
    new_jeu = copy.deepcopy(jeu)
    new_jeu.Change_Plateau(i[0], i[1], tab, False)
    v = max(v, MinVal(new_jeu, A, B, profondeur - 1, -playeur))
    if v >= B:
      return v
    A = max(A, v)
  return v


def timeur(fonction):

  def inner(*args, **kwargs):
    debut = time.perf_counter()
    res = fonction(*args, **kwargs)
    fin = time.perf_counter()
    print(f"Temps d'exécution : {fin - debut}")
    return res

  return inner


@timeur
def AlphaBetaSearch(jeu, playeur, profondeur=4):
  """
  Fonction qui retourne le coup à jouer
  
  Args:
    jeu (Othello Object): Le jeu Othello
    playeur (int): 1 ou -1 pour dire qui joue
    profondeur (int): quelle taille devra faire l'arbre de MinMax (depth)

  Returns:
    (x, y): La position a jouer
  """
  best_move = None
  best_score = -math.inf
  score = -math.inf
  A = math.inf
  B = -math.inf

  tab = jeu.Pose()
  coord = [[i, j] for i in range(8) for j in range(8) if len(tab[i][j]) != 0]
  for i in coord:
    new_jeu = copy.deepcopy(jeu)
    new_jeu.Change_Plateau(i[0], i[1], tab, False)
    score = MinVal(new_jeu, A, B, profondeur - 1, -playeur)
    if score > best_score:
      best_score = score
      best_move = i
  
  return tuple(best_move)


def evaluate(jeu, player, phase):
  """
  Calcule la qualité du coup joué.

  Args:
      jeu (object): Un objet Othello.
      coordonnee (tuple): coordonnées x, y représentant la case jouée.
      player (int): Quelle joueur jouant le coup.
      phase (str): str représentant la phase du jeu ("beginning", "middle" ou "end").

  Returns:
      float: Le score calculé en fonction de plusieurs critères de notre heuristique.
  """

  if phase < 12:
    weights = [1, 1, 1]
  elif phase < 52:
    weights = [1, 1, 1]
  else:
    weights = [1, 1]

  nbPion = np.sum(jeu.plateau == player)

  coinBord = np.array(
    [[True, False, True, True, True, True, False, True],
     [False, False, False, False, False, False, False, False],
     [True, False, False, False, False, False, False, True],
     [True, False, False, False, False, False, False, True],
     [True, False, False, False, False, False, False, True],
     [True, False, False, False, False, False, False, True],
     [False, False, False, False, False, False, False, False],
     [True, False, True, True, True, True, False, True]])

  zoneDanger = np.array(
    [[False, True, False, False, False, False, True, False],
     [True, True, True, True, True, True, True, True],
     [False, True, False, False, False, False, True, False],
     [False, True, False, False, False, False, True, False],
     [False, True, False, False, False, False, True, False],
     [False, True, False, False, False, False, True, True],
     [True, True, True, True, True, True, True, True],
     [False, True, False, False, False, False, True, False]])

  bord_corner_score = np.sum(coinBord * (jeu.plateau == player)) * 2
  zoneDanger_score = np.sum(zoneDanger * (jeu.plateau == player)) * -1

  coupValide = jeu.Pose()
  coupValide = [[i, j] for i in range(8) for j in range(8)
                if len(coupValide[i][j]) != 0]
  mobility = len(coupValide)

  distance_score = 0

  if phase < 12:
    distance_score = sum(
      [calculer_distance_centre(coordonne) for coordonne in coupValide])

    score = weights[0] * (bord_corner_score + zoneDanger_score
                          ) + weights[1] * nbPion + weights[2] * distance_score
  elif phase < 52:
    score = weights[0] * (bord_corner_score + zoneDanger_score
                          ) + weights[1] * nbPion + weights[2] * mobility
  else:
    score = weights[0] * nbPion + weights[1] * (bord_corner_score)

  return score


def calculer_distance_centre(coordonne):
  ''' Pythagore distance entre la coordonnée est le centre du plateau '''
  distance = math.sqrt((coordonne[0] - 3.5)**2 + (coordonne[1] - 3.5)**2)
  return distance
