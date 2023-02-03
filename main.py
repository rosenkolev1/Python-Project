from game.game import Game
from game.table import Table
from game.deck.deck import Deck
from game.user import User

deck = Deck()

user_first = User("roskata", 10_000)
user_second = User("stefan", 10_000)

game_first = Game(25, 50)
game_first.add_player(user_first)
game_first.add_player(user_second)

game_first.start_game()