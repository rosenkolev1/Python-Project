import pytest
from src.game.deck.card import Card
from src.game.deck.deck import Deck
from src.game.deck.preset_deck import PresetDeck
from src.game.deck.preset_empty_deck import PresetEmptyDeck
from src.game.deck.rank import Rank
from src.game.deck.suit import Suit
from src.game.game import Game
from src.game.hand.hand import Hand
from src.game.hand.hand_combination import HandCombination 
from src.game.player.player_action.player_action_type import PlayerActionType
from src.game.setting.game_setting import GameSetting
from src.game.setting.hand_visibility_setting import HandVisibilitySetting
from src.table.table import Table
from src.user.user import User
from src.game.player.player import Player
from src.game.player.bot_player import BotPlayer
from src.game.player.human_player import HumanPlayer
from src.game.player.player_action.player_action import PlayerAction
from src.game.player.choose_action.choose_action_factory import ChooseActionFactory
from test.game.helper.settings_functions import default_game_settings

def test_6_human_players_4_pots_different_winners_with_folding_players():
    user_1 = User("Roskata", 100)
    user_2 = User("Stefan", 150)
    user_3 = User("Kris", 200)
    user_4 = User("Miro", 250)
    user_5 = User("Ge6a", 1000)
    user_6 = User("Pe6o", 1000)

    player_1 = HumanPlayer(user_1)
    player_2 = HumanPlayer(user_2)
    player_3 = HumanPlayer(user_3)
    player_4 = HumanPlayer(user_4)
    player_5 = HumanPlayer(user_5)
    player_6 = HumanPlayer(user_6)

    player_1_preset_actions = ChooseActionFactory.create_choose_action_predetermined_human_player(
        [
            PlayerAction(PlayerActionType.ALL_IN, 100) #Pre-flop 4
        ]
    )

    player_2_preset_actions = ChooseActionFactory.create_choose_action_predetermined_human_player(
        [
            PlayerAction(PlayerActionType.CALL, 75), #Pre-flop 5
            PlayerAction(PlayerActionType.ALL_IN, 50) #Flop 1
        ]
    )

    player_3_preset_actions = ChooseActionFactory.create_choose_action_predetermined_human_player(
        [
            PlayerAction(PlayerActionType.CALL, 50), #Pre-flop 6
            PlayerAction(PlayerActionType.ALL_IN, 100) #Flop 2
        ]
    )

    player_4_preset_actions = ChooseActionFactory.create_choose_action_predetermined_human_player(
        [
            PlayerAction(PlayerActionType.CALL, 50), #Pre-flop 1
            PlayerAction(PlayerActionType.CALL, 50), #Pre-flop 7
            PlayerAction(PlayerActionType.ALL_IN, 150) #Flop 3
        ]
    )

    player_5_preset_actions = ChooseActionFactory.create_choose_action_predetermined_human_player(
        [
            PlayerAction(PlayerActionType.CALL, 50), #Pre-flop 2
            PlayerAction(PlayerActionType.FOLD, 0), #Pre-flop 8
        ]
    )

    player_6_preset_actions = ChooseActionFactory.create_choose_action_predetermined_human_player(
        [
            PlayerAction(PlayerActionType.CALL, 50), #Pre-flop 3
            PlayerAction(PlayerActionType.CALL, 50), #Pre-flop 9
            PlayerAction(PlayerActionType.FOLD, 0), #Flop 4
        ]
    )

    player_1.predefine_choose_action(player_1_preset_actions)
    player_2.predefine_choose_action(player_2_preset_actions)
    player_3.predefine_choose_action(player_3_preset_actions)
    player_4.predefine_choose_action(player_4_preset_actions)
    player_5.predefine_choose_action(player_5_preset_actions)
    player_6.predefine_choose_action(player_6_preset_actions)

    preset_deck = PresetDeck(6, 2)

    preset_deck.preset_player_cards(0, [
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.FOUR, Suit.DIAMONDS)
    ])

    preset_deck.preset_player_cards(1, [
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.THREE, Suit.DIAMONDS)
    ])

    preset_deck.preset_player_cards(2, [
        Card(Rank.SEVEN, Suit.CLUBS),
        Card(Rank.SEVEN, Suit.DIAMONDS)
    ])

    preset_deck.preset_player_cards(3, [
        Card(Rank.EIGHT, Suit.CLUBS),
        Card(Rank.EIGHT, Suit.DIAMONDS)
    ])

    preset_deck.preset_player_cards(4, [
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.ACE, Suit.SPADES)
    ])

    preset_deck.preset_player_cards(5, [
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.ACE, Suit.SPADES)
    ])

    preset_deck.preset_community(
        [
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.ACE, Suit.SPADES),
            Card(Rank.FIVE, Suit.HEARTS),
            Card(Rank.JACK, Suit.CLUBS),
            Card(Rank.NINE, Suit.DIAMONDS)
        ]
    )

    player_1_best_hand = Hand(
        [
            Card(Rank.ACE, Suit.HEARTS), 
            Card(Rank.ACE, Suit.SPADES), 
            Card(Rank.JACK, Suit.CLUBS), 
            Card(Rank.NINE, Suit.DIAMONDS), 
            Card(Rank.JACK, Suit.HEARTS)
        ])

    player_2_best_hand = Hand(
        [
            Card(Rank.ACE, Suit.HEARTS), 
            Card(Rank.ACE, Suit.SPADES), 
            Card(Rank.JACK, Suit.CLUBS), 
            Card(Rank.NINE, Suit.DIAMONDS), 
            Card(Rank.ACE, Suit.CLUBS)
        ])

    player_3_best_hand = Hand(
        [
            Card(Rank.ACE, Suit.HEARTS), 
            Card(Rank.ACE, Suit.SPADES), 
            Card(Rank.JACK, Suit.CLUBS), 
            Card(Rank.SEVEN, Suit.CLUBS), 
            Card(Rank.SEVEN, Suit.DIAMONDS)
        ])

    player_4_best_hand = Hand(
        [
            Card(Rank.ACE, Suit.HEARTS), 
            Card(Rank.ACE, Suit.SPADES), 
            Card(Rank.JACK, Suit.CLUBS), 
            Card(Rank.EIGHT, Suit.CLUBS), 
            Card(Rank.EIGHT, Suit.DIAMONDS)
        ])

    player_5_best_hand = None
    player_6_best_hand = None

    game_first = Game(default_game_settings(preset_deck))
    game_first.add_player(player_1)
    game_first.add_player(player_2)
    game_first.add_player(player_3)
    game_first.add_player(player_4)
    game_first.add_player(player_5)
    game_first.add_player(player_6)

    game_first.start_game()

    assert len(game_first.pots) == 4

    assert player_1.best_hand.__repr__() == player_1_best_hand.__repr__()
    assert player_2.best_hand.__repr__() == player_2_best_hand.__repr__()
    assert player_3.best_hand.__repr__() == player_3_best_hand.__repr__()
    assert player_4.best_hand.__repr__() == player_4_best_hand.__repr__()
    assert player_5.best_hand.__repr__() == player_5_best_hand.__repr__()
    assert player_6.best_hand.__repr__() == player_6_best_hand.__repr__()
    
    assert player_1.user.money == 0
    assert player_2.user.money == 700
    assert player_3.user.money == 0
    assert player_4.user.money == 150
    assert player_5.user.money == 950
    assert player_6.user.money == 900

if __name__ == "__main__":
    retcode = pytest.main(["test/game/test_game_6pl.py"])