"""
This Connect Four player uses a minimax algotithm to decide the bests move to make
"""
__author__ = "Ben McAuliffe"
__license__ = "MIT"
__date__ = "March 2023"

import random
import time
import numpy as np
import math
import connect4
from connect4 import print_rack

class ComputerPlayer:
    def __init__(self, id, difficulty_level):
        """
        Constructor, takes a difficulty level (likely the # of plies to look
        ahead), and a player ID that's either 1 or 2 that tells the player what
        its number is.
        """
        self.id = id
        self.difficulty_level = difficulty_level

    def pick_move(self, rack):
        """
        Pick the move to make. It will be passed a rack with the current board
        layout, column-major. A 0 indicates no token is there, and 1 or 2
        indicate discs from the two players. Column 0 is on the left, and row 0 
        is on the bottom. It must return an int indicating in which column to 
        drop a disc. The player current just pauses for half a second (for 
        effect), and then chooses a random valid move.
        """
        imaginary_board = [list(row) for row in rack]
        #move, score = miniMax(imaginary_board,self.id,self.difficulty_level,self.id,None)
        move, score = miniMaxAB(imaginary_board,self.id,self.difficulty_level,self.id,None,- math.inf,math.inf)

        #MINIMAXAB_NoMove Start
        # bestScore = -math.inf
        # move = None
        # moveList = getMoves(imaginary_board)
        # for j in moveList:
        #     if imaginary_board[j][-1] == 0: #full col check
        #         row = find_top_spot_open(imaginary_board,j)
        #         imaginary_board[j][row] = self.id
        #         score = miniMaxAB_noMove(imaginary_board,self.id,self.difficulty_level,changeID(self.id),- math.inf,math.inf)
        #         imaginary_board[j][row] = 0
        #         #print(score)
        #         if score > bestScore:
        #             bestScore = score
        #             move = j
        #no move end
        return move
#totals all quartes of a certain rack for a certain player
def scoreQuartets(rack, id):
    total = rightHorizontal(rack,id) + rightDiagonal(rack,id) + leftDiagonal(rack,id) + up(rack,id)
    return total

#gets the score of all the left diagonal quartets
def leftDiagonal(rack,id):
    score = 0
    count = 0
    negCount = 0 #opponent
    otherID = changeID(id)
    for i in range(len(rack) - 3):
        for j in range(len(rack[i]) - 3):
            if rack[i+3][j] == id:
                count += 1
            elif rack[i+3][j] == otherID:
                negCount += 1
            if rack[i][j+3] == id:
                count += 1
            elif rack[i][j+3] == otherID:
                negCount += 1
            if rack[i+1][j+2] == id:
                count += 1
            elif rack[i+1][j+2] == otherID:
                negCount += 1
            if rack[i+2][j+1] == id:
                count += 1
            elif rack[i+2][j+1] == otherID:
                negCount += 1
            score += totalQuartets(count,negCount)
            count = 0
            negCount = 0
    return score

#gets the score of all the right diagonal quartets
def rightDiagonal(rack,id):
    score = 0
    count = 0
    negCount = 0 #opponent
    otherID = changeID(id)

    for i in range(len(rack) - 3):
        for j in range(len(rack[i]) - 3):
            if rack[i][j] == id:
                    count += 1
            elif rack[i][j] == otherID:
                negCount += 1
            if rack[i+3][j+3] == id:
                count += 1
            elif rack[i+3][j+3] == otherID:
                negCount += 1
            if rack[i+1][j+1] == id:
                count += 1
            elif rack[i+1][j+1] == otherID:
                negCount += 1
            if rack[i+2][j+2] == id:
                count += 1
            elif rack[i+2][j+2] == otherID:
                negCount += 1
            score += totalQuartets(count,negCount)
            count = 0
            negCount = 0
    return score



#gets the score of all the right horizontal quartets
def rightHorizontal(rack,id):
    score = 0
    count = 0
    negCount = 0 #opponent
    otherID = changeID(id)
    for i in range(len(rack) - 3):
        for j in range(len(rack[i])):
            if rack[i][j] == id:
                count += 1
            elif rack[i][j] == otherID:
                negCount += 1
            if rack[i+1][j] == id:
                count += 1
            elif rack[i+1][j] == otherID:
                negCount += 1
            if rack[i+2][j] == id:
                count += 1
            elif rack[i+2][j] == otherID:
                negCount += 1
            if rack[i+3][j] == id:
                count += 1
            elif rack[i+3][j] == otherID:
                negCount += 1
            score += totalQuartets(count,negCount)
            count = 0
            negCount = 0
    return score

