# Jeu Othello avec IA
Ce dépôt contient une implémentation Python du jeu Othello (Reversi), y compris un adversaire IA qui utilise l'algorithme Minimax avec élagage Alpha-Beta et des heuristiques personnalisées pour les différentes phases du jeu.

## Caractéristiques
- Interface utilisateur textuelle
- Jeu humain contre IA
- Algorithme Minimax avec élagage Alpha-Beta pour la prise de décision de l'IA
- heuristique personnalisée pour les phases de début, de milieu et de fin de partie
- Possibilité d'afficher les coups disponibles pour le joueur actuel

## Getting Started
Conditions préalables
Python 3.x
Installation de l'application
Clonez le dépôt :
```bash
git clone https://github.com/yourusername/othello-ai.git](https://github.com/GuillaumeDorschner/Othello-ESILV.git
```
Naviguez jusqu'au répertoire du projet :
```bash
cd Othello-ESILV
```

## Lancer le jeu
Pour lancer le jeu, il suffit d'exécuter le fichier main.py :

```bash
python main.py
```

## Comment jouer
Au début du jeu, le joueur peut choisir d'incarner les Noirs ou les Blancs. Les Noirs jouent toujours en premier. L'échiquier sera affiché dans la ligne de commande, avec B (noirs), W (blancs).

Pendant son tour, le joueur doit entrer la ligne et la colonne du coup désiré. L'IA effectue alors son déplacement et le tableau mis à jour s'affiche.

Le jeu se poursuit jusqu'à ce qu'il n'y ait plus de mouvements légaux pour l'un ou l'autre des joueurs ou que le plateau soit plein. Le joueur qui a le plus de pions de sa couleur sur le plateau gagne.

## Stratégie de l'IA
L'IA utilise un algorithme Minimax avec élagage Alpha-Beta pour rechercher l'arbre de jeu et décider du meilleur coup. La fonction d'évaluation prend en compte différents facteurs en fonction de la phase de jeu en cours (début, milieu ou fin) :

Début (12 premiers coups) :
- Priorité au placement des pions loin du centre
- Priorité au gain de pions

Milieu (36 coups suivants) :
- Priorité aux positions de bord et de coin
- Priorité à l'acquisition de pions
- Privilégier les coups qui permettent une mobilité future

Fin (12 derniers coups) :
- Donner la priorité au gain de pions
- Priorité aux coins importants
Ces heuristiques aident l'IA à adapter sa stratégie à l'évolution de l'état du jeu et à créer un adversaire plus stimulant.

## Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
