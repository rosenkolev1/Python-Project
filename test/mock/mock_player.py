from typing import List
from game.player_action_type import PlayerActionType
from game.pot_player import PotPlayer
from game.user import User

class MockPlayer(PotPlayer):
    
    def __init__(self, user: User, mock_choose_action, stake:float = 0) -> None:
        super().__init__(user)
        self.mock_choose_action = mock_choose_action    

    def choose_action(self, possible_actions: List[PlayerActionType], call_amount: float) -> PlayerActionType:
        return self.mock_choose_action(self, possible_actions, call_amount)