import random
from typing import List
from game.player_action import PlayerAction
from game.player_action_type import PlayerActionType 
from game.deck.card import Card
from game.deck.rank import Rank
from game.deck.suit import Suit
from game.game import Game
from game.hand import Hand
from game.pot_player import PotPlayer
from game.user import User
from game.deck.deck import Deck
from test.mock.mock_deck import MockDeck
from test.mock.mock_empty_deck import MockEmptyDeck
from test.mock.mock_player import MockPlayer 

# mock_deck = MockDeck(2, 2)
mock_deck = MockEmptyDeck()

# mock_deck.preset_player_cards(0, [Card(Rank.TWO, Suit.CLUBS), Card(Rank.EIGHT, Suit.DIAMONDS)])
# mock_deck.preset_player_cards(1, [Card(Rank.THREE, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS)])

# mock_deck.preset_flop([Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS)])
# mock_deck.preset_turn_or_river(Card(Rank.SEVEN, Suit.CLUBS))
# mock_deck.preset_turn_or_river(Card(Rank.ACE, Suit.HEARTS))
    
user_first = User("roskata", 100)
user_second = User("stefan", 200)

def mock_choose_action_first(self: PotPlayer, possible_actions: List[PlayerActionType], call_amount: float) -> PlayerActionType:
        action_type: PlayerActionType = PlayerActionType.RAISE

        if action_type == PlayerActionType.CALL:
            return PlayerAction(action_type, call_amount) 

        amount: float = min(call_amount + random.randint(1, 50), self.user.money)

        return PlayerAction(action_type, amount)

player_first = MockPlayer(user_first, mock_choose_action_first)
player_second = MockPlayer(user_second, mock_choose_action_first)

player_first.best_hand = Hand(
    [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.EIGHT, Suit.DIAMONDS)])

player_second.best_hand = Hand(
    [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.SEVEN, Suit.DIAMONDS)])

game_first = Game(mock_deck, 25, 50)
game_first.add_player(player_first)
game_first.add_player(player_second)

game_first.start_game()

assert user_first.money == 0
assert user_second.money == 300

# assert game_first.players[0].best_hand.__repr__() == .__repr__()

# assert game_first.players[1].best_hand.__repr__() == Hand([
#     Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.SEVEN, Suit.DIAMONDS)
#     ]).__repr__()