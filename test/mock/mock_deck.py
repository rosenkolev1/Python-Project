from typing import List
from game.deck.card import Card
from game.deck.deck import Deck
from game.deck.rank import Rank
from game.deck.suit import Suit

class MockDeck(Deck):
    
    def __init__(self, players_count: int, player_cards_count: int) -> None:
        super().__init__()
        
        self.players_count = players_count
        self.player_cards_count = player_cards_count
        self.preset: List[Card] = [None]*players_count*player_cards_count        

    def preset_player_cards(self, player_turn: int, cards: List[Card]):
        for i in range(len(cards)):
            self.preset[player_turn + i * self.players_count] = cards[i]  
    
    def preset_flop(self, cards: List[Card]):
        self.preset.append(None)
        
        for card in cards:
            self.preset.append(card)
            
    def preset_turn_or_river(self, card: Card):
        self.preset.append(None)
              
        self.preset.append(card)
              
    def shuffle_deck(self) -> None:
        self.preset.reverse()
        self.cards = self.preset