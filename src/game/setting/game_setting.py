
from src.game.deck.deck import Deck
from src.game.setting.hand_visibility_setting import HandVisibilitySetting


class GameSetting:

    def __init__(self) -> None:
        self.deck: Deck = None

        self.override_turn_enabled = False
        self.turn: int = 0

        self.dealer_index: int = 0

        self.small_blind_enabled: bool = None
        self.small_blind_bet: float = None
        self.small_blind_holder: int = None

        self.big_blind_enabled: bool = None
        self.big_blind_bet: float = None
        self.big_blind_holder: int = None

        self.ante_enabled: bool = None
        self.ante_amount: float = None

        self.raise_minimum_amount: float = None
        self.raise_maximum_amount: float = None

        self.hand_visibility_setting: HandVisibilitySetting = None

    def set_deck(self, deck: Deck) -> "GameSetting":
        self.deck = deck
        return self

    def enable_small_blind(self, amount: float) -> "GameSetting":
        self.small_blind_bet = amount
        self.small_blind_enabled = True
        return self

    def enable_big_blind(self, amount: float) -> "GameSetting":
        self.big_blind_bet = amount
        self.big_blind_enabled = True
        return self

    def set_dealer(self, holder: int) -> "GameSetting":
        self.dealer_index = holder
        return self

    def set_big_blind_holder(self, holder: int) -> "GameSetting":
        self.big_blind_holder = holder
        return self

    def set_small_blind_holder(self, holder: int) -> "GameSetting":
        self.small_blind_holder = holder
        return self

    def set_hand_visibility(self, setting: HandVisibilitySetting):
        self.hand_visibility_setting = setting
        return self

    def set_turn(self, turn: int) -> "GameSetting":
        self.turn = turn
        self.override_turn_enabled = True
        return self