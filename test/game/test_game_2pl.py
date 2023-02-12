from typing import List
import pytest

from src.game.deck.preset_deck import PresetDeck
from src.game.game import Game
from src.game.hand.hand import Hand
from src.game.player.bot_player import BotPlayer
from src.game.player.choose_action_factory import ChooseActionFactory
from src.game.player.player_action import PlayerAction
from src.game.player.player_action_type import PlayerActionType
from src.game.setting.game_setting import GameSetting
from src.game.setting.hand_visibility_setting import HandVisibilitySetting
from src.user.user import User
from src.game.deck.card import Card
from src.game.deck.rank import Rank
from src.game.deck.suit import Suit
from test.game.helper.settings_functions import default_game_settings

@pytest.mark.parametrize("user_first,user_second,user_first_expected_balance,user_second_expected_balance", 
    [
        (User("roskata", 100), User("stefan", 200), 0, 300), # roskata is all-in at pre_flop
        (User("roskata", 200), User("stefan", 200), 0, 400), # roskata and stefan are all-in at pre-flop
    ])
def test_2_players_always_raise_one_or_both_all_in(user_first: User, user_second: User, user_first_expected_balance: float, user_second_expected_balance: float):
    preset_deck = PresetDeck(2, 2)

    preset_deck.preset_player_cards(0, [Card(Rank.TWO, Suit.CLUBS), Card(Rank.EIGHT, Suit.DIAMONDS)])
    preset_deck.preset_player_cards(1, [Card(Rank.THREE, Suit.CLUBS), Card(Rank.SEVEN, Suit.DIAMONDS)])

    preset_deck.preset_flop([Card(Rank.THREE, Suit.SPADES), Card(Rank.FOUR, Suit.DIAMONDS), Card(Rank.FOUR, Suit.CLUBS)])
    preset_deck.preset_turn(Card(Rank.SEVEN, Suit.CLUBS))
    preset_deck.preset_river(Card(Rank.ACE, Suit.HEARTS))

    player_first = BotPlayer(user_first, ChooseActionFactory.create_choose_action_always_raise_if_possible())
    player_second = BotPlayer(user_second, ChooseActionFactory.create_choose_action_always_raise_if_possible())

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

    game_settings: GameSetting = default_game_settings(preset_deck)

    game_settings.set_small_blind_holder(0)
    game_settings.set_big_blind_holder(1)

    game_first = Game(game_settings)
    game_first.add_player(player_first)
    game_first.add_player(player_second)

    game_first.start_game()
    
    assert user_first.money == user_first_expected_balance
    assert user_second.money == user_second_expected_balance

    assert game_first.players[0].best_hand.__repr__() == player_first_best_hand.__repr__()
    assert game_first.players[1].best_hand.__repr__() == player_second_best_hand.__repr__()



if __name__ == "__main__":
    retcode = pytest.main()