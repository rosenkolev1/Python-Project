import itertools
import random
import typing

from src.game.deck.card import Card
from src.game.deck.rank import Rank
from src.game.deck.suit import Suit


class Deck:

    def __init__(self) -> None:
        self.cards: typing.List[Card] = [Card(rank, suit) for suit, rank in list(itertools.product(Suit, Rank))]

    def shuffle_deck(self) -> None:
        random.shuffle(self.cards)