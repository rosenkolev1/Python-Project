from typing import List
from src.game.deck.deck import Deck
from src.game.game import Game
from src.game.player.player import Player
from src.game.setting.game_setting import GameSetting
from src.user.user import User

class Table:

    def __init__(self, game_setting: GameSetting) -> None:
        self.game_settings = game_setting
        self.users: List[User] = []
        self.current_game: Game = None
        self.game_history: List[Game] = []

        self.has_rotated_button = False
    
    def new_game(self):
        self.current_game = Game(self.game_settings)
        self.current_game.table = self

    def start_game(self):
        if self.current_game.is_two_player_game and not self.has_rotated_button:
            self.game_settings.set_small_blind_holder(0)
            self.game_settings.set_big_blind_holder(1)
        #In this case, for some reason(*cough* removing players *cough*) the big and small blinds are the same,
        #So change them. They should both be equal to zero before the change
        #Also set the dealer, who should be equal to one, to be equal to the small blind holder, i.e. to 0
        #TODO: Should probably instead make a function for removing users which deals internally with the movement
        # of the dealer and the big and small blind holders 
        elif (self.current_game.is_two_player_game and 
              self.game_settings.small_blind_holder == self.game_settings.big_blind_holder):
            self.game_settings.set_dealer(0)
            self.game_settings.set_big_blind_holder(1)



        self.current_game.start_game()
        self.game_history.append(self.current_game)

    def reset_button(self):
        self.game_settings.set_dealer(0)
        self.game_settings.set_small_blind_holder(1 if len(self.users.count) != 2 else 0)
        self.game_settings.set_big_blind_holder(2 if len(self.users.count) != 2 else 1)

        self.has_rotated_button = False

    def rotate_button(self) -> Game:
        self.has_rotated_button = True

        self.next_dealer()
        self.next_small_blind_holder()
        self.next_big_blind_holder()

    def __next_index(self, indexer: int) -> int:
        indexer += 1

        if indexer >= len(self.users):
            indexer = 0

        return indexer

    def next_big_blind_holder(self) -> None:
        self.game_settings.set_big_blind_holder(self.__next_index(self.game_settings.big_blind_holder))

    def next_small_blind_holder(self) -> None:
        self.game_settings.set_small_blind_holder(self.__next_index(self.game_settings.small_blind_holder))

    def next_dealer(self) -> None:
        self.game_settings.set_dealer(self.__next_index(self.game_settings.dealer_index))

    def add_user(self, user: User) -> None:
        self.game_settings._validate_money_for_game_settings(user.money)
        self.users.append(user)
