from typing import List
import pytest

from src.game.deck.preset_deck import PresetDeck
from src.game.game import Game
from src.game.hand.hand import Hand
from src.game.player.bot_player import BotPlayer
from src.game.player.choose_action.choose_action_factory import ChooseActionFactory
from src.game.player.human_player import HumanPlayer
from src.game.player.player_action.player_action import PlayerAction
from src.game.player.player_action.player_action_type import PlayerActionType
from src.game.setting.game_setting import GameSetting
from src.game.setting.hand_visibility_setting import HandVisibilitySetting
from src.user.user import User
from src.game.deck.card import Card
from src.game.deck.rank import Rank
from src.game.deck.suit import Suit
from test.game.helper.settings_functions import default_game_settings

@pytest.mark.parametrize("user_first,user_second,user_third,user_first_expected_balance,user_second_expected_balance,user_third_expected_balance", 
    [
        (User("roskata", 100), User("stefan", 200), User("kris", 200), 0, 0, 500),
        (User("roskata", 200), User("stefan", 200), User("kris", 200), 0, 0, 600),
    ])
def test_3_players_always_raise(user_first: User, user_second: User, user_third: User,
                                   user_first_expected_balance: float, user_second_expected_balance: float, user_third_expected_balance: float):
    preset_deck = PresetDeck(3, 2)

    preset_deck.preset_player_cards(0, [Card(Rank.TWO, Suit.CLUBS), Card(Rank.EIGHT, Suit.DIAMONDS)])
    preset_deck.preset_player_cards(1, [Card(Rank.THREE, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS)])
    preset_deck.preset_player_cards(2, [Card(Rank.ACE, Suit.CLUBS), Card(Rank.ACE, Suit.DIAMONDS)])

    preset_deck.preset_flop([Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS)])
    preset_deck.preset_turn(Card(Rank.SEVEN, Suit.CLUBS))
    preset_deck.preset_river(Card(Rank.ACE, Suit.HEARTS))

    player_first = BotPlayer(user_first, ChooseActionFactory.create_choose_action_always_raise_if_possible())
    player_second = BotPlayer(user_second, ChooseActionFactory.create_choose_action_always_raise_if_possible())
    player_third = BotPlayer(user_third, ChooseActionFactory.create_choose_action_always_raise_if_possible())

    player_first_best_hand = Hand(
        [
            Card(Rank.FOUR, Suit.DIAMONDS), 
            Card(Rank.FOUR, Suit.CLUBS), 
            Card(Rank.SEVEN, Suit.CLUBS), 
            Card(Rank.ACE, Suit.HEARTS), 
            Card(Rank.EIGHT, Suit.DIAMONDS)
        ])

    player_second_best_hand = Hand(
        [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.SEVEN, Suit.DIAMONDS)])
    
    player_third_best_hand = Hand(
        [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.ACE, Suit.CLUBS), Card(Rank.ACE, Suit.DIAMONDS)])

    game_first = Game(default_game_settings(preset_deck))
    game_first.add_player(player_first)
    game_first.add_player(player_second)
    game_first.add_player(player_third)

    game_first.start_game()

    assert user_first.money == user_first_expected_balance
    assert user_second.money == user_second_expected_balance
    assert user_third.money == user_third_expected_balance

    assert game_first.players[0].best_hand.__repr__() == player_first_best_hand.__repr__()
    assert game_first.players[1].best_hand.__repr__() == player_second_best_hand.__repr__()
    assert game_first.players[2].best_hand.__repr__() == player_third_best_hand.__repr__()

@pytest.mark.parametrize("user_first,user_second,user_third,user_first_expected_balance,user_second_expected_balance,user_third_expected_balance", 
    [
        (User("roskata", 100), User("stefan", 200), User("kris", 200), 0, 20, 480),
    ])
