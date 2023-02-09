from typing import List
from game.deck.deck import Deck
from game.game import Game
from game.player.player import Player
from game.user import User

class Table:

    def __init__(self, small_blind_bet: float, big_blind_bet: float) -> None:
        self.dealer_index: int = 0

        self.small_blind_bet: float = small_blind_bet
        self.small_blind_holder: int = 1
        
        self.big_blind_bet: float = big_blind_bet
        self.big_blind_holder: int = 2 

        self.users: List[User] = []
        self.current_game: Game = None
        self.total_games: List[Game] = []

        self.has_rotated_button = False
    
    def new_game(self, deck: Deck):
        self.current_game = Game(deck, -1, -1)
        self.current_game.table = self

    def start_game(self):
        if self.current_game.two_player_game and not self.has_rotated_button:
            self.small_blind_holder = 0
            self.big_blind_holder = 1

        self.current_game.small_blind_bet = self.small_blind_bet
        self.current_game.big_blind_bet = self.big_blind_bet

        self.current_game.dealer_index = self.dealer_index
        self.current_game.small_blind_holder = self.small_blind_holder
        self.current_game.big_blind_holder = self.big_blind_holder

        self.current_game.start_game()

    def reset_button(self):
        self.dealer_index = 0
        self.small_blind_holder = 1 if len(self.users.count) != 2 else 0
        self.big_blind_holder = 2 if len(self.users.count) != 2 else 1

        self.has_rotated_button = False

    def rotate_button(self) -> Game:
        self.has_rotated_button = True

        self.next_dealer()
        self.next_small_blind_holder()
        self.next_big_blind_holder()

    def __next_index(self, indexer: int) -> int:
        indexer += 1

        if indexer == len(self.users):
            indexer = 0

        return indexer

    def next_big_blind_holder(self) -> None:
        self.big_blind_holder = self.__next_index(self.big_blind_holder)

    def next_small_blind_holder(self) -> None:
        self.small_blind_holder = self.__next_index(self.small_blind_holder)

    def next_dealer(self) -> None:
        self.dealer_index = self.__next_index(self.dealer_index)

    def _validate_money_for_big_blind_bet(self, money: float) -> None:
        if money < self.big_blind_bet:
            raise ValueError("The player that you are trying to add has less money than required to sit on the table!")

    def add_user(self, user: User) -> None:
        self._validate_money_for_big_blind_bet(user.money)

        self.users.append(user)
