from src.game.deck.rank import Rank
from src.game.deck.suit import Suit


class Card:

    def __init__(self, rank: Rank, suit: Suit) -> None:
        self.suit = suit
        self.rank = rank

    def __repr__(self) -> str:
        return self.suit.value + str(self.rank.name)