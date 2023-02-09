from typing import List, Tuple
from game.player.player_action import PlayerAction
from game.player.player_action_type import PlayerActionType
from game.player.player import Player
from game.user import User
from game.user_interface.game_ui import GameUI

class HumanPlayer(Player):
    
    def __init__(self, user: User) -> None:
        super().__init__(user)

    def receive_input(self, possible_actions: List[PlayerActionType], call_amount: float) -> str:
        return input(GameUI.choose_actions_command_prompt(self, possible_actions, call_amount))

    def get_command_and_amount(self, text_input: str) -> Tuple[str, float]:
        input_args: List[str] = text_input.split()

        command: str = input_args[0]
        
        try:
            amount: float = float(input_args[1]) if len(input_args) > 1 else None
        except ValueError:
            return "", None

        return command, amount

    def predefine_choose_action(self, new_choose_action):
        original_choose_action = self.choose_action
        original_receive_input = self.receive_input

        self.choose_action = lambda possible_actions, call_amount: new_choose_action(
            self, possible_actions, call_amount, original_choose_action, original_receive_input)
            
    def choose_action(self, possible_actions: List[PlayerActionType], call_amount: float) -> PlayerActionType:
        while True:
            text_input: str = self.receive_input(possible_actions, call_amount)

            command, amount = self.get_command_and_amount(text_input)

            chosen_action: PlayerActionType = GameUI.PLAYER_COMMAND_ACTION_MAP.get(command.lower())

            if chosen_action is None or chosen_action not in possible_actions:
                print(GameUI.INVALID_COMMAND)
                continue

            if chosen_action == PlayerActionType.RAISE:
                if amount is None:
                    print(GameUI.INVALID_COMMAND_MISSING_AMOUNT_ARGUMENT)
                    continue

                amount= min(call_amount + amount, self.user.money)

                return PlayerAction(PlayerActionType.RAISE, amount)

            elif chosen_action == PlayerActionType.BET:
                if amount is None:
                    print(GameUI.INVALID_COMMAND_MISSING_AMOUNT_ARGUMENT)
                    continue

                amount = min(amount, self.user.money)

                return PlayerAction(PlayerActionType.BET, amount)

            elif chosen_action == PlayerActionType.ALL_IN:
                return PlayerAction(PlayerActionType.ALL_IN, self.user.money)

            elif chosen_action == PlayerActionType.CALL:
                return PlayerAction(PlayerActionType.CALL, call_amount)

            else:
                return PlayerAction(chosen_action, 0)