from this import d
from Bot import Bot
from typing import Literal
from GameAction import GameAction
from GameState import GameState
import numpy as np

class MinimaxBot(Bot):
    def get_action(self, state: GameState) -> GameAction:
        """
        Returns action based on state.
        """
        raise NotImplementedError()
    
    def minimax(self, state: GameState, depth: int, alpha: int, beta: int, maximizingPlayer: bool):
        """
            Fungsi yang berisi algoritma minimax dan juga alfa beta pruning 
            dengan memanfaatkan fungsi get_child_for_parent untuk mencari 
            jalan yang mungkin dan juga count_state_advantage untuk mencari 
            nilai tiap jalan yang didapatkan.
        """
        return 0

    def count_state_advantage(self, state: GameState) -> int:
        """
            Fungsi yang menghitung nilai keuntungan dari suatu state 
            pada parameter fungsi ini. (objective function)
        """
        player_one_score, player_two_score = self.count_score_player(state)

        advantage = player_one_score - player_two_score
        return advantage
    
    def get_child_from_parent(self, state: GameState):
        """
            Fungsi yang mencari semua kemungkinan jalan dari suatu state 
            yang menjadi parameter fungsi dan mengembalikannya ke dalam 
            array of GameState
        """
        return 0
    
    def is_game_over(self, state: GameState):
        """
            Fungsi yang akan mengembalikan true jika semua garis sudah 
            terisi (tidak bisa jalan lagi)
        """
        return (state.row_status == 1).all() and (state.col_status == 1).all()
    
    def is_add_new_box(self, new_state: GameState, parent_state: GameState) -> bool:
        """
            Fungsi yang akan mengembalikan true jika new_state menambahkan 
            kotak baru dari parent_state (state sebelumnya)
        """
        return 0

    def update_state(self, state: GameState, action_type: Literal["row", "col"], x: int, y: int) -> GameState:
        """
            Fungsi yang mengembalikan GameState baru dari GameState lama
        """
        if(action_type == "row"):
            state.row_status[y, x] = 1

            if y != 3:
                state.board_status[y, x] += 1
                state.board_status[y, x] *= (-1 if state.player1_turn else 1)

            if y-1 != -1:
                state.board_status[y-1, x] += 1
                state.board_status[y-1, x] *= (-1 if state.player1_turn else 1)
        else:
            state.col_status[y, x] = 1

            if x != 3:
                state.board_status[y, x] += 1
                state.board_status[y, x] *= (-1 if state.player1_turn else 1)
            
            if x-1 != -1:
                state.board_status[y, x-1] += 1
                state.board_status[y, x-1] *= (-1 if state.player1_turn else 1)
        
        return state

    def count_score_player(self, state: GameState):
        """
            Fungsi yang akan mengembalikan jumlah score player 1 dan player 2.
        """
        player_one_box = np.argwhere(state.board_status == 4)
        player_two_box = np.argwhere(state.board_status == -4)

        player_one_score = len(player_one_box)
        player_two_score = len(player_two_box)

        return player_one_score, player_two_score
    
    def create_action(self, prev_state: GameState, goal_state: GameState) -> GameAction:
        """
            Fungsi yang mengembalikan GameAction dari 2 GameState.
        """
        LEN_MAX = 4
        for i in range(0, LEN_MAX):
            for j in range(0, LEN_MAX):
                if j < 3 and prev_state.row_status[i, j] != goal_state.row_status[i, j]:
                    return GameAction("row", (i, j))
                if i < 3 and prev_state.col_status[i, j] != goal_state.col_status[i, j]:
                    return GameAction("col", (i, j))
