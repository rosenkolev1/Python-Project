import sys
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
from src.game.setting.invalid_money_for_settings_exception import InvalidMoneyForSettingsException
from src.table.table import Table
from src.user.user import User
from src.game.player.player import Player
from src.game.player.bot_player import BotPlayer
from src.game.player.human_player import HumanPlayer
from src.game.player.player_action import PlayerAction
from src.game.player.choose_action_factory import ChooseActionFactory

user_1 = User("Roskata", 1000)
user_2 = User("Stefan", 1000)
user_3 = User("Kris", 1000)
user_4 = User("Miro", 1000)
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
            .enable_big_blind(50, 1)
            .enable_small_blind(25, 0)
            # .enable_ante(10)
            .set_dealer(-1)
            .set_hand_visibility(HandVisibilitySetting.ALL)
            # .set_deck(Deck())
            )

# game_1 = Game(game_settings)
# game_1.add_player(human_player_1)
# game_1.add_player(human_player_2)
# game_1.add_player(human_player_3)
# game_1.add_player(human_player_4)
# game_1.add_player(human_player_5)
# game_1.add_player(human_player_6)

# game_1.start_game()

table_1 = Table(game_settings)

table_1.add_user(user_1)
table_1.add_user(user_2)
table_1.add_user(user_3)
table_1.add_user(user_4)
table_1.add_user(user_5)
table_1.add_user(user_6)

#Redirect output to a file for fun
with open('tournament_games.txt', mode='w', encoding="utf-8") as sys.stdout:

    #Create a table and play games until there is a single winner left
    print("The tournament begins!\n\n")

    while True:
        game_settings.set_deck(Deck())
        table_1.new_game()

        new_table_users = []

        for i in range(0, len(table_1.users)):
            user = table_1.users[i]

            try:
                bot_player = BotPlayer(user, ChooseActionFactory.create_choose_action_always_random(
                            [PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
                        ))

                table_1.current_game.add_player(bot_player)
                
                new_table_users.append(user)
            except InvalidMoneyForSettingsException as e:
                print(f"\nPlayer: {user.name} has been eliminated from the tournament!!!\n")

        table_1.users = new_table_users

        if len(table_1.users) == 1:
            print(f"The winner of the tournament is {table_1.users[0].name}")
            break

        table_1.rotate_button()

        print(f"{'*' * 100} Game #{len(table_1.game_history) + 1} {'*' * 100}")
        table_1.start_game()
        print(f"{'*' * 100} End of Game #{len(table_1.game_history)} {'*' * 100}")

        if len(table_1.game_history) % 5 == 0:
            game_settings.big_blind_bet += 5
            game_settings.small_blind_bet = game_settings.big_blind_bet / 2

            print(f"\nBig blind increased to: {game_settings.big_blind_bet}")
            print(f"Small blind increased to: {game_settings.small_blind_bet}\n")