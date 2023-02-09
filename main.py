import random

from typing import List
from game.deck.card import Card

from game.deck.preset_deck import PresetDeck
from game.deck.rank import Rank
from game.deck.suit import Suit
from game.game import Game
from game.hand.hand import Hand
from game.player.bot_player import BotPlayer
from game.player.choose_action_factory import ChooseActionFactory
from game.player.human_player import HumanPlayer
from game.player.player_action import PlayerAction
from game.player.player_action_type import PlayerActionType
from game.user import User

preset_deck = PresetDeck(2, 2)

preset_deck.preset_player_cards(0, [Card(Rank.TWO, Suit.CLUBS), Card(Rank.EIGHT, Suit.DIAMONDS)])
preset_deck.preset_player_cards(1, [Card(Rank.THREE, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS)])

preset_deck.preset_flop([Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS)])
preset_deck.preset_turn(Card(Rank.SEVEN, Suit.CLUBS))
preset_deck.preset_river(Card(Rank.ACE, Suit.HEARTS))

user_first = User("roskata", 100)
user_second = User("stefan", 200)

player_first_actions = ChooseActionFactory.create_choose_action_predetermined_human_player(
            [
                PlayerAction(PlayerActionType.CALL, 25), #Pre-flop
                PlayerAction(PlayerActionType.CALL, 10),
                PlayerAction(PlayerActionType.BET, 5), #Flop
                PlayerAction(PlayerActionType.CALL, 5),
                PlayerAction(PlayerActionType.CHECK, 0), #Turn
                # PlayerAction(PlayerActionType.ALL_IN, 0) #River
            ]
        )
    
player_second_actions = ChooseActionFactory.create_choose_action_predetermined(
        [
            PlayerAction(PlayerActionType.RAISE, 10), #Pre-flop
            PlayerAction(PlayerActionType.CHECK, 0), #Flop
            PlayerAction(PlayerActionType.RAISE, 5),
            PlayerAction(PlayerActionType.CHECK, 0), #Turn
            PlayerAction(PlayerActionType.RAISE, 60), #River
        ], 
    )

player_first = HumanPlayer(user_first)
player_second = BotPlayer(user_second, player_second_actions)

player_first.predefine_choose_action(player_first_actions)

player_first_best_hand = Hand(
    [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.EIGHT, Suit.DIAMONDS)])

player_second_best_hand = Hand(
    [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.SEVEN, Suit.DIAMONDS)])

game_first = Game(preset_deck, 25, 50)
game_first.add_player(player_first)
game_first.add_player(player_second)

game_first.start_game()