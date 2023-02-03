from typing import List
from game.deck.card import Card
from game.deck.deck import Deck
from game.deck.rank import Rank
from game.deck.suit import Suit

class MockDeck(Deck):
    
    def __init__(self, preset: List[Card]) -> None:
        super()
        
        self.preset: List[Card] = preset        

    
    def shuffle_deck(self) -> None:
        self.cards = self.preset