from typing import List
from game.player.player_action import PlayerAction
from game.player.player_action_type import PlayerActionType
from game.player.player import Player
from game.user import User

class HumanPlayer(Player):
    
    def __init__(self, user: User) -> None:
        super().__init__(user)

    def action_command_prompt(self, action: PlayerActionType, call_amount: float):
        if action == PlayerActionType.FOLD:
            return "Fold"
        elif action == PlayerActionType.CHECK:
            return "Check"
        elif action == PlayerActionType.RAISE:
            return "Raise <amount-raise>"
        elif action == PlayerActionType.BET:
            return"Bet <amount-bet>"
        elif action == PlayerActionType.ALL_IN:
            return f"All-in {self.user.money}$"
        elif action == PlayerActionType.CALL:
            return f"Call {call_amount}$"
            
        raise ValueError("Invalid action command!")

    def choose_actions_command_prompt(self, actions: List[PlayerActionType], call_amount: float) -> str:
        sorted_actions = sorted(actions, key=lambda x: x.value)
        action_strings: List[str] = []

        for action in sorted_actions:
            action_str = self.action_command_prompt(action, call_amount)
            action_strings.append(action_str)

        res = f"Choose an action ({' | '.join(action_strings)}): "
        return res

    def choose_action(self, possible_actions: List[PlayerActionType], call_amount: float) -> PlayerActionType:
        while True:
            human_input: str = input(self.choose_actions_command_prompt(possible_actions, call_amount))
            input_args: List[str] = human_input.split()

            command: str = input_args[0]
            amount: float = float(input_args[1]) if len(input_args) > 1 else None

            if command.lower() == PlayerActionType.FOLD.value.lower():
                return PlayerAction(PlayerActionType.FOLD, 0)

            elif command.lower() == PlayerActionType.CHECK.value.lower():
                return PlayerAction(PlayerActionType.CHECK, 0)

            elif command.lower() == PlayerActionType.RAISE.value.lower():
                amount= min(call_amount + amount, self.user.money)

                return PlayerAction(PlayerActionType.RAISE, amount)

            elif command.lower() == PlayerActionType.BET.value.lower():
                amount = min(amount, self.user.money)

                return PlayerAction(PlayerActionType.BET, amount)

            elif command.lower() == PlayerActionType.ALL_IN.value.lower():
                return PlayerAction(PlayerActionType.ALL_IN, self.user.money)

            elif command.lower() == PlayerActionType.CALL.value.lower():
                return PlayerAction(PlayerActionType.CALL, call_amount)

            else:
                print("\nThe given command is invalid, try again!\n")