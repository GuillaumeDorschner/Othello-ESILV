"""
Titre du programme : Projet Othello
Auteur : Guillaume Dorschner / Valentin Grateau / Louis Anne
Date de création : 17/04/2023
Description : jeu d'Othello avec IA MinMax 
"""

import Othello_IG as IG
from tkinter import Tk

#création de la fenêtre de jeu
fenetre = Tk()

#lancement du jeu
interface = IG.Interface(fenetre)
