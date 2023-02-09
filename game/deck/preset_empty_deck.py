from typing import List

from game.deck.card import Card
from game.deck.deck import Deck

class PresetEmptyDeck(Deck):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.preset: List[Card] = [None]*52        
        
    def shuffle_deck(self) -> None:
        self.cards = self.preset
