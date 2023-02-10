from src.game.deck.card import Card
from src.game.deck.deck import Deck
from src.game.deck.preset_deck import PresetDeck
from src.game.deck.preset_empty_deck import PresetEmptyDeck
from src.game.deck.rank import Rank
from src.game.deck.suit import Suit
from src.game.game import Game
from src.game.hand.hand import Hand
from src.game.hand.hand_combination import HandCombination 
from src.game.player.player_action_type import PlayerActionType
from src.game.setting.game_setting import GameSetting
from src.game.setting.hand_visibility_setting import HandVisibilitySetting
from src.table.table import Table
from src.user.user import User
from src.game.player.player import Player
from src.game.player.bot_player import BotPlayer
from src.game.player.human_player import HumanPlayer
from src.game.player.player_action import PlayerAction
from src.game.player.choose_action_factory import ChooseActionFactory

user_first = User("Roskata", 100)
user_second = User("Stefan", 200)

# player_first = BotPlayer(user_first, ChooseActionFactory.create_choose_action_always_random(
#     [PlayerActionType.ALL_IN, PlayerActionType.FOLD], PlayerActionType.ALL_IN
# ))
player_first = HumanPlayer(user_first)

# player_second = BotPlayer(user_second, ChooseActionFactory.create_choose_action_always_random(
#     [PlayerActionType.ALL_IN, PlayerActionType.FOLD], PlayerActionType.ALL_IN
# ))

# player_second = BotPlayer(user_second, ChooseActionFactory.create_choose_action_predetermined(
#     [PlayerAction(PlayerActionType.CALL, 0)]
# ))

player_second = HumanPlayer(user_second)

# player_second = HumanPlayer(user_second)
# player_second.choose_action = lambda possible_actions, call_amount: ChooseActionFactory.create_choose_action_always_random(
#     [PlayerActionType.ALL_IN, PlayerActionType.FOLD], PlayerActionType.ALL_IN
# )(player_second, possible_actions, call_amount)
# player_second.predefine_choose_action(ChooseActionFactory.create_choose_action_always_random(
#     [PlayerActionType.ALL_IN, PlayerActionType.FOLD], PlayerActionType.ALL_IN
# ))

game_settings = GameSetting()
# game_settings.enable_big_blind(50)
game_settings.enable_small_blind(25)
game_settings.set_dealer(0)
game_settings.set_small_blind_holder(1)
# game_settings.set_big_blind_holder(2)
game_settings.set_hand_visibility(HandVisibilitySetting.ALL)
game_settings.set_deck(Deck())

game_first = Game(game_settings)
game_first.add_player(player_first)
game_first.add_player(player_second)

game_first.start_game()