from typing import List, Tuple
from src.game.player.choose_action.choose_action_info import ChooseActionInfo
from src.game.player.player_action.player_action import PlayerAction
from src.game.player.player_action.player_action_type import PlayerActionType
from src.game.player.player import Player
from src.game.pot import Pot
from src.game.setting.game_setting import GameSetting
from src.user.user import User
from src.game.user_interface.game_ui import GameUI

class HumanPlayer(Player):
    
    def __init__(self, user: User) -> None:
        super().__init__(user)

        self.original_choose_action = self.choose_action
        self.original_receive_input = self.receive_input

    def receive_input(self, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo) -> str:
        return input(GameUI.choose_actions_command_prompt(self, possible_actions, action_info))

    def get_command_and_amount(self, text_input: str) -> Tuple[str, float]:
        input_args: List[str] = text_input.split()

        command: str = input_args[0]
        
        try:
            amount: float = float(input_args[1]) if len(input_args) > 1 else None
        except ValueError:
            return "", None

        return command, amount

    def __bet_amount_is_below_minimum(self, action_info: ChooseActionInfo, bet_amount: float, min_bet_amount: float):
        return action_info.game.settings.bet_minimum_enabled and bet_amount < min_bet_amount

    def __bet_amount_is_positive(self, amount: float):
        return amount > 0

    def restore_original_choose_action(self):
        self.choose_action = self.original_choose_action
        self.receive_input = self.original_receive_input

    def predefine_choose_action(self, new_choose_action):
        self.choose_action = lambda possible_actions, action_info: new_choose_action(self, possible_actions, action_info)
            
    def choose_action(self, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo) -> PlayerAction:
        while True:
            text_input: str = self.receive_input(possible_actions, action_info)

            command, amount = self.get_command_and_amount(text_input)

            chosen_action: PlayerActionType = GameUI.PLAYER_COMMAND_ACTION_MAP.get(command.lower())

            # minimum_bet_money_required = self.user.money < settings.bet_minimum_amount + call_amount
            minimum_bet_required = action_info.pot.highest_bet_amount

            if chosen_action is None or chosen_action not in possible_actions:
                print(GameUI.INVALID_COMMAND)
                continue

            if chosen_action == PlayerActionType.RAISE:
                if amount is None:
                    print(GameUI.INVALID_COMMAND_MISSING_AMOUNT_ARGUMENT)
                    continue

                if not self.__bet_amount_is_positive(amount):
                    print(GameUI.INVALID_BET_AMOUNT_IS_NEGATIVE_OR_ZERO)
                    continue

                if self.__bet_amount_is_below_minimum(action_info, amount, minimum_bet_required):
                    print(GameUI.invalid_raise_amount_below_minimum(minimum_bet_required))
                    continue

                amount= min(action_info.call_amount + amount, self.user.money)

                return PlayerAction(PlayerActionType.RAISE, amount)

            elif chosen_action == PlayerActionType.BET:
                if amount is None:
                    print(GameUI.INVALID_COMMAND_MISSING_AMOUNT_ARGUMENT)
                    continue

                if not self.__bet_amount_is_positive(amount):
                    print(GameUI.INVALID_BET_AMOUNT_IS_NEGATIVE_OR_ZERO)
                    continue

                if self.__bet_amount_is_below_minimum(action_info, amount, minimum_bet_required):
                    print(GameUI.invalid_bet_amount_below_minimum(minimum_bet_required))
                    continue

                amount = min(amount, self.user.money)

                return PlayerAction(PlayerActionType.BET, amount)

            elif chosen_action == PlayerActionType.ALL_IN:
                return PlayerAction(PlayerActionType.ALL_IN, self.user.money)

            elif chosen_action == PlayerActionType.CALL:
                return PlayerAction(PlayerActionType.CALL, action_info.call_amount)

            else:
                return PlayerAction(chosen_action, 0)