def test_3_human_players_single_side_pot_winner_is_from_main_pot_no_fold(user_first: User, user_second: User, user_third: User,
                                   user_first_expected_balance: float, user_second_expected_balance: float, user_third_expected_balance: float):
    preset_deck = PresetDeck(3, 2)

    preset_deck.preset_player_cards(0, [Card(Rank.TWO, Suit.CLUBS), Card(Rank.EIGHT, Suit.DIAMONDS)])
    preset_deck.preset_player_cards(1, [Card(Rank.THREE, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS)])
    preset_deck.preset_player_cards(2, [Card(Rank.ACE, Suit.CLUBS), Card(Rank.ACE, Suit.DIAMONDS)])

    preset_deck.preset_flop([Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS)])
    preset_deck.preset_turn(Card(Rank.SEVEN, Suit.CLUBS))
    preset_deck.preset_river(Card(Rank.ACE, Suit.HEARTS))

    player_first_actions = ChooseActionFactory.create_choose_action_predetermined_human_player(
            [
                PlayerAction(PlayerActionType.ALL_IN, 100) #Pre-flop
            ]
        )
    
    player_second_actions = ChooseActionFactory.create_choose_action_predetermined_human_player(
            [
                PlayerAction(PlayerActionType.CALL, 75), #Pre-flop
                PlayerAction(PlayerActionType.CHECK, 0), #Flop
                PlayerAction(PlayerActionType.CALL, 50),
                PlayerAction(PlayerActionType.CHECK, 0), #Turn
                PlayerAction(PlayerActionType.CHECK, 0), #River
                PlayerAction(PlayerActionType.CALL, 30)
            ], 
        )
    
    player_third_actions = ChooseActionFactory.create_choose_action_predetermined_human_player(
            [
                PlayerAction(PlayerActionType.CALL, 50), #Pre-flop
                PlayerAction(PlayerActionType.BET, 50), #Flop
                PlayerAction(PlayerActionType.CHECK, 0), #Turn
                PlayerAction(PlayerActionType.BET, 30) #River
            ], 
        )

    # player_first = BotPlayer(user_first, player_first_actions)
    # player_second = BotPlayer(user_second, player_second_actions)
    # player_third = BotPlayer(user_third, player_third_actions)
    player_first = HumanPlayer(user_first)
    player_second = HumanPlayer(user_second)
    player_third = HumanPlayer(user_third)

    player_first.predefine_choose_action(player_first_actions)
    player_second.predefine_choose_action(player_second_actions)
    player_third.predefine_choose_action(player_third_actions)

    player_first_best_hand = Hand(
        [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.EIGHT, Suit.DIAMONDS)])

    player_second_best_hand = Hand(
        [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.SEVEN, Suit.DIAMONDS)])
    
    player_third_best_hand = Hand(
        [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.ACE, Suit.CLUBS), Card(Rank.ACE, Suit.DIAMONDS)])

    game_first = Game(default_game_settings(preset_deck))
    game_first.add_player(player_first)
    game_first.add_player(player_second)
    game_first.add_player(player_third)

    game_first.start_game()

    assert user_first.money == user_first_expected_balance
    assert user_second.money == user_second_expected_balance
    assert user_third.money == user_third_expected_balance

    assert game_first.players[0].best_hand.__repr__() == player_first_best_hand.__repr__()
    assert game_first.players[1].best_hand.__repr__() == player_second_best_hand.__repr__()
    assert game_first.players[2].best_hand.__repr__() == player_third_best_hand.__repr__()

@pytest.mark.parametrize("user_first,user_second,user_third,user_first_expected_balance,user_second_expected_balance,user_third_expected_balance", 
    [
        (User("roskata", 100), User("stefan", 200), User("kris", 200), 300, 180, 20),
    ])
