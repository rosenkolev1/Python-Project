import random
from typing import List

from game.player_action import PlayerAction
from game.player_action_type import PlayerActionType
from game.pot_player import PotPlayer

def mock_choose_action_always_raise(self: PotPlayer, possible_actions: List[PlayerActionType], call_amount: float) -> PlayerActionType:
    action_type: PlayerActionType = PlayerActionType.RAISE

    if action_type == PlayerActionType.CALL:
        return PlayerAction(action_type, call_amount) 

    amount: float = min(call_amount + random.randint(1, 50), self.user.money)

    return PlayerAction(action_type, amount)