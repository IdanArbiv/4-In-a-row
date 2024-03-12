#-------------------------------------------------------------------------------
# Name:        ReversiAgents
# Purpose:     
#
# Author:      Nadav Erell
#
# Created:     02/02/2013
#-------------------------------------------------------------------------------

from Game_Searches import *
from ReversiBoard import *

class Agent:
    TYPE_HUMAN = 1
    TYPE_COMPUTER = 2
    
    def __init__(self):
        pass

    def performMove(self, gameState, move):
        print(str(self),"Performing move:")
        print(move)
        raise NotImplementedError

class HumanAgent(Agent):
    def __init__(self, color):
        self.color = color

    def getMove(self, board):
        moves = board.getPossibleMoves(board.currentPlayer)
        if len(moves) == 0:
            return None
        print("Choose move:")
        for (i, move) in enumerate(moves):
            print("".join((str(i+1), ". ", str(move))))
        choice = -1
        while choice <= 0 or choice > len(moves):
            try:
                choice = int(input())
            except:
                pass
        return moves[choice-1]

class ComputerAgent():
    def __init__(self, color):
        self.color = color
        
    def getMove(self, board):
        newBoard = board.clone()
        newBoard.ply = 4
        prob = ReversiGameProblem(newBoard, 1)
        
        if self.color == PLAYER_WHITE: 
            return MaxiMinAlphaBeta(prob, newBoard)
        if self.color == PLAYER_BLACK: 
            return MiniMaxAlphaBeta(prob, newBoard)


class ReversiGameProblem(GameTreeProblem):
    
    def __init__(self, initialState, heuristic):
        self.initialState = initialState
        self.h = heuristic

    def TerminalTest(self, boardState):
        return (len(boardState.getPossibleMoves(PLAYER_BLACK)) == 0 and len(boardState.getPossibleMoves(PLAYER_WHITE)) == 0) 

    def CutoffTest(self, boardState):
        return boardState.ply == 0


    # Heuristic evaluation for non terminal board states
    def Eval(self, boardState):
        whiteScore = 0
        blackScore = 0
        for i in range(8):
            for j in range(8):
                whiteScore += (1 if (boardState.cells[i][j] == PLAYER_WHITE) else 0)
                blackScore += (1 if (boardState.cells[i][j] == PLAYER_BLACK) else 0)
        
        # Frame cells are worth double
        for i in range(8):
            whiteScore += (1 if (boardState.cells[i][0] == PLAYER_WHITE) else 0)
            blackScore += (1 if (boardState.cells[i][0] == PLAYER_BLACK) else 0)
            whiteScore += (1 if (boardState.cells[i][7] == PLAYER_WHITE) else 0)
            blackScore += (1 if (boardState.cells[i][7] == PLAYER_BLACK) else 0)
        for j in range(8):
            whiteScore += (1 if (boardState.cells[0][j] == PLAYER_WHITE) else 0)
            blackScore += (1 if (boardState.cells[0][j] == PLAYER_BLACK) else 0)
            whiteScore += (1 if (boardState.cells[7][j] == PLAYER_WHITE) else 0)
            blackScore += (1 if (boardState.cells[7][j] == PLAYER_BLACK) else 0)

        # Corners worth additional 5, total is 8
            whiteScore += (5 if (boardState.cells[0][0] == PLAYER_WHITE) else 0)
            blackScore += (5 if (boardState.cells[0][0] == PLAYER_BLACK) else 0)
            whiteScore += (5 if (boardState.cells[0][7] == PLAYER_WHITE) else 0)
            blackScore += (5 if (boardState.cells[0][7] == PLAYER_BLACK) else 0)
            whiteScore += (5 if (boardState.cells[7][0] == PLAYER_WHITE) else 0)
            blackScore += (5 if (boardState.cells[7][0] == PLAYER_BLACK) else 0)
            whiteScore += (5 if (boardState.cells[7][7] == PLAYER_WHITE) else 0)
            blackScore += (5 if (boardState.cells[7][7] == PLAYER_BLACK) else 0)

        return (whiteScore - blackScore)

    # Actual final score if board is in terminal state
    def Utility(self, boardState):
        whiteScore = 0
        blackScore = 0
        for i in range(8):
            for j in range(8):
                whiteScore += (1 if (boardState.cells[i][j] == PLAYER_WHITE) else 0)
                blackScore += (1 if (boardState.cells[i][j] == PLAYER_BLACK) else 0)
        return (whiteScore - blackScore)       

    def Successors(self, boardState):
        moves = boardState.getPossibleMoves(boardState.currentPlayer)
        succs = []
        for move in moves:
            newBoard = boardState.clone()
            newBoard.executeMove(move)
            succs.append((move, newBoard))
        return succs
