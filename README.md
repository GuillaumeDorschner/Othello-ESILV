# Othello Game with AI
This repository contains a Python implementation of the Othello (Reversi) game, including an AI opponent that uses the Minimax algorithm with Alpha-Beta pruning and custom heuristics for different phases of the game.

## Quick demo
https://github.com/GuillaumeDorschner/Othello-ESILV/assets/44686652/1a1ded84-62cb-431d-b99a-0e3403b91171

## Getting Started
Prerequisites:
Python 3.x
Application Installation:
Clone the repository:
```bash
git clone https://github.com/GuillaumeDorschner/Othello-ESILV.git
```
Navigate to the project directory:
```bash
cd Othello-ESILV
```

## Launching the Game
To start the game, simply run the main.py file:
```bash
python main.py
```

## How to Play
At the beginning of the game, the player can choose to play as Black or White. Black always plays first. The chessboard will be displayed in the command line, with B (black), W (white).
During their turn, the player must enter the row and column of the desired move. The AI then makes its move, and the updated board is displayed.
The game continues until there are no more legal moves for either player or the board is full. The player with the most pieces of their color on the board wins.


## Features
- Textual user interface
- Human versus AI gameplay
- Minimax algorithm with Alpha-Beta pruning for AI decision-making
- Custom heuristics for the early, middle, and endgame phases
- Ability to display available moves for the current player

## AI Strategy
The AI uses a Minimax algorithm with Alpha-Beta pruning to search the game tree and decide on the best move. The evaluation function considers different factors depending on the current game phase (beginning, middle, or end):

Beginning (first 12 moves):

Priority on placing pieces away from the center
Priority on capturing pieces
Middle (next 36 moves):

Priority on edge and corner positions
Priority on capturing pieces
Favor moves that allow future mobility
End (last 12 moves):

Priority on capturing pieces
Priority on important corners
These heuristics help the AI adapt its strategy to the evolving game state and create a more challenging opponent.

## License
This project is under the MIT license. See the LICENSE file for more details.
