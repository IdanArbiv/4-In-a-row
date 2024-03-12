CELL_CLEAR = '-';
PLAYER_WHITE = 'W';
PLAYER_BLACK = 'B';

def inputToCellCode(cell):
    if cell == 'C' or cell == '0':
        return CELL_CLEAR
    elif cell == 'W' or cell == '1':
        return PLAYER_WHITE
    elif cell == 'B' or cell == '2':
        return PLAYER_BLACK

import sys
import os

class ReversiBoard():
    
    def __init__(self, boardPath = None):
        self.ply = 0
        self.currentPlayer = PLAYER_WHITE
        self.cells = [[CELL_CLEAR for x in range(8)] for x in range(8)]
        if boardPath == None:
            self.cells[3][3] = PLAYER_WHITE
            self.cells[4][4] = PLAYER_WHITE
            self.cells[3][4] = PLAYER_BLACK
            self.cells[4][3] = PLAYER_BLACK
        else:
            try:
                print("Opening init file...\n")
                f = open(boardPath, 'r')
                lines = f.readlines()
                for i in range(8):
                    cells = lines[i].split()
                    for j in range(8):
                        self.cells[i][j] = inputToCellCode(cells[j])
                if lines[len(lines)-1].find("TURN") != -1:
                    self.currentPlayer = (PLAYER_WHITE if lines[len(lines)-1].split()[1].strip() == 'W' else PLAYER_BLACK)
            except Exception:
                print ("Failed to load data, exiting...")
                os._exit(1)
            f.close()

    def clone(self):
        newBoard = ReversiBoard()
        newBoard.currentPlayer = self.currentPlayer
        newBoard.ply = self.ply
        for i in range(8):
            for j in range(8):
                newBoard.cells[i][j] = self.cells[i][j]
        return newBoard 
        
    def printMe(self):
        print()
        whiteScore = 0
        blackScore = 0
        for i in range(8):
            for j in range(8):
                whiteScore += (1 if (self.cells[i][j] == PLAYER_WHITE) else 0)
                blackScore += (1 if (self.cells[i][j] == PLAYER_BLACK) else 0)
        print("Scores:\n======\nWhite:", whiteScore, "| Black:", blackScore, "\n")
                
        print("  0 1 2 3 4 5 6 7")
        print(" +----------------+")
        for i in range(8):
            sys.stdout.write(str(i) + "|")
            for j in range(8):
                sys.stdout.write(str(self.cells[i][j]) + " ")
            sys.stdout.write("|")
            print()
        print(" +----------------+")
    
    def getPossibleMoves(self, p1):
        moves = []
        if p1==PLAYER_BLACK:
            p2 = PLAYER_WHITE
        else:
            p2 = PLAYER_BLACK
            
        for i in range(8):
            for j in range(8):
                moveFound = False
                if self.cells[i][j] == CELL_CLEAR:
                    # Look N
                    if i>0:
                        moveFound = moveFound or validDirection(self, i-1, j, -1, 0, p1, p2)
                    # Look NE
                    if i>0 and j<7:
                        moveFound = moveFound or validDirection(self, i-1, j+1, -1, +1, p1, p2)
                    # Look E
                    if j<7:
                        moveFound = moveFound or validDirection(self, i, j+1, 0, +1, p1, p2)
                    # Look SE
                    if i<7 and j<7:
                        moveFound = moveFound or validDirection(self, i+1, j+1, +1, +1, p1, p2)
                    # Look S
                    if i<7:
                        moveFound = moveFound or validDirection(self, i+1, j, +1, 0, p1, p2)
                    # Look SW
                    if i<7 and j>0:
                        moveFound = moveFound or validDirection(self, i+1, j-1, +1, -1, p1, p2)
                    # Look W
                    if j>0:
                        moveFound = moveFound or validDirection(self, i, j-1, 0, -1, p1, p2)
                    # Look NW
                    if i>0 and j>0:
                        moveFound = moveFound or validDirection(self, i-1, j-1, -1, -1, p1, p2)
                if moveFound:
                    moves.append((p1, i, j))
        return moves

    def executeMove(self, move):
        p1 = move[0]
        if p1==PLAYER_BLACK:
            p2 = PLAYER_WHITE
        else:
            p2 = PLAYER_BLACK
        
        i = move[1]
        j = move[2]
        
        if self.cells[i][j] != CELL_CLEAR:
            raise BadMoveException
        
        self.cells[i][j] = p1   # Put piece in selected cell
        
        # Look N
        if i>0:
            moveOK = validDirection(self, i-1, j, -1, 0, p1, p2)
            if moveOK:
                flipDirection(self, i-1, j, -1, 0, p1, p2)
        # Look NE
        if i>0 and j<7:
            moveOK = validDirection(self, i-1, j+1, -1, +1, p1, p2)
            if moveOK:
                flipDirection(self, i-1, j+1, -1, +1, p1, p2)
        # Look E
        if j<7:
            moveOK = validDirection(self, i, j+1, 0, +1, p1, p2)
            if moveOK:
                flipDirection(self, i, j+1, 0, +1, p1, p2)
        # Look SE
        if i<7 and j<7:
            moveOK = validDirection(self, i+1, j+1, +1, +1, p1, p2)
            if moveOK:
                flipDirection(self, i+1, j+1, +1, +1, p1, p2)
        # Look S
        if i<7:
            moveOK = validDirection(self, i+1, j, +1, 0, p1, p2)
            if moveOK:
                flipDirection(self, i+1, j, +1, 0, p1, p2)
        # Look SW
        if i<7 and j>0:
            moveOK = validDirection(self, i+1, j-1, +1, -1, p1, p2)
            if moveOK:
                flipDirection(self, i+1, j-1, +1, -1, p1, p2)
        # Look W
        if j>0:
            moveOK = validDirection(self, i, j-1, 0, -1, p1, p2)
            if moveOK:
                flipDirection(self, i, j-1, 0, -1, p1, p2)
        # Look NW
        if i>0 and j>0:
            moveOK = validDirection(self, i-1, j-1, -1, -1, p1, p2)    
            if moveOK:
                flipDirection(self, i-1, j-1, -1, -1, p1, p2)
        
        self.currentPlayer = (PLAYER_WHITE if self.currentPlayer == PLAYER_BLACK else PLAYER_BLACK)
        self.ply -= 1 
    
def validDirection(board, i, j, dy, dx, p1, p2):
    if (i>=0 and i<8 and j>=0 and j<8 and board.cells[i][j]==p2):
        while (i>=0 and i<8 and j>=0 and j<8 and board.cells[i][j]==p2):
            i += dy
            j += dx
        return (i>=0 and i<8 and j>=0 and j<8 and board.cells[i][j]==p1)
    return False

def flipDirection(board, i, j, dx, dy, p1, p2):
    if (i>=0 and i<8 and j>=0 and j<8 and board.cells[i][j]==p2):
        while (i>=0 and i<8 and j>=0 and j<8 and board.cells[i][j]==p2):
            board.cells[i][j] = p1
            i += dx
            j += dy

def BadMoveException():
    pass
