from typing import List
import pytest

from game.deck.deck import Deck
from game.game import Game
from game.hand import Hand
from game.player_action import PlayerAction
from game.player_action_type import PlayerActionType
from game.pot_player import PotPlayer
from game.user import User
from game.deck.card import Card
from game.deck.rank import Rank
from game.deck.suit import Suit

from test.mock.mock_choose_action import MockChooseAction
from test.mock.mock_deck import MockDeck
from test.mock.mock_empty_deck import MockEmptyDeck
from test.mock.mock_player import MockPlayer

@pytest.mark.parametrize("user_first,user_second,user_first_expected_balance,user_second_expected_balance", 
    [
        (User("roskata", 100), User("stefan", 200), 0, 300), # roskata is all-in at pre_flop
        (User("roskata", 200), User("stefan", 200), 0, 400), # roskata and stefan are all-in at pre-flop
    ])
def test_2_players_always_raise_one_or_both_all_in(user_first: User, user_second: User, user_first_expected_balance: float, user_second_expected_balance: float):
    mock_deck = MockDeck(2, 2)

    mock_deck.preset_player_cards(0, [Card(Rank.TWO, Suit.CLUBS), Card(Rank.EIGHT, Suit.DIAMONDS)])
    mock_deck.preset_player_cards(1, [Card(Rank.THREE, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS)])

    mock_deck.preset_flop([Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS)])
    mock_deck.preset_turn_or_river(Card(Rank.SEVEN, Suit.CLUBS))
    mock_deck.preset_turn_or_river(Card(Rank.ACE, Suit.HEARTS))

    player_first = MockPlayer(user_first, MockChooseAction.mock_choose_action_always_raise_if_possible)
    player_second = MockPlayer(user_second, MockChooseAction.mock_choose_action_always_raise_if_possible)

    player_first_best_hand = Hand(
        [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.EIGHT, Suit.DIAMONDS)])

    player_second_best_hand = Hand(
        [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.SEVEN, Suit.DIAMONDS)])

    game_first = Game(mock_deck, 25, 50)
    game_first.add_player(player_first)
    game_first.add_player(player_second)

    game_first.start_game()
    
    assert user_first.money == user_first_expected_balance
    assert user_second.money == user_second_expected_balance

    assert game_first.players[0].best_hand.__repr__() == player_first_best_hand.__repr__()
    assert game_first.players[1].best_hand.__repr__() == player_second_best_hand.__repr__()

@pytest.mark.parametrize("user_first,user_second,user_third,user_first_expected_balance,user_second_expected_balance,user_third_expected_balance", 
    [
        (User("roskata", 100), User("stefan", 200), User("kris", 200), 0, 0, 500),
        (User("roskata", 200), User("stefan", 200), User("kris", 200), 0, 0, 600),
    ])
def test_3_players_always_raise(user_first: User, user_second: User, user_third: User,
                                   user_first_expected_balance: float, user_second_expected_balance: float, user_third_expected_balance: float):
    mock_deck = MockDeck(3, 2)

    mock_deck.preset_player_cards(0, [Card(Rank.TWO, Suit.CLUBS), Card(Rank.EIGHT, Suit.DIAMONDS)])
    mock_deck.preset_player_cards(1, [Card(Rank.THREE, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS)])
    mock_deck.preset_player_cards(2, [Card(Rank.ACE, Suit.CLUBS), Card(Rank.ACE, Suit.DIAMONDS)])

    mock_deck.preset_flop([Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS)])
    mock_deck.preset_turn_or_river(Card(Rank.SEVEN, Suit.CLUBS))
    mock_deck.preset_turn_or_river(Card(Rank.ACE, Suit.HEARTS))

    player_first = MockPlayer(user_first, MockChooseAction.mock_choose_action_always_raise_if_possible)
    player_second = MockPlayer(user_second, MockChooseAction.mock_choose_action_always_raise_if_possible)
    player_third = MockPlayer(user_third, MockChooseAction.mock_choose_action_always_raise_if_possible)

    player_first_best_hand = Hand(
        [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.EIGHT, Suit.DIAMONDS)])

    player_second_best_hand = Hand(
        [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.SEVEN, Suit.DIAMONDS)])
    
    player_third_best_hand = Hand(
        [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.ACE, Suit.CLUBS), Card(Rank.ACE, Suit.DIAMONDS)])

    game_first = Game(mock_deck, 25, 50)
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
def test_3_players_single_side_pot_winner_is_from_main_pot_no_fold(user_first: User, user_second: User, user_third: User,
                                   user_first_expected_balance: float, user_second_expected_balance: float, user_third_expected_balance: float):
    mock_deck = MockDeck(3, 2)

    mock_deck.preset_player_cards(0, [Card(Rank.TWO, Suit.CLUBS), Card(Rank.EIGHT, Suit.DIAMONDS)])
    mock_deck.preset_player_cards(1, [Card(Rank.THREE, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS)])
    mock_deck.preset_player_cards(2, [Card(Rank.ACE, Suit.CLUBS), Card(Rank.ACE, Suit.DIAMONDS)])

    mock_deck.preset_flop([Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS)])
    mock_deck.preset_turn_or_river(Card(Rank.SEVEN, Suit.CLUBS))
    mock_deck.preset_turn_or_river(Card(Rank.ACE, Suit.HEARTS))

    player_first_actions = MockChooseAction.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.RAISE, 100) #Pre-flop
            ]
        )
    
    player_second_actions = MockChooseAction.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.CALL, 75), #Pre-flop
                PlayerAction(PlayerActionType.CHECK, 0), #Flop
                PlayerAction(PlayerActionType.CALL, 50),
                PlayerAction(PlayerActionType.CHECK, 0), #Turn
                PlayerAction(PlayerActionType.CHECK, 0), #River
                PlayerAction(PlayerActionType.CALL, 30)
            ], 
        )
    
    player_third_actions = MockChooseAction.create_choose_action_predetermined(
            [
                PlayerAction(PlayerActionType.CALL, 50), #Pre-flop
                PlayerAction(PlayerActionType.RAISE, 50), #Flop
                PlayerAction(PlayerActionType.CHECK, 0), #Turn
                PlayerAction(PlayerActionType.RAISE, 30)
            ], #River
        )

    player_first = MockPlayer(user_first, player_first_actions)
    player_second = MockPlayer(user_second, player_second_actions)
    player_third = MockPlayer(user_third, player_third_actions)

    player_first_best_hand = Hand(
        [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.EIGHT, Suit.DIAMONDS)])

    player_second_best_hand = Hand(
        [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.SEVEN, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.SEVEN, Suit.DIAMONDS)])
    
    player_third_best_hand = Hand(
        [Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS), Card(Rank.ACE, Suit.HEARTS), Card(Rank.ACE, Suit.CLUBS), Card(Rank.ACE, Suit.DIAMONDS)])

    game_first = Game(mock_deck, 25, 50)
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