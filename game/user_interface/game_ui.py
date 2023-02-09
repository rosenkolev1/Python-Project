
from typing import List
from game.player.player import Player
from game.player.player_action_type import PlayerActionType


class GameUI:
    
    PLAYER_COMMAND_ACTION_MAP = {
        "fold": PlayerActionType.FOLD,
        "check": PlayerActionType.CHECK,
        "call": PlayerActionType.CALL,
        "bet": PlayerActionType.BET,
        "raise": PlayerActionType.RAISE,
        "all-in": PlayerActionType.ALL_IN,
    }

    INVALID_COMMAND: str = "\nThe given command is invalid, try again!\n"

    INVALID_COMMAND_MISSING_AMOUNT_ARGUMENT = "\nThe given command is invalid because you have not specified an amount!\n"

    @staticmethod
    def action_command_prompt(player: Player, action: PlayerActionType, call_amount: float):
        if action == PlayerActionType.FOLD:
            return "Fold"
        elif action == PlayerActionType.CHECK:
            return "Check"
        elif action == PlayerActionType.RAISE:
            return "Raise <amount-raise>"
        elif action == PlayerActionType.BET:
            return"Bet <amount-bet>"
        elif action == PlayerActionType.ALL_IN:
            return f"All-in {player.user.money}$"
        elif action == PlayerActionType.CALL:
            return f"Call {call_amount}$"
            
        raise ValueError("Invalid action command!")

    @staticmethod
    def choose_actions_command_prompt(player: Player, actions: List[PlayerActionType], call_amount: float) -> str:
        sorted_actions = sorted(actions, key=lambda x: x.value)
        action_strings: List[str] = []

        for action in sorted_actions:
            action_str = GameUI.action_command_prompt(player, action, call_amount)
            action_strings.append(action_str)

        res = f"Choose an action ({' | '.join(action_strings)}): "
        return res