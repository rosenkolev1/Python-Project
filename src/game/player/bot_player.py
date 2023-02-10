from typing import List
from src.game.player.player_action_type import PlayerActionType
from src.game.player.player import Player
from src.user.user import User

class BotPlayer(Player):
    
    def __init__(self, user: User, choose_action = None) -> None:
        super().__init__(user)
        self.choose_action_preset = choose_action    

    def predefine_choose_action(self, new_choose_action):
        self.choose_action_preset = new_choose_action

    def choose_action(self, possible_actions: List[PlayerActionType], call_amount: float) -> PlayerActionType:
        return self.choose_action_preset(self, possible_actions, call_amount)