def test_3_players_single_side_pot_winner_is_from_side_pot_no_fold(user_first: User, user_second: User, user_third: User,
                                   user_first_expected_balance: float, user_second_expected_balance: float, user_third_expected_balance: float):
    preset_deck = PresetDeck(3, 2)

    preset_deck.preset_player_cards(0, [Card(Rank.ACE, Suit.CLUBS), Card(Rank.ACE, Suit.DIAMONDS)])
    preset_deck.preset_player_cards(1, [Card(Rank.THREE, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS)])
    preset_deck.preset_player_cards(2, [Card(Rank.TWO, Suit.CLUBS), Card(Rank.EIGHT, Suit.DIAMONDS)])

    preset_deck.preset_flop([Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS)])
    preset_deck.preset_turn(Card(Rank.SEVEN, Suit.CLUBS))
    preset_deck.preset_river(Card(Rank.ACE, Suit.HEARTS))

    player_first_actions = ChooseActionFactory.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.ALL_IN, 100) #Pre-flop
            ]
        )
    
    player_second_actions = ChooseActionFactory.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.CALL, 75), #Pre-flop
                PlayerAction(PlayerActionType.CHECK, 0), #Flop
                PlayerAction(PlayerActionType.CALL, 50),
                PlayerAction(PlayerActionType.CHECK, 0), #Turn
                PlayerAction(PlayerActionType.CHECK, 0), #River
                PlayerAction(PlayerActionType.CALL, 30)
            ], 
        )
    
    player_third_actions = ChooseActionFactory.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.CALL, 50), #Pre-flop
                PlayerAction(PlayerActionType.BET, 50), #Flop
                PlayerAction(PlayerActionType.CHECK, 0), #Turn
                PlayerAction(PlayerActionType.BET, 30) #River
            ],
        )

    player_first = BotPlayer(user_first, player_first_actions)
    player_second = BotPlayer(user_second, player_second_actions)
    player_third = BotPlayer(user_third, player_third_actions)

    player_first_best_hand = Hand(
        [
            Card(Rank.FOUR, Suit.DIAMONDS), 
            Card(Rank.FOUR, Suit.CLUBS), 
            Card(Rank.ACE, Suit.HEARTS), 
            Card(Rank.ACE, Suit.CLUBS), 
            Card(Rank.ACE, Suit.DIAMONDS)
        ])

    player_second_best_hand = Hand(
        [
            Card(Rank.FOUR, Suit.DIAMONDS), 
            Card(Rank.FOUR, Suit.CLUBS), 
            Card(Rank.SEVEN, Suit.CLUBS), 
            Card(Rank.ACE, Suit.HEARTS), 
            Card(Rank.SEVEN, Suit.DIAMONDS)
        ])
    
    player_third_best_hand = Hand(
        [
            Card(Rank.FOUR, Suit.DIAMONDS), 
            Card(Rank.FOUR, Suit.CLUBS), 
            Card(Rank.SEVEN, Suit.CLUBS), 
            Card(Rank.ACE, Suit.HEARTS), 
            Card(Rank.EIGHT, Suit.DIAMONDS)
        ])

    game_first = Game(default_game_settings(preset_deck))
    game_first.add_player(player_first)
    game_first.add_player(player_second)
    game_first.add_player(player_third)

    game_first.start_game()

    assert user_first.money == user_first_expected_balance
    assert user_second.money == user_second_expected_balance
    assert user_third.money == user_third_expected_balance

    assert game_first.players[0].best_hand.__repr__() == player_first_best_hand.__repr__()
    assert game_first.players[1].best_hand.__repr__() == player_second_best_hand.__repr__()
    assert game_first.players[2].best_hand.__repr__() == player_third_best_hand.__repr__()

@pytest.mark.parametrize("user_first,user_second,user_third,user_first_expected_balance,user_second_expected_balance,user_third_expected_balance", 
    [
        (User("roskata", 100), User("stefan", 200), User("kris", 200), 175, 175, 150),
    ])
def test_3_players_single_side_pot_winner_is_all_in_others_fold(user_first: User, user_second: User, user_third: User,
                                   user_first_expected_balance: float, user_second_expected_balance: float, user_third_expected_balance: float):
    preset_deck = PresetDeck(3, 2)

    preset_deck.preset_player_cards(0, [Card(Rank.ACE, Suit.CLUBS), Card(Rank.ACE, Suit.DIAMONDS)])
    preset_deck.preset_player_cards(1, [Card(Rank.THREE, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS)])
    preset_deck.preset_player_cards(2, [Card(Rank.TWO, Suit.CLUBS), Card(Rank.EIGHT, Suit.DIAMONDS)])

    preset_deck.preset_flop([Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS)])
    preset_deck.preset_turn(Card(Rank.SEVEN, Suit.CLUBS))
    preset_deck.preset_river(Card(Rank.ACE, Suit.HEARTS))

    player_first_actions = ChooseActionFactory.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.ALL_IN, 100) #Pre-flop
            ]
        )
    
    player_second_actions = ChooseActionFactory.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.FOLD, 0), #Pre-flop
            ], 
        )
    
    player_third_actions = ChooseActionFactory.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.FOLD, 0), #Pre-flop
            ],
        )

    player_first = BotPlayer(user_first, player_first_actions)
    player_second = BotPlayer(user_second, player_second_actions)
    player_third = BotPlayer(user_third, player_third_actions)

    game_first = Game(default_game_settings(preset_deck))
    game_first.add_player(player_first)
    game_first.add_player(player_second)
    game_first.add_player(player_third)

    game_first.start_game()

    assert user_first.money == user_first_expected_balance
    assert user_second.money == user_second_expected_balance
    assert user_third.money == user_third_expected_balance

    assert game_first.players[0].best_hand is None
    assert game_first.players[1].best_hand is None
    assert game_first.players[2].best_hand is None

