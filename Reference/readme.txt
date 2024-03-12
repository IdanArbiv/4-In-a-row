=============================
     PyReversi - Readme
=============================

Welcome! Following is a brief explanation on how to run and use the source code for
my simple Reversi implementation.
The code was written as part of a larger project for a computer vision system for
real-time tracking of a physical board game, as well as suggesting moves based on
a simple AI. The full project may be found at:
http://www.cs.bgu.ac.il/~ben-shahar/Teaching/Computational-Vision/StudentProjects/ICBV121/ICBV-2013-1-NadavErell/index.php

As such, the code can be used in two separate modes:
- Standalone Reversi game
- Single move processing

Standalone Reversi game
=======================
Simply run the file Reversi.py. It will display instructions on screen for selecting
Player vs Player, Player vs Computer, or Computer vs Computer play mode.
Each turn, all legal moves will be presented for you to choose from.

Single move processing
======================
This mode is used as a utility for the main system written in MATLAB, and processes
a single move from a given board state, suggesting moves for either player.
To use this mode, run the file ReversiSingleMove.py. Input is an 8x8 grid of the
numbers 0, 1 or 2, or alternatively characters 'C', 'W', or 'B', representing a clear
slot, a white disc or a black disc respectively.

Input: board.ini
Output: whiteMove.txt, blackMove.txt

Other files
===========
The files ReversiBoard.py, ReversiAgents.py and Game_Searches.py contain the main mechanism
of the game, and are pretty self-explanatory.
Game_Searches.py contains implementations of a Minimax algorithm with some variations, 
and is not specific to the Reversi problem.


You are completely free to use this code in whatever way you please, for whatever purpose.

Nadav Erell
erelln@post.bgu.ac.il


21 March, 2013