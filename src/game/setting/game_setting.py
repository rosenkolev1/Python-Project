
from src.game.deck.deck import Deck
from src.game.setting.hand_visibility_setting import HandVisibilitySetting
from src.game.setting.invalid_money_for_settings_exception import InvalidMoneyForSettingsException


class GameSetting:

    def __init__(self) -> None:
        self.deck: Deck = None

        self.override_turn_enabled = False
        # self.turn: int = 0

        self.dealer_index: int = 0

        self.small_blind_enabled: bool = None
        self.small_blind_bet: float = None
        self.small_blind_holder: int = None

        self.big_blind_enabled: bool = None
        self.big_blind_bet: float = None
        self.big_blind_holder: int = None

        self.ante_enabled: bool = None
        self.ante_bet: float = None

        self.bet_minimum_amount: float = None
        self.bet_maximum_amount: float = None

        self.hand_visibility_setting: HandVisibilitySetting = None

    def set_deck(self, deck: Deck) -> "GameSetting":
        self.deck = deck
        return self

    def enable_small_blind(self, amount: float, holder: int) -> "GameSetting":
        self.small_blind_bet = amount
        self.small_blind_holder = holder
        self.small_blind_enabled = True
        return self

    def enable_big_blind(self, amount: float, holder: int) -> "GameSetting":
        self.big_blind_bet = amount
        self.big_blind_holder = holder
        self.big_blind_enabled = True
        return self

    def enable_ante(self, amount: float) -> "GameSetting":
        self.ante_bet = amount
        self.ante_enabled = True
        return self

    def set_dealer(self, holder: int) -> "GameSetting":
        self.dealer_index = holder
        return self

    def set_big_blind_bet(self, amount: int) -> "GameSetting":
        self.big_blind_bet = amount
        return self

    def set_small_blind_bet(self, amount: int) -> "GameSetting":
        self.small_blind_bet = amount
        return self

    def set_big_blind_holder(self, holder: int) -> "GameSetting":
        self.big_blind_holder = holder
        return self

    def set_small_blind_holder(self, holder: int) -> "GameSetting":
        self.small_blind_holder = holder
        return self

    def set_ante_bet(self, amount: int) -> "GameSetting":
        self.ante_bet = amount
        return self

    def set_hand_visibility(self, setting: HandVisibilitySetting):
        self.hand_visibility_setting = setting
        return self

    def _validate_money_for_game_settings(self, money: float) -> None:
        required_amount = 0

        if self.big_blind_enabled:
            required_amount += self.big_blind_bet
        elif self.small_blind_enabled:
            required_amount += self.small_blind_bet

        if self.ante_enabled:
            required_amount += self.ante_bet

        if money < required_amount:
            raise InvalidMoneyForSettingsException(
                "The player that you are trying to add has less money than required to enter the game!\n" + 
                f"At least {required_amount} is needed to enter the game!")