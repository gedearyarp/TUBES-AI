from Bot import Bot
from GameAction import GameAction
from GameState import GameState

class LocalSearchBot(Bot):
    def get_action(self, state: GameState) -> GameAction:
        raise NotImplementedError()

    def minimax(self, state: GameState, depth: int, alpha: int, beta: int, maximizingPlayer: bool):
        """
            Fungsi yang berisi algoritma minimax dan juga alfa beta pruning 
            dengan memanfaatkan fungsi get_child_for_parent untuk mencari 
            jalan yang mungkin dan juga count_state_advantage untuk mencari 
            nilai tiap jalan yang didapatkan.
        """
        return 0

    def count_state_advantage(state: GameState) -> int:
        """
            Fungsi yang menghitung nilai keuntungan dari suatu state 
            pada parameter fungsi ini. (objective function)
        """
        return 0
    
    def get_child_from_parent(state: GameState):
        """
            Fungsi yang mencari semua kemungkinan jalan dari suatu state 
            yang menjadi parameter fungsi dan mengembalikannya ke dalam 
            array of GameState
        """
        return 0
    
    def is_game_over(state: GameState):
        """
            Fungsi yang akan mengembalikan true jika semua garis sudah 
            terisi (tidak bisa jalan lagi)
        """
        return 0
    
    def is_add_new_box(new_state: GameState, parent_state: GameState) -> bool:
        """
            Fungsi yang akan mengembalikan true jika new_state menambahkan 
            kotak baru dari parent_state (state sebelumnya)
        """
        return 0
    
    def count_score_player(state: GameState):
        """
            Fungsi yang akan mengembalikan jumlah score player 1 dan player 2.
        """
        return 0
    
    def create_action(prev_state: GameState, goal_state: GameState) -> GameAction:
        """
            Fungsi yang mengembalikan GameAction dari 2 GameState.
        """
        return 0