#Gets the score of all the vertical quartets
def up(rack,id):
    score = 0
    count = 0
    negCount = 0 #opponent
    otherID = changeID(id)
    for i in range(len(rack)):
        for j in range(len(rack[i]) - 3):
            if rack[i][j] == id:
                count += 1
            elif rack[i][j] == otherID:
                negCount += 1
            if rack[i][j+1] == id:
                count += 1
            elif rack[i][j+1] == otherID:
                negCount += 1
            if rack[i][j+2] == id:
                count += 1
            elif rack[i][j+2] == otherID:
                negCount += 1
            if rack[i][j+3] == id:
                count += 1
            elif rack[i][j+3] == otherID:
                negCount += 1
            score += totalQuartets(count,negCount)
            count = 0
            negCount = 0
    return score
    

#scores quartets based on the tile counts 
def totalQuartets(count,negCount):
    if(count > 0 and negCount > 0) or (count == 0 and negCount == 0):
        return 0
    if count == 1:
        return 1
    if negCount == 1:
        return -1
    if count == 2:
        return 10
    if negCount == 2:
        return -10
    if count == 3:
        return 100
    if negCount == 3:
        return -100
    if count >= 4:
        return math.inf
    if negCount >= 4:
        return -math.inf

#getMoves takes in a rack and outputs the possible moves that can be made
def getMoves(rack):
    column = 0
    setOfMoves = [] #list of the coordinates of possible moves
    shape = np.shape(rack)
    for column in range(shape[0]): 
        if rack[column][-1] == 0:
            setOfMoves.append((column))
    return setOfMoves

#switches the id from one player to the other
def changeID(id):
    if id == 1:
        return 2
    else:
        return 1

 #finds the top open spot in a given collumn
def find_top_spot_open(board, column):
    for i in range(len(board[column])):
        if(board[column][i] == 0):
            return i
    raise Exception("Column Full")

 #checks for a tie game
def tie(rack):
    for column in rack:
        if column[-1] == 0:
            return False
    return True

#finds the optimal move for number of plys minimax looks for connect 4
def miniMax(rack,id,depth,turn, prevMove):
    moveList = getMoves(rack)
    #init 
    semiMax = -math.inf
    semiMin = math.inf

    if tie(rack):
        return prevMove, 0 

    if depth <= 0: #bottom of tree get all scores
        bottomScore = scoreQuartets(rack,id)
        return prevMove, bottomScore
    else: 
        whichMove = moveList[0] 

        for j in moveList:
            if rack[j][-1] == 0: #full col check
                row = find_top_spot_open(rack,j)
               
                if turn == id: #bots turn
                    rack[j][row] = turn # place tile on board
                    place, middleScore = miniMax(rack,id,depth-1,changeID(turn), j)
                    if middleScore > semiMax: #better score check
                            semiMax = middleScore
                            whichMove = j
                
                else: #players turn
                    if rack[j][-1] == 0: #full col check
                        rack[j][row] = turn# place tile on board
                        place, middleScore = miniMax(rack,id,depth-1,changeID(turn),j) #recurse down
                        if middleScore < semiMin: #better score check
                                semiMin = middleScore
                                whichMove = j
                rack[j][row] = 0 #undo tile move for next iteration
        if id == turn:

            return whichMove, semiMax
        else:
            return whichMove, semiMin

#finds the optimal move for number of plys minimax looks for connect 4
def miniMaxAB(rack,id,depth,turn, prevMove,alpha,beta): 
    #alpha starts at -inf
    #beta starts at inf
    moveList = getMoves(rack)
    #init 
    semiMax = -math.inf
    semiMin = math.inf

    if tie(rack):
        return prevMove,0

    if depth <= 0: #bottom of tree get all scores
        bottomScore = scoreQuartets(rack,id)
        return prevMove, bottomScore
    else: 
        whichMove = moveList[0] 

        for j in moveList:
            if rack[j][-1] == 0: #full col check
                row = find_top_spot_open(rack,j)
               
                if turn == id: #bots turn
                    rack[j][row] = turn # place tile on board
                    place, middleScore = miniMaxAB(rack,id,depth-1,changeID(turn), j,alpha,beta)
                    if middleScore > semiMax: #better score check
                        semiMax = middleScore
                        if alpha >= beta:
                            rack[j][row] = 0
                            break
                            pass
                        whichMove = j
                    alpha = max(semiMax,alpha)
                    if alpha >= beta:
                        #4print(alpha, " ", beta)
                        rack[j][row] = 0
                        break
                        pass

                
                else: #players turn
                    if rack[j][-1] == 0: #full col check
                        rack[j][row] = turn# place tile on board
                        place, middleScore = miniMaxAB(rack,id,depth-1,changeID(turn),j,alpha,beta) #recurse down
                        if middleScore < semiMin: #better score check
                            semiMin = middleScore
                            if alpha > beta:
                              rack[j][row] = 0
                              break
                              pass
                            whichMove = j
                        beta = min(semiMin,beta)
                        if alpha > beta:
                            #print(alpha, " ", beta)
                            rack[j][row] = 0
                            break
                            pass
                rack[j][row] = 0 #undo tile move for next iteration
        if id == turn:

            return whichMove, semiMax
        else:
            return whichMove, semiMin
