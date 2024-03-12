#-------------------------------------------------------------------------------
# Name:        Game_Searches
# Purpose:     Module implementing game search algorithms: zero sum, non-zero sum, cooperative.
#
# Author:      Nadav Erell
#
# Created:     23/12/2012
#-------------------------------------------------------------------------------

import sys


# Return MIN value
def MiniMaxAlphaBeta(problem, initialState):
    action_State_List = problem.Successors(initialState)
    if len(action_State_List) == 0:
        return None
    valuesList = [(MaxValue(problem, s, -sys.maxsize, sys.maxsize), action) for (action, s) in action_State_List]
#    print(valuesList)
#    for (v,a) in valuesList:
#        print("Top:", v, a) 
    (value, action) = valuesList[0]
    for (v, a) in valuesList:
        if v < value:
            value = v
            action = a
    return action

# Return MAX value
def MaxiMinAlphaBeta(problem, initialState):
    action_State_List = problem.Successors(initialState)
    if len(action_State_List) == 0:
        return None
    valuesList = [(MinValue(problem, s, -sys.maxsize, sys.maxsize), action) for (action, s) in action_State_List]
#    print(valuesList)
#    for (v,a) in valuesList:
#        print("Top:", v, a) 
    (value, action) = valuesList[0]
    for (v, a) in valuesList:
        if v > value:
            value = v
            action = a
    return action

def MaxValue(problem, state, alpha, beta):
    if problem.TerminalTest(state):
        return problem.Utility(state)
    if problem.CutoffTest(state):
        return problem.Eval(state)
    v = None
    for (a,s) in problem.Successors(state):
        val = MinValue(problem, s, alpha, beta)
        if val == None:
            return problem.Eval(state)
        if v == None:
            v = val 
        elif v < val:
            v = val
        if v >= beta:
            return v
        alpha = max(alpha, v)
    if v==None:
        return problem.Eval(state)
    return v

def MinValue(problem, state, alpha, beta):
    if problem.TerminalTest(state):
        return problem.Utility(state)
    if problem.CutoffTest(state):
        return problem.Eval(state)
    v = None
    for (a,s) in problem.Successors(state):
        val = MaxValue(problem, s, alpha, beta)
        if val == None:
            return problem.Eval(state)
        if v == None:
            v = val 
        elif v > val:
            v = val
        if v <= alpha:
            return v
        beta = min(beta, v)
    if v==None:
        return problem.Eval(state)
    return v



def MiniMinAlphaBeta(problem, initialState):
    action_State_List = problem.Successors(initialState)
    valuesList = [(MiniMinValue(problem, s, -sys.maxsize, sys.maxsize), action) for (action, s) in action_State_List]
    #for (v,a) in valuesList:
        #print("Top:", v, a) 
    (value, action) = valuesList[0]
    for (v, a) in valuesList:
        if v < value:
            value = v
            action = a
    return action

def MiniMinValue(problem, state, alpha, beta):
    if problem.TerminalTest(state):
        return problem.Utility(state)
    if problem.CutoffTest(state):
        return problem.Eval(state)
    v = None
    for (a,s) in problem.Successors(state):
        val = MiniMinValue(problem, s, alpha, beta)
        if v == None:
            v = val 
        elif v > val:
            v = val
        #if v <= alpha:
        #    return v
        beta = min(beta, v)
    return v




class GameTreeProblem():
    
    def __init__(self, initialState, heuristic):
        self.initialState = initialState
        self.h = heuristic

    def TerminalTest(self, state):
        raise NotImplementedError

    def CutoffTest(self, state):
        raise NotImplementedError

    def Utility(self, state):
        raise NotImplementedError 

    def Eval(self, state):
        raise NotImplementedError        

    def Successors(self, state):
        raise NotImplementedError
