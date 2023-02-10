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

users_original_money = [100, 150, 200, 250, 1000, 1000]

user_1 = User("Roskata", 100)
user_2 = User("Stefan", 150)
user_3 = User("Kris", 200)
user_4 = User("Miro", 250)
user_5 = User("Ge6a", 1000)
user_6 = User("Pe6o", 1000)

bot_player_1 = BotPlayer(user_1)
bot_player_2 = BotPlayer(user_2)
bot_player_3 = BotPlayer(user_3)
bot_player_4 = BotPlayer(user_4)
bot_player_5 = BotPlayer(user_5)
bot_player_6 = BotPlayer(user_6)

human_player_1 = HumanPlayer(user_1)
human_player_2 = HumanPlayer(user_2)
human_player_3 = HumanPlayer(user_3)
human_player_4 = HumanPlayer(user_4)
human_player_5 = HumanPlayer(user_5)
human_player_6 = HumanPlayer(user_6)

bot_player_1.predefine_choose_action(ChooseActionFactory.create_choose_action_always_random(
    [PlayerActionType.FOLD, PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
))
bot_player_2.predefine_choose_action(ChooseActionFactory.create_choose_action_always_random(
    [PlayerActionType.FOLD, PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
))
bot_player_3.predefine_choose_action(ChooseActionFactory.create_choose_action_always_random(
    [PlayerActionType.FOLD, PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
))
bot_player_4.predefine_choose_action(ChooseActionFactory.create_choose_action_always_random(
    [PlayerActionType.FOLD, PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
))
bot_player_5.predefine_choose_action(ChooseActionFactory.create_choose_action_always_random(
    [PlayerActionType.FOLD, PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
))
bot_player_6.predefine_choose_action(ChooseActionFactory.create_choose_action_always_random(
    [PlayerActionType.FOLD, PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
))

game_settings = (GameSetting()
            .enable_big_blind(50, 2)
            .enable_small_blind(25, 1)
            .set_dealer(0)
            .set_hand_visibility(HandVisibilitySetting.ALL)
            .enable_ante(25)
            .set_deck(Deck())
            )
# game_settings.set_deck(preset_deck)

game_first = Game(game_settings)
game_first.add_player(bot_player_1)
game_first.add_player(bot_player_2)
game_first.add_player(bot_player_3)
game_first.add_player(bot_player_4)
game_first.add_player(bot_player_5)
game_first.add_player(bot_player_6)

# game_first.add_player(human_player_1)
# game_first.add_player(human_player_2)
# game_first.add_player(human_player_3)
# game_first.add_player(human_player_4)
# game_first.add_player(human_player_5)
# game_first.add_player(human_player_6)

game_first.start_game()