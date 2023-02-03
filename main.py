from game.deck.card import Card
from game.deck.rank import Rank
from game.deck.suit import Suit
from game.game import Game
from game.hand import Hand
from game.user import User
from game.deck.deck import Deck
from test.mock_deck import MockDeck 

# test_deck = [
#     Card(Rank.TWO, Suit.CLUBS), Card(Rank.EIGHT, Suit.DIAMONDS), #user_second
#     Card(Rank.THREE, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS), #user_first
#     Card(Rank.ACE, Suit.SPADES), #THROWAWAY
#     Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), #Flop
#     Card(Rank.ACE, Suit.SPADES), #THROWAWAY
#     Card(Rank.SEVEN, Suit.CLUBS), 
#     Card(Rank.ACE, Suit.SPADES), #THROWAWAY
#     Card(Rank.ACE, Suit.HEARTS), #River
# ]
# test_deck.reverse()

# mock_deck = MockDeck(test_deck)
    
# user_first = User("roskata", 10_000)
# user_second = User("stefan", 10_000)

# game_first = Game(mock_deck, 25, 50)
# game_first.add_player(user_first)
# game_first.add_player(user_second)

# game_first.start_game()

# assert user_first.money == 0
# assert user_second.money == 20_000

# assert game_first.players[0].best_hand.__repr__() == Hand([
#     Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.SPADES)
#     ]).__repr__()