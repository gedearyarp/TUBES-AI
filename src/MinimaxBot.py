from Bot import Bot
from GameAction import GameAction
from GameState import GameState

class MinimaxBot(Bot):
    def get_action(self, state: GameState) -> GameAction:
        """
        Returns action based on state.
        """
        raise NotImplementedError()
