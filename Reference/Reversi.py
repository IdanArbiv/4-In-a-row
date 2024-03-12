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
    #board = ReversiBoard("board.ini")
    board = ReversiBoard()
    board.printMe()
    
#    moves = board.getPossibleMoves(PLAYER_WHITE)

    #==============================================#
    #          Query user for parameters           #
    #==============================================#    
    print("\n\n\nReady to play some Reversi?")
    gameType = 0
    while gameType <= 0 or gameType > 3:
        gameType = int(input("\nChoose game type:\n1. Human vs. Human\n2. Human vs Computer\n3. Computer vs Computer"))
    
    if gameType == 1:
        player1 = HumanAgent(PLAYER_WHITE)
        player2 = HumanAgent(PLAYER_BLACK)
    elif gameType == 2:
        color = 0
        while color <= 0 or color > 2:
            color = int(input("\nDo you wish to play (1) White or (2) Black?"))
        if color == 1:
            player1 = HumanAgent(PLAYER_WHITE)
            player2 = ComputerAgent(PLAYER_BLACK)
        else:
            player2 = HumanAgent(PLAYER_BLACK)
            player1 = ComputerAgent(PLAYER_WHITE)
    else:
        player1 = ComputerAgent(PLAYER_WHITE)
        player2 = ComputerAgent(PLAYER_BLACK)
            

    #==============================================#
    #               Run game till done             #
    #==============================================#  

    moveCounter = 1
    Done = False
    while (not Done):
        cls()
        board.printMe()
        if board.currentPlayer == PLAYER_WHITE:
            print("\nMove: White\n")            
            player = (player1 if player1.color == PLAYER_WHITE else player2)
            
        elif board.currentPlayer == PLAYER_BLACK:
            print("\nMove: Black\n")            
            player = (player1 if player1.color == PLAYER_BLACK else player2)

        if isinstance(player, ComputerAgent):
            getAnyKey()
        move = player.getMove(board)
        print(move)
        if move != None:
            board.executeMove(move)
        else:
            board.currentPlayer = (PLAYER_BLACK if board.currentPlayer == PLAYER_WHITE else PLAYER_WHITE)         
        
        
        moveCounter += 1
        
        Done = (len(board.getPossibleMoves(PLAYER_BLACK)) == 0 and len(board.getPossibleMoves(PLAYER_WHITE)) == 0)
    
    board.printMe()
    print('Game ended\n')
    getAnyKey()


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
