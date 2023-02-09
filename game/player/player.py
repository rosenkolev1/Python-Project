from abc import ABC, abstractmethod
from typing import List
from game.deck.card import Card
from game.player.player_action import PlayerAction
from game.player.player_action_type import PlayerActionType

from game.user import User

class Player(ABC):

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

    def reset_player(self):
        self.stake = 0
        self.has_folded = False
        self.has_played_turn = False
        self.cards: List[Card] = []
        self.best_hand: Card = None 

    @abstractmethod
    def choose_action(self, possible_actions: List[PlayerActionType], call_amount: float) -> PlayerAction:
        pass

        