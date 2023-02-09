from typing import List
from game.player.player_action_type import PlayerActionType
from game.player.player import Player
from game.user import User

class BotPlayer(Player):
    
    def __init__(self, user: User, choose_action) -> None:
        super().__init__(user)
        self.choose_action_preset = choose_action    

    def choose_action(self, possible_actions: List[PlayerActionType], call_amount: float) -> PlayerActionType:
        return self.choose_action_preset(self, possible_actions, call_amount)