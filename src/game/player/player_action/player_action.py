from src.game.player.player_action.player_action_type import PlayerActionType


class PlayerAction:

    def __init__(self, action_type: PlayerActionType, amount: float) -> None:
        self.type = action_type
        self.amount = amount