from typing import List
from src.game.player.choose_action_info import ChooseActionInfo
from src.game.player.player_action import PlayerAction
from src.game.player.player_action_type import PlayerActionType
from src.game.player.player import Player
from src.game.pot import Pot
from src.game.setting.game_setting import GameSetting
from src.user.user import User

class BotPlayer(Player):
    
    def __init__(self, user: User, choose_action = None) -> None:
        super().__init__(user)
        self.choose_action_preset = choose_action    

    def __bet_amount_is_below_minimum(self, action_info: ChooseActionInfo, bet_amount: float, min_bet_amount: float):
        return action_info.game.settings.bet_minimum_enabled and bet_amount < min_bet_amount

    def __bet_amount_is_positive(self, amount: float):
        return amount > 0

    def predefine_choose_action(self, new_choose_action):
        self.choose_action_preset = new_choose_action

    def choose_action(self, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo) -> PlayerAction:
        chosen_action: PlayerAction = self.choose_action_preset(self, possible_actions, action_info)

        if chosen_action.type in [PlayerActionType.BET, PlayerActionType.RAISE]:
            
            if not self.__bet_amount_is_positive(chosen_action.amount):
                raise ValueError(f"Invalid bet or raise amount! The amount must be positive!")
                
            elif self.__bet_amount_is_below_minimum(action_info, chosen_action.amount, action_info.pot.highest_bet_amount):
                raise ValueError(f"Invalid bet or raise amount! The amount must be at least {action_info.pot.highest_bet_amount}")

        return chosen_action
            