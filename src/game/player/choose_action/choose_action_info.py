from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game.pot import Pot
    from src.game.game import Game

class ChooseActionInfo:

    def __init__(self, call_amount: float, pot: Pot, game: Game) -> None:
        self.call_amount = call_amount
        self.pot = pot
        self.game = game