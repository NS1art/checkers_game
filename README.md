### Checkers Game

# Introduction

This is a checkers game developed with Python/PyGame, following TechWithTim's tutorial. 
https://www.youtube.com/watch?v=mYbrH1Cl3nw

# Educational objective

The aim of this project is to understand theorically the logic behind a Minimax algorithm and then implement a Minimax-based Artificial Intelligence which knows how to play the Checkers Game and how to beat a human player.

# Packages used in this code

- Pygame

# Code organization

The first step of the project was to build a classic and interactive Checkers Game.
The branch `main` corresponds to the first version of the Checkers Game, where the user can plays both players 1 and 2.
`constants.py` contains all constant variables called in the different python scripts. 
`board.py` contains the class Board including all the methods used to define the Checkers board design (the number of squares, the remaining number of pieces for each player, the state of the board...)
`piece.py` contains the class Piece including all the methods used to define anything related to a Checker piece (the color, the position on the board...)
`game.py` contains the class Game including all the methods required to play the Checkers Game (move the pieces, check valid moves, change players turns...)

In a second step, the Minimax algorithm was added and corresponds to the player 2, aka the Artificial Intelligence.
The branch `ia-minimax` corresponds to this "advanced" version of the Checkers Game, where the user can only be the player 1 and (hopefully) gets beated by the player 2!

# How to run the game

Clone the repository and switch to branch `ia-minimax`.
Be sure that Pygame is installed in your local environment before attempting to run the game.
Then in the root of the repository, run `main.py` and start playing against the AI!