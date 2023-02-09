from typing import List
from game.game import Game
from game.user import User

class Table:

    def __init__(self) -> None:
        self.users: List[User] = []
        self.total_games: List[Game] = []
        