@pytest.mark.parametrize("user_first,user_second,user_third,user_first_expected_balance,user_second_expected_balance,user_third_expected_balance", 
    [
        (User("roskata", 100), User("stefan", 200), User("kris", 200), 0, 250, 250),
    ])
def test_3_players_single_side_pot_2_way_tie_for_main_all_in_player_looses_no_fold(user_first: User, user_second: User, user_third: User,
                                   user_first_expected_balance: float, user_second_expected_balance: float, user_third_expected_balance: float):
    preset_deck = PresetDeck(3, 2)

    preset_deck.preset_player_cards(0, [Card(Rank.TWO, Suit.CLUBS), Card(Rank.EIGHT, Suit.DIAMONDS)])
    preset_deck.preset_player_cards(1, [Card(Rank.THREE, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS)])
    preset_deck.preset_player_cards(2, [Card(Rank.FIVE, Suit.HEARTS), Card(Rank.SEVEN, Suit.HEARTS)])

    preset_deck.preset_flop([Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS)])
    preset_deck.preset_turn(Card(Rank.SEVEN, Suit.CLUBS))
    preset_deck.preset_river(Card(Rank.ACE, Suit.HEARTS))

    player_first_actions = ChooseActionFactory.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.ALL_IN, 100) #Pre-flop
            ]
        )
    
    player_second_actions = ChooseActionFactory.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.CALL, 75), #Pre-flop
                PlayerAction(PlayerActionType.CHECK, 0), #Flop
                PlayerAction(PlayerActionType.CALL, 50),
                PlayerAction(PlayerActionType.CHECK, 0), #Turn
                PlayerAction(PlayerActionType.CHECK, 0), #River
                PlayerAction(PlayerActionType.CALL, 30)
            ], 
        )
    
    player_third_actions = ChooseActionFactory.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.CALL, 50), #Pre-flop
                PlayerAction(PlayerActionType.BET, 50), #Flop
                PlayerAction(PlayerActionType.CHECK, 0), #Turn
                PlayerAction(PlayerActionType.BET, 30) #River
            ],
        )

    player_first = BotPlayer(user_first, player_first_actions)
    player_second = BotPlayer(user_second, player_second_actions)
    player_third = BotPlayer(user_third, player_third_actions)

    player_first_best_hand = Hand(
        [
            Card(Rank.FOUR, Suit.DIAMONDS), 
            Card(Rank.FOUR, Suit.CLUBS), 
            Card(Rank.SEVEN, Suit.CLUBS), 
            Card(Rank.ACE, Suit.HEARTS), 
            Card(Rank.EIGHT, Suit.DIAMONDS)
        ])

    player_second_best_hand = Hand(
        [
            Card(Rank.FOUR, Suit.DIAMONDS), 
            Card(Rank.FOUR, Suit.CLUBS), 
            Card(Rank.SEVEN, Suit.CLUBS), 
            Card(Rank.ACE, Suit.HEARTS), 
            Card(Rank.SEVEN, Suit.DIAMONDS)
        ])
    
    player_third_best_hand = Hand(
        [
            Card(Rank.FOUR, Suit.DIAMONDS), 
            Card(Rank.FOUR, Suit.CLUBS), 
            Card(Rank.SEVEN, Suit.CLUBS), 
            Card(Rank.ACE, Suit.HEARTS), 
            Card(Rank.SEVEN, Suit.HEARTS)
        ])

    game_first = Game(default_game_settings(preset_deck))
    game_first.add_player(player_first)
    game_first.add_player(player_second)
    game_first.add_player(player_third)

    game_first.start_game()

    assert user_first.money == user_first_expected_balance
    assert user_second.money == user_second_expected_balance
    assert user_third.money == user_third_expected_balance

    assert game_first.players[0].best_hand.__repr__() == player_first_best_hand.__repr__()
    assert game_first.players[1].best_hand.__repr__() == player_second_best_hand.__repr__()
    assert game_first.players[2].best_hand.__repr__() == player_third_best_hand.__repr__()

