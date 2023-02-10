from src.game.deck.card import Card
from src.game.deck.deck import Deck
from src.game.deck.preset_deck import PresetDeck
from src.game.deck.preset_empty_deck import PresetEmptyDeck
from src.game.deck.rank import Rank
from src.game.deck.suit import Suit
from src.game.hand.hand import Hand
from src.game.hand.hand_combination import HandCombination 
from src.game.player.player_action_type import PlayerActionType
from src.table.table import Table
from src.user.user import User
from src.game.player.player import Player
from src.game.player.bot_player import BotPlayer
from src.game.player.human_player import HumanPlayer
from src.game.player.player_action import PlayerAction
from src.game.player.choose_action_factory import ChooseActionFactory

preset_deck = PresetDeck(2, 2)

preset_deck.preset_player_cards(0, [Card(Rank.TWO, Suit.CLUBS), Card(Rank.EIGHT, Suit.DIAMONDS)])
preset_deck.preset_player_cards(1, [Card(Rank.THREE, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS)])

preset_deck.preset_flop([Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS)])
preset_deck.preset_turn(Card(Rank.SEVEN, Suit.CLUBS))
preset_deck.preset_river(Card(Rank.ACE, Suit.HEARTS))

user_first = User("roskata", 100)
user_second = User("stefan", 200)

player_first_actions = [
                PlayerAction(PlayerActionType.CALL, 25), #Pre-flop
                PlayerAction(PlayerActionType.CALL, 10),
                PlayerAction(PlayerActionType.BET, 5), #Flop
                PlayerAction(PlayerActionType.CALL, 5),
                PlayerAction(PlayerActionType.CHECK, 0), #Turn
                PlayerAction(PlayerActionType.ALL_IN, 0) #River
            ]

player_first_choose_action = ChooseActionFactory.create_choose_action_predetermined_human_player(player_first_actions)

player_second_actions = [
            PlayerAction(PlayerActionType.RAISE, 10), #Pre-flop
            PlayerAction(PlayerActionType.CHECK, 0), #Flop
            PlayerAction(PlayerActionType.RAISE, 5),
            PlayerAction(PlayerActionType.CHECK, 0), #Turn
            PlayerAction(PlayerActionType.BET, 60), #River
        ]

player_second_choose_action = ChooseActionFactory.create_choose_action_predetermined(player_second_actions)

player_first = HumanPlayer(user_first)
player_second = BotPlayer(user_second, player_second_choose_action)

player_first.predefine_choose_action(player_first_choose_action)

player_first_best_hand = Hand(
    [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.EIGHT, Suit.DIAMONDS)])

player_second_best_hand = Hand(
    [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.SEVEN, Suit.DIAMONDS)])

# game_first = Game(preset_deck, 25, 50)
# game_first.add_player(player_first)
# game_first.add_player(player_second)

# game_first.start_game()

table_one = Table(25, 50)
table_one.add_user(user_first)
table_one.add_user(user_second)

table_one.new_game(preset_deck)
table_one.current_game.add_player(player_first)
table_one.current_game.add_player(player_second)

table_one.start_game()

#Debug
user_first.money = 200
user_second.money = 100

table_one.rotate_button()

table_one.new_game(Deck())

player_first.predefine_choose_action(ChooseActionFactory.create_choose_action_predetermined_human_player(player_second_actions))
player_second.predefine_choose_action(ChooseActionFactory.create_choose_action_predetermined(player_first_actions))

player_first.reset_player()
player_second.reset_player()

table_one.current_game.add_player(player_first)
table_one.current_game.add_player(player_second)

table_one.start_game()

# user_three = User("Third", 100)
# player_three = HumanPlayer(user_three)
# player_three.predefine_choose_action(ChooseActionFactory.create_choose_action_predetermined_human_player(player_first_actions))

# table_two = Table(25, 50)
# table_two.add_user(user_three)
# table_two.add_user(user_second)

# table_two.new_game(Deck())
# table_two.current_game.add_player(player_three)
# table_two.current_game.add_player(player_second)

# player_second.reset_player()

# table_two.start_game()