import random
from typing import List
from game.deck.card import Card
from game.hand import Hand
from game.player_action import PlayerAction
from game.player_action_type import PlayerActionType

from game.user import User

class PotPlayer:

    def __init__(self, user: User, stake:float = 0) -> None:
        self.user = user
        self.stake = stake
        self.has_folded = False
        self.has_played_turn = False
        self.cards: List[Card] = []
        self.best_hand: Card = None 

    @property
    def is_all_in(self) -> bool:
        return self.user.money == 0

    def choose_action(self, possible_actions: List[PlayerActionType], call_amount: float) -> PlayerAction:
        #Choose randomly
        # action_type: PlayerActionType = possible_actions[random.randint(0, len(possible_actions) - 1)]
        # action_type: PlayerActionType = PlayerActionType.FOLD
        action_type: PlayerActionType = PlayerActionType.RAISE

        if action_type == PlayerActionType.CALL:
            return PlayerAction(action_type, call_amount) 

        amount: float = min(call_amount + random.randint(1, 50), self.user.money)

        return PlayerAction(action_type, amount)

        