@pytest.mark.parametrize("user_first,user_second,user_third,user_first_expected_balance,user_second_expected_balance,user_third_expected_balance", 
    [
        (User("roskata", 100), User("stefan", 200), User("kris", 200), 300, 100, 100),
    ])
def test_3_players_single_side_pot_2_way_tie_for_main_all_in_player_wins_side(user_first: User, user_second: User, user_third: User,
                                   user_first_expected_balance: float, user_second_expected_balance: float, user_third_expected_balance: float):
    preset_deck = PresetDeck(3, 2)

    preset_deck.preset_player_cards(0, [Card(Rank.ACE, Suit.CLUBS), Card(Rank.ACE, Suit.DIAMONDS)])
    preset_deck.preset_player_cards(1, [Card(Rank.THREE, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS)])
    preset_deck.preset_player_cards(2, [Card(Rank.FIVE, Suit.HEARTS), Card(Rank.SEVEN, Suit.HEARTS)])

    preset_deck.preset_flop([Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS)])
    preset_deck.preset_turn(Card(Rank.SEVEN, Suit.CLUBS))
    preset_deck.preset_river(Card(Rank.ACE, Suit.HEARTS))

    player_first_actions = ChooseActionFactory.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.ALL_IN, 100) #Pre-flop
            ]
        )
    
    player_second_actions = ChooseActionFactory.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.CALL, 75), #Pre-flop
                PlayerAction(PlayerActionType.CHECK, 0), #Flop
                PlayerAction(PlayerActionType.CALL, 50),
                PlayerAction(PlayerActionType.CHECK, 0), #Turn
                PlayerAction(PlayerActionType.CHECK, 0), #River
                PlayerAction(PlayerActionType.CALL, 30)
            ], 
        )
    
    player_third_actions = ChooseActionFactory.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.CALL, 50), #Pre-flop
                PlayerAction(PlayerActionType.BET, 50), #Flop
                PlayerAction(PlayerActionType.CHECK, 0), #Turn
                PlayerAction(PlayerActionType.BET, 30) #River
            ],
        )

    player_first = BotPlayer(user_first, player_first_actions)
    player_second = BotPlayer(user_second, player_second_actions)
    player_third = BotPlayer(user_third, player_third_actions)

    player_first_best_hand = Hand(
        [
            Card(Rank.FOUR, Suit.DIAMONDS), 
            Card(Rank.FOUR, Suit.CLUBS), 
            Card(Rank.ACE, Suit.HEARTS), 
            Card(Rank.ACE, Suit.CLUBS), 
            Card(Rank.ACE, Suit.DIAMONDS)
        ])

    player_second_best_hand = Hand(
        [
            Card(Rank.FOUR, Suit.DIAMONDS), 
            Card(Rank.FOUR, Suit.CLUBS), 
            Card(Rank.SEVEN, Suit.CLUBS), 
            Card(Rank.ACE, Suit.HEARTS), 
            Card(Rank.SEVEN, Suit.DIAMONDS)
        ])
    
    player_third_best_hand = Hand(
        [
            Card(Rank.FOUR, Suit.DIAMONDS), 
            Card(Rank.FOUR, Suit.CLUBS), 
            Card(Rank.SEVEN, Suit.CLUBS), 
            Card(Rank.ACE, Suit.HEARTS), 
            Card(Rank.SEVEN, Suit.HEARTS)
        ])

    game_first = Game(default_game_settings(preset_deck))
    game_first.add_player(player_first)
    game_first.add_player(player_second)
    game_first.add_player(player_third)

    game_first.start_game()

    assert user_first.money == user_first_expected_balance
    assert user_second.money == user_second_expected_balance
    assert user_third.money == user_third_expected_balance

    assert game_first.players[0].best_hand.__repr__() == player_first_best_hand.__repr__()
    assert game_first.players[1].best_hand.__repr__() == player_second_best_hand.__repr__()
    assert game_first.players[2].best_hand.__repr__() == player_third_best_hand.__repr__()

if __name__ == "__main__":
    retcode = pytest.main()