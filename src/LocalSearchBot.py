from Bot import Bot
from GameAction import GameAction
from GameState import GameState
from numpy import zeros
import sys

INT_MIN = -sys.maxsize - 1

LEN_BOX = 4
MAX_BOX_LINE = 4

ROW = "row"
COL = "col"

class LocalSearchBot(Bot):
    initialState = None
    successorValueRow = zeros((LEN_BOX, LEN_BOX-1), dtype=int)
    successorValueCol = zeros((LEN_BOX-1, LEN_BOX), dtype=int)
    successorValue = [successorValueRow, successorValueCol]

    def get_action(self, state: GameState) -> GameAction:
        self.initialState = state
        return self.localSearch()

    def localSearch(self):
        self.objective_function(LEN_BOX, LEN_BOX-1, 1, 0, 0, self.initialState.row_status)
        self.objective_function(LEN_BOX-1, LEN_BOX, 0, 1, 1, self.initialState.col_status)
        return self.getNeighbor()

    def objective_function(self, x, y, xMin, yMin, a, status):
        for i in range(0, x):
            for j in range(0, y):
                if status[i, j] == 1:
                    self.successorValue[a][i,j] = INT_MIN
                if status[i, j] == 0:
                    if (a == 0 and i == 0) or (a == 1 and j == 0):
                        if abs(self.initialState.board_status[i, j]) <= 1:
                            self.successorValue[a][i,j] = 0
                        elif abs(self.initialState.board_status[i, j]) == 2:
                            self.successorValue[a][i,j] = -1
                        elif abs(self.initialState.board_status[i, j]) == 3:
                            self.successorValue[a][i,j] = 1
                    elif (a == 0 and i == LEN_BOX-1) or (a == 1 and j == LEN_BOX-1):
                        if abs(self.initialState.board_status[i-xMin, j-yMin]) <= 1:
                            self.successorValue[a][i,j] = 0
                        elif abs(self.initialState.board_status[i-xMin, j-yMin]) == 2:
                            self.successorValue[a][i,j] = -1
                        elif abs(self.initialState.board_status[i-xMin, j-yMin]) == 3:
                            self.successorValue[a][i,j] = 1
                    else:
                        if abs(self.initialState.board_status[i, j]) == 3 and abs(self.initialState.board_status[i-xMin, j-yMin]) == 3:
                            self.successorValue[a][i,j] = 3
                        elif abs(self.initialState.board_status[i, j]) == 3 or abs(self.initialState.board_status[i-xMin, j-yMin]) == 3:
                            if abs(self.initialState.board_status[i, j]) == 2 or abs(self.initialState.board_status[i-xMin, j-yMin]) == 2:
                                self.successorValue[a][i,j] = 2
                            else:
                                self.successorValue[a][i,j] = 1
                        elif abs(self.initialState.board_status[i, j]) == 2 and abs(self.initialState.board_status[i-xMin, j-yMin]) == 2:
                            self.successorValue[a][i,j] = -2
                        elif abs(self.initialState.board_status[i, j]) == 2 or abs(self.initialState.board_status[i-xMin, j-yMin]) == 2:
                            self.successorValue[a][i,j] = -1
                        else:
                            self.successorValue[a][i,j] = 0

    def getNeighbor(self):
        max = INT_MIN
        maxAction = None
        for i in range (0, LEN_BOX):
            for j in range (0, LEN_BOX-1):
                if self.successorValue[0][i, j] >= max:
                    max = self.successorValue[0][i, j]
                    maxAction = GameAction(ROW, (j, i))
        for i in range (0, LEN_BOX-1):
            for j in range (0, LEN_BOX):
                if self.successorValue[1][i, j] >= max:
                    max = self.successorValue[1][i, j]
                    maxAction = GameAction(COL, (j, i))
        return maxAction