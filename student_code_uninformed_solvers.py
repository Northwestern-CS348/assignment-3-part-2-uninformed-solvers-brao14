from solver import *
from collections import deque

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        if self.currentState.state == self.victoryCondition:
            return True

        self.visited[self.currentState] = True

        moves = self.gm.getMovables()
        cstate = self.currentState

        if moves:
            for move in moves:
                self.gm.makeMove(move)
                nstate = GameState(self.gm.getGameState(), cstate.depth + 1, move)
                if nstate not in self.visited:  
                    nstate.parent = cstate
                    cstate.children.append(nstate)
                self.gm.reverseMove(move)

            while cstate.nextChildToVisit < len(cstate.children):
                nstate = cstate.children[cstate.nextChildToVisit]
                if nstate not in self.visited:  
                    cstate.nextChildToVisit + cstate.nextChildToVisit + 1
                    self.currentState = nstate
                    self.gm.makeMove(nstate.requiredMovable)
                    self.visited[nstate] = True
                    break
                else:   
                    cstate.nextChildToVisit + cstate.nextChildToVisit + 1
        else:
            return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.states = deque()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.
        Returns:
            True if the desired solution state is reached, False otherwise
        """
        self.visited[self.currentState] = True
        if self.currentState.state == self.victoryCondition:
            return True

        moves = self.gm.getMovables()
        cstate = self.currentState
        if not cstate.children:  
            for move in moves:
                self.gm.makeMove(move)
                nstate = GameState(self.gm.getGameState(), cstate.depth + 1, move)
                if nstate not in self.visited:
                    nstate.parent = cstate
                    self.visited[nstate] = False
                    cstate.children.append(nstate)
                self.gm.reverseMove(move)

        for child in cstate.children:
            if not self.visited[child] and child not in self.states:
                self.states.append(child)  
        
        nstate = self.states.popleft()
        path = deque()
        queue_state = nstate

        while queue_state.parent is not None:
            path.append(queue_state.requiredMovable)    
            print(path)
            queue_state = queue_state.parent
        
        while self.currentState.parent is not None:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        while path:
            self.gm.makeMove(path.pop())

        self.currentState = nstate

        if self.currentState.state == self.victoryCondition:
            return True
        else:
            return False

