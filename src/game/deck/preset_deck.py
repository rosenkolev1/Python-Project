from typing import List
from src.game.deck.card import Card
from src.game.deck.deck import Deck

class PresetDeck(Deck):
    
    def __init__(self, players_count: int, player_cards_count:int = 2) -> None:
        super().__init__()
        
        self.players_count = players_count
        self.player_cards_count = player_cards_count
        self.preset: List[Card] = [None]*(players_count * player_cards_count + 8)
        self.flop_start_index = players_count * player_cards_count + 1
        self.turn_start_index = self.flop_start_index + 4   
        self.river_start_index = self.turn_start_index + 2

    def preset_player_cards(self, player_turn: int, cards: List[Card]):
        for i in range(len(cards)):
            self.preset[player_turn + i * self.players_count] = cards[i]  
    
    def preset_community(self, cards: List[Card]):
        flop_cards: List[Card] = [cards[i] for i in range(0, len(cards)) if i < 3]
        turn_card: Card = cards[3]
        river_card: Card = cards[4]

        self.preset_flop(flop_cards)
        self.preset_turn(turn_card)
        self.preset_river(river_card)

    def preset_flop(self, cards: List[Card]):
        for i in range(len(cards)):
            self.preset[self.flop_start_index + i] = cards[i]

    def preset_turn(self, card: Card):
        self.preset[self.turn_start_index] = card  

    def preset_river(self, card: Card):
        self.preset[self.river_start_index] = card    
              
    def shuffle_deck(self) -> None:
        self.preset.reverse()
        self.cards = self.preset