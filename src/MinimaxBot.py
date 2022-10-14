from this import d
from Bot import Bot
from typing import Literal
from GameAction import GameAction
from GameState import GameState
from copy import deepcopy
import numpy as np
import sys

INT_MAX = sys.maxsize
INT_MIN = -sys.maxsize - 1

LEN_BOX = 4
MAX_BOX_LINE = 4

ROW = "row"
COL = "col"

PLAYER_1 = 1
PLAYER_2 = 2

DEPTH = 3

class MinimaxBot(Bot):
    def get_action(self, state: GameState) -> GameAction:
        self.player_number = 1 if state.player1_turn else 2

        next_state = self.minimax(None, deepcopy(state), DEPTH, INT_MIN, INT_MAX, self.player_number)[0]
        return self.create_action(state, next_state)

    def minimax(self, result_state: GameState, state: GameState, depth: int, alpha: int, beta: int, maximizing_player: int):
        if depth == 0 or self.is_game_over(state):
            return deepcopy(result_state), self.count_state_advantage(state)

        if maximizing_player == PLAYER_1:
            max_eval = INT_MIN
            
            for child in self.get_child_from_parent(state):
                current_result_state = deepcopy(child) if result_state == None else deepcopy(result_state)
                next_maximizing_player = PLAYER_1 if self.is_add_new_box(state, child) else PLAYER_2
                
                next_state, eval = self.minimax(current_result_state, child, depth - 1, alpha, beta, next_maximizing_player)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if alpha >= beta:
                    break

            return next_state, max_eval
        else:
            min_eval = INT_MAX

            for child in self.get_child_from_parent(state):
                current_result_state = deepcopy(child) if result_state == None else deepcopy(result_state)
                next_maximizing_player = PLAYER_2 if self.is_add_new_box(state, child) else PLAYER_1
                
                next_state, eval = self.minimax(current_result_state, child, depth - 1, alpha, beta, next_maximizing_player)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if alpha >= beta:
                    break

            return next_state, min_eval

    def count_state_advantage(self, state: GameState) -> int:
        player_one_score, player_two_score = self.count_score_player(state)

        advantage = player_one_score - player_two_score
        if self.player_number == PLAYER_2:
            advantage = player_two_score - player_one_score

        return advantage
    
    def get_child_from_parent(self, state: GameState) -> list:
        child_list = []
        for y in range(0, LEN_BOX):
            for x in range(0, LEN_BOX):
                curr_state = deepcopy(state)
                if x < 3 and curr_state.row_status[y, x] == 0:
                    new_state = self.update_state(curr_state, ROW, y, x)
                    child_list.append(new_state)
                if y < 3 and curr_state.col_status[y, x] == 0:
                    new_state = self.update_state(curr_state, COL, y, x)
                    child_list.append(new_state)

        return child_list

    def update_state(self, parent_state: GameState, action_type: Literal["row", "col"], y: int, x: int) -> GameState:
        state = deepcopy(parent_state)

        if(action_type == ROW):
            state.row_status[y, x] = 1

            if y != 3:
                state.board_status[y, x] = abs(state.board_status[y, x]) + 1
                state.board_status[y, x] *= (-1 if state.player1_turn else 1)

            if y != 0:
                state.board_status[y-1, x] = abs(state.board_status[y-1, x]) + 1
                state.board_status[y-1, x] *= (-1 if state.player1_turn else 1)
        else:
            state.col_status[y, x] = 1

            if x != 3:
                state.board_status[y, x] = abs(state.board_status[y, x]) + 1
                state.board_status[y, x] *= (-1 if state.player1_turn else 1)
            
            if x != 0:
                state.board_status[y, x-1] = abs(state.board_status[y, x-1]) + 1
                state.board_status[y, x-1] *= (-1 if state.player1_turn else 1)

        return state

    def create_action(self, prev_state: GameState, new_state: GameState) -> GameAction:
        for y in range(0, LEN_BOX):
            for x in range(0, LEN_BOX):
                if x < 3 and prev_state.row_status[y, x] != new_state.row_status[y, x]:
                    return GameAction(ROW, (x, y))
                if y < 3 and prev_state.col_status[y, x] != new_state.col_status[y, x]:
                    return GameAction(COL, (x, y))

    def is_add_new_box(self, prev_state: GameState, new_state: GameState) -> bool:
        result = False

        if prev_state.player1_turn :
            parent_player_one_box = self.count_box(prev_state, PLAYER_1)
            new_player_one_box = self.count_box(new_state, PLAYER_1)

            result = parent_player_one_box > new_player_one_box
        else:
            prev_state = self.count_box(prev_state, PLAYER_2)
            new_player_two_box = self.count_box(new_state, PLAYER_2)

            result = prev_state > new_player_two_box

        return result

    def count_score_player(self, state: GameState):
        player_one_score = self.count_box(state, PLAYER_1)
        player_two_score = self.count_box(state, PLAYER_2)

        return player_one_score, player_two_score

    def count_box(self, state: GameState, player_number: int) -> int:
        result = 0
        
        if player_number == PLAYER_1:
            player_one_box = np.argwhere(state.board_status == MAX_BOX_LINE)
            result = len(player_one_box)
        else:
            player_two_box = np.argwhere(state.board_status == -MAX_BOX_LINE)
            result = len(player_two_box)

        return result

    def is_game_over(self, state: GameState):
        return (state.row_status == 1).all() and (state.col_status == 1).all()
