import itertools
import random
import typing
from game.deck.card import Card
from game.deck.rank import Rank
from game.deck.suit import Suit

class Deck:

    def __init__(self) -> None:
        self.cards: typing.List[Card] = [Card(rank, suit) for suit, rank in list(itertools.product(Suit, Rank))]

    def shuffle_deck(self) -> None:
        random.shuffle(self.cards)