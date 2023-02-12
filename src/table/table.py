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
    
    def new_game(self):
        self.current_game = Game(self.game_settings)
        self.current_game.table = self

    def start_game(self):
        self.current_game.start_game()
        self.game_history.append(self.current_game)

    def rotate_button(self) -> Game:
        self.next_dealer()

        if self.game_settings.small_blind_enabled:
            self.next_small_blind_holder()

        if self.game_settings.big_blind_enabled:
            self.next_big_blind_holder()

    def __index_diff(self, index_1: int, index_2: int) -> int:
        dif: int = 0

        if index_1 is None or index_2 is None:
            return 0

        while index_1 != index_2:
            index_1 = self.__next_index(index_1)
            dif += 1

        return dif

    def __next_index(self, indexer: int) -> int:
        indexer += 1

        if indexer >= len(self.users):
            indexer = 0

        return indexer

    def __prev_index(self, indexer: int) -> int:
        indexer -= 1

        if indexer < 0:
            indexer = len(self.users) - 1

        return indexer

    def next_big_blind_holder(self) -> None:
        self.game_settings.set_big_blind_holder(self.__next_index(self.game_settings.big_blind_holder))

    def next_small_blind_holder(self) -> None:
        self.game_settings.set_small_blind_holder(self.__next_index(self.game_settings.small_blind_holder))

    def next_dealer(self) -> None:
        self.game_settings.set_dealer(self.__next_index(self.game_settings.dealer_index))

    def add_user(self, user: User) -> None:
        self.game_settings.validate_money_for_game_settings(user.money)
        self.users.append(user)

    def remove_user(self, user: User) -> None:
        dealer_user: User = self.dealer_user
        old_dealer_index = self.users.index(dealer_user)

        small_blind_holder_diff = self.__index_diff(old_dealer_index, self.game_settings.small_blind_holder)
        big_blind_holder_diff = self.__index_diff(old_dealer_index, self.game_settings.big_blind_holder)

        self.users.remove(user)

        def restore_relative_to_dealer(dealer_index: int, diff: int) -> int:            
            new_index: int = dealer_index

            #Restore the blind_holder relative to the dealer
            for i in range(0, diff):
                new_index = self.__next_index(new_index)

            return new_index

        if dealer_user == user:
            self.game_settings.dealer_index = self.__prev_index(self.game_settings.dealer_index)

        else:
            self.game_settings.dealer_index = self.users.index(dealer_user)

        if self.game_settings.small_blind_enabled:
            self.game_settings.small_blind_holder = restore_relative_to_dealer(
                self.game_settings.dealer_index, small_blind_holder_diff)

        if self.game_settings.big_blind_enabled:
            self.game_settings.big_blind_holder = restore_relative_to_dealer(
                self.game_settings.dealer_index, big_blind_holder_diff)

    @property
    def dealer_user(self) -> User:
        return self.users[self.game_settings.dealer_index]

    @property
    def small_blind_user(self) -> User:
        if not self.game_settings.small_blind_enabled:
            return None

        return self.users[self.game_settings.small_blind_holder]

    @property
    def big_blind_user(self) -> User:
        if not self.game_settings.big_blind_enabled:
            return None

        return self.users[self.game_settings.big_blind_holder]

