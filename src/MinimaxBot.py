from this import d
from Bot import Bot
from typing import Literal
from GameAction import GameAction
from GameState import GameState
from copy import deepcopy
import time
import numpy as np
import sys

INT_MAX = sys.maxsize
INT_MIN = -sys.maxsize - 1

DOT_SIZE = 4

ROW = "row"
COL = "col"

PLAYER_1 = 1
PLAYER_2 = 2

FULL_BOX_WEIGHT = 40

MIN_DEPTH = 1
MAX_DEPTH = 4

class MinimaxBot(Bot):
    start_time = None
    player_number = None
    next_state = [None for i in range(MIN_DEPTH, MAX_DEPTH+1)]
    is_depth_success = [True for i in range(MIN_DEPTH, MAX_DEPTH+1)]
    current_depth = 0
    
    def get_action(self, state: GameState) -> GameAction:
        self.start_time = time.time()
        self.player_number = PLAYER_1 if state.player1_turn else PLAYER_2

        for i in range(MIN_DEPTH, MAX_DEPTH+1):
            self.current_depth = i
            _ = self.minimax(deepcopy(state), i, INT_MIN, INT_MAX, self.player_number)
        
        print("====================")
        print(self.next_state)
        print(self.is_depth_success)

        for i in range(MAX_DEPTH, MIN_DEPTH-1, -1):
            if self.is_depth_success[i - MIN_DEPTH]:
                return self.create_action(state, self.next_state[i - MIN_DEPTH])

    def minimax(self, state: GameState, depth: int, alpha: int, beta: int, maximizing_player: int):
        if time.time() - self.start_time > 4.9:
            print(self.current_depth)
            for i in range(self.current_depth, MAX_DEPTH+1):
                self.is_depth_success[i - MIN_DEPTH] = False
            return 0
        
        if depth == 0 or self.is_game_over(state):
            return self.count_state_advantage(state, maximizing_player)

        if maximizing_player == self.player_number:
            max_eval = INT_MIN
            
            for child in self.get_child_from_parent(state):
                next_maximizing_player = PLAYER_1 if child.player1_turn else PLAYER_2

                eval = self.minimax(deepcopy(child), depth - 1, alpha, beta, next_maximizing_player)
                
                if depth == self.current_depth and eval > max_eval:
                    self.next_state[self.current_depth - MIN_DEPTH] = deepcopy(child)

                if depth == self.current_depth and eval == max_eval:
                    self.next_state[self.current_depth - MIN_DEPTH] = deepcopy(child) if np.random.randint(50)==25 else self.next_state[self.current_depth - MIN_DEPTH]

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if alpha >= beta:
                    break

            return max_eval
        else:
            min_eval = INT_MAX

            for child in self.get_child_from_parent(state):
                next_maximizing_player = PLAYER_1 if child.player1_turn else PLAYER_2
                
                eval = self.minimax(deepcopy(child), depth - 1, alpha, beta, next_maximizing_player)

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if alpha >= beta:
                    break

            return min_eval
    
    def get_child_from_parent(self, state: GameState) -> list:
        child_list = []
        for y in range(0, DOT_SIZE):
            for x in range(0, DOT_SIZE):
                curr_state = deepcopy(state)
                if x < (DOT_SIZE - 1) and curr_state.row_status[y, x] == 0:
                    new_state = self.update_state(curr_state, ROW, y, x)
                    child_list.append(new_state)
                if y < (DOT_SIZE - 1) and curr_state.col_status[y, x] == 0:
                    new_state = self.update_state(curr_state, COL, y, x)
                    child_list.append(new_state)

        return child_list

    def update_state(self, parent_state: GameState, action_type: Literal["row", "col"], y: int, x: int) -> GameState:
        state = deepcopy(parent_state)

        if(action_type == ROW):
            state.row_status[y, x] = 1

            if y != (DOT_SIZE - 1):
                state.board_status[y, x] = abs(state.board_status[y, x]) + 1
                state.board_status[y, x] *= (-1 if state.player1_turn else 1)

            if y != 0:
                state.board_status[y-1, x] = abs(state.board_status[y-1, x]) + 1
                state.board_status[y-1, x] *= (-1 if state.player1_turn else 1)
        else:
            state.col_status[y, x] = 1

            if x != (DOT_SIZE - 1):
                state.board_status[y, x] = abs(state.board_status[y, x]) + 1
                state.board_status[y, x] *= (-1 if state.player1_turn else 1)
            
            if x != 0:
                state.board_status[y, x-1] = abs(state.board_status[y, x-1]) + 1
                state.board_status[y, x-1] *= (-1 if state.player1_turn else 1)
        
        player_turn = deepcopy(state.player1_turn)
        if not self.is_add_new_box(parent_state, state):
            state = state._replace(player1_turn= not player_turn)

        return state

    def create_action(self, prev_state: GameState, new_state: GameState) -> GameAction:
        for y in range(0, DOT_SIZE):
            for x in range(0, DOT_SIZE):
                if x < (DOT_SIZE - 1) and prev_state.row_status[y, x] != new_state.row_status[y, x]:
                    return GameAction(ROW, (x, y))
                if y < (DOT_SIZE - 1) and prev_state.col_status[y, x] != new_state.col_status[y, x]:
                    return GameAction(COL, (x, y))

    def is_add_new_box(self, prev_state: GameState, new_state: GameState) -> bool:
        if prev_state.player1_turn :
            prev_player_one_box = self.count_box(prev_state, PLAYER_1)
            new_player_one_box = self.count_box(new_state, PLAYER_1)

            result = (prev_player_one_box < new_player_one_box)
        else:
            prev_player_two_box = self.count_box(prev_state, PLAYER_2)
            new_player_two_box = self.count_box(new_state, PLAYER_2)

            result = (prev_player_two_box < new_player_two_box)

        return result

    def count_score_player(self, state: GameState) -> tuple:
        player_one_score = self.count_box(state, PLAYER_1)
        player_two_score = self.count_box(state, PLAYER_2)

        return player_one_score, player_two_score

    def count_box(self, state: GameState, player: int) -> int:
        if player == PLAYER_1:
            player_one_box = np.argwhere(state.board_status == -DOT_SIZE)
            result = len(player_one_box)
        else:
            player_two_box = np.argwhere(state.board_status == DOT_SIZE)
            result = len(player_two_box)

        return result

    def is_game_over(self, state: GameState) -> bool:
        return (state.row_status == 1).all() and (state.col_status == 1).all()

    def count_state_advantage(self, state: GameState, player: int) -> int:
        player_one_score, player_two_score = self.count_score_player(state)
        chain_advantage = self.count_chain_advantage(state)

        if self.player_number == PLAYER_1:
            advantage = FULL_BOX_WEIGHT * (player_one_score - player_two_score)

        if self.player_number == PLAYER_2:
            advantage = FULL_BOX_WEIGHT * (player_two_score - player_one_score)

        if self.player_number == player:
            advantage += chain_advantage
        else:
            advantage -= chain_advantage

        return advantage

    def count_chain_advantage(self, state: GameState) -> int:
        board_status = deepcopy(state.board_status)
        board_visited = np.zeros((DOT_SIZE - 1, DOT_SIZE - 1), dtype=int)

        closed_chain_advantage = []
        for y in range(0, DOT_SIZE - 1):
            for x in range(0, DOT_SIZE - 1):
                if board_visited[y, x] == 0 and (abs(board_status[y, x]) == 3):
                    closed_chain_advantage.append(self.count_chain(state, board_status, board_visited, y, x))
        closed_chain_advantage = [x for x in closed_chain_advantage if x >= 3]

        open_chain_advantage = []
        for y in range(0, DOT_SIZE - 1):
            for x in range(0, DOT_SIZE - 1):
                if board_visited[y, x] == 0 and (abs(board_status[y, x]) == 2):
                    open_chain_advantage.append(self.count_chain(state, board_status, board_visited, y, x))
        open_chain_advantage = [x for x in open_chain_advantage if x >= 3]

        result = 20 * sum(closed_chain_advantage)
        result -= 80 if len(open_chain_advantage) == 2 else 0

        return result
    
    def count_chain(self, state: GameState, board_status: np.ndarray, board_visited: np.ndarray, y: int, x: int) -> int:
        if y < 0 or y >= DOT_SIZE - 1 or x < 0 or x >= DOT_SIZE - 1 or abs(board_status[y, x]) <= 1 or board_visited[y, x] == 1:
            return 0

        board_visited[y, x] = 1
        
        temp_advantage = 1
        neighbor_box = self.generate_unmarked_line_neighbor_box(state, y, x)

        for box in neighbor_box:
            temp_advantage += self.count_chain(state, board_status, board_visited, box[0], box[1])

        return temp_advantage

    def generate_unmarked_line_neighbor_box(self, state: GameState, y: int, x:int) -> list:
        neighbor_box = []

        if y-1 >= 0 and state.row_status[y, x] == 0:
            neighbor_box.append((y-1, x))
        if y+1 <= 2 and state.row_status[y+1, x] == 0:
            neighbor_box.append(((y+1, x)))

        if x-1 >= 0 and state.col_status[y, x] == 0:
            neighbor_box.append((y, x-1))
        if x+1 <= 2 and state.col_status[y, x+1] == 0:
            neighbor_box.append((y, x+1)) 

        return neighbor_box