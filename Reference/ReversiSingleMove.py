#-------------------------------------------------------------------------------
# Name:        Reversi
# Purpose:     
#              
#
# Author:      Nadav Erell
#
# Created:     02/02/2013
#-------------------------------------------------------------------------------

from ReversiBoard import *
from ReversiAgents import *
import random
from os import system

def main():
    
    #==============================================#
    #          Initialize board state from file    #
    #==============================================#
    board = ReversiBoard("board.ini")

    player1 = ComputerAgent(PLAYER_WHITE)
    player2 = ComputerAgent(PLAYER_BLACK)
            

    cls()
    board.printMe()

    move1 = player1.getMove(board)
    board.currentPlayer = PLAYER_BLACK
    move2 = player2.getMove(board)
    print("\nMove: White\n")            
    print(move1)
    f = open('whiteMove.txt', 'w')
    if move1:
        f.write(str(move1[1]) + " " + str(move1[2]))
    else:
        f.write("-1 -1")
    f.close()
    print("\nMove: Black\n")            
    print(move2)
    f = open('blackMove.txt', 'w')
    if move2:
        f.write(str(move2[1]) + " " + str(move2[2]))
    else:
        f.write("-1 -1")
    f.close()

        
    Done = (len(board.getPossibleMoves(PLAYER_BLACK)) == 0 and len(board.getPossibleMoves(PLAYER_WHITE)) == 0)

    if Done:
        board.printMe()
        print('Game ended\n')

    #getAnyKey()


class reversiGameState():
    def __init__(self, board, currentPlayer):
        self.board = board
        self.currentPlayer = currentPlayer

class reversiSearchState():
    def __init__(self, board, currentPlayer, ply):
        self.board = board
        self.currentPlayer = currentPlayer
        self.ply = ply


def cls():
    try:
        os.system('cls') #windows
    except Exception:
        os.system('clear') #linux
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

def getAnyKey():
    print('\nPress Enter to continue')
    x = 0
    try:
        x = int(input())
        if x > 0:
            return x
    except:
        pass

if __name__ == "__main__":
    main()
