
from src.game.deck.deck import Deck
from src.game.setting.hand_visibility_setting import HandVisibilitySetting
from src.game.setting.invalid_money_for_settings_exception import InvalidMoneyForSettingsException


class GameSetting:

    def __init__(self) -> None:
        self.deck: Deck = None

        # self.override_turn_enabled = False
        # self.turn: int = 0

        self.dealer_index: int = 0

        self.small_blind_enabled: bool = False
        self.small_blind_bet: float = None
        self.small_blind_holder: int = None

        self.big_blind_enabled: bool = False
        self.big_blind_bet: float = None
        self.big_blind_holder: int = None

        self.ante_enabled: bool = False
        self.ante_bet: float = None

        self.bet_minimum_enabled: bool = False
        self.bet_minimum_amount: float = None

        self.bet_maximum_enabled: bool = False
        self.bet_maximum_amount: float = None

        self.hand_visibility_setting: HandVisibilitySetting = None

    def return_self_wrapper(func):
        def wrap(*args, **kwargs):
            self = args[0]

            func(*args, **kwargs)

            return self

        return wrap

    @return_self_wrapper
    def enable_small_blind(self, amount: float, holder: int) -> "GameSetting":
        self.small_blind_bet = amount
        self.small_blind_holder = holder
        self.small_blind_enabled = True

    @return_self_wrapper
    def enable_big_blind(self, amount: float, holder: int) -> "GameSetting":
        self.big_blind_bet = amount
        self.big_blind_holder = holder
        self.big_blind_enabled = True

    @return_self_wrapper
    def enable_ante(self, amount: float) -> "GameSetting":
        self.ante_bet = amount
        self.ante_enabled = True

    @return_self_wrapper
    def enable_minimum_bet(self, amount: float) -> "GameSetting":
        self.bet_minimum_enabled = True
        self.bet_minimum_amount = amount

    @return_self_wrapper
    def enable_maximum_bet(self, amount: float) -> "GameSetting":
        self.bet_maximum_enabled = True
        self.bet_maximum_amount = amount

    @return_self_wrapper
    def disable_small_blind(self) -> "GameSetting":
        self.small_blind_enabled = False

    @return_self_wrapper
    def disable_big_blind(self) -> "GameSetting":
        self.big_blind_enabled = False

    @return_self_wrapper
    def disable_minimum_bet(self) -> "GameSetting":
        self.bet_minimum_enabled = False

    @return_self_wrapper
    def disable_maximum_bet(self) -> "GameSetting":
        self.bet_maximum_enabled = False

    @return_self_wrapper
    def disable_ante(self) -> "GameSetting":
        self.ante_enabled = False

    @return_self_wrapper
    def set_dealer(self, holder: int) -> "GameSetting":
        self.dealer_index = holder

    @return_self_wrapper
    def set_big_blind_bet(self, amount: int) -> "GameSetting":
        self.big_blind_bet = amount

    @return_self_wrapper
    def set_small_blind_bet(self, amount: int) -> "GameSetting":
        self.small_blind_bet = amount

    @return_self_wrapper
    def set_big_blind_holder(self, holder: int) -> "GameSetting":
        self.big_blind_holder = holder

    @return_self_wrapper
    def set_small_blind_holder(self, holder: int) -> "GameSetting":
        self.small_blind_holder = holder

    @return_self_wrapper
    def set_ante_bet(self, amount: int) -> "GameSetting":
        self.ante_bet = amount

    @return_self_wrapper
    def set_minimum_bet(self, amount: int) -> "GameSetting":
        self.bet_minimum_amount = amount

    @return_self_wrapper
    def set_maximum_bet(self, amount: int) -> "GameSetting":
        self.bet_maximum_amount = amount

    @return_self_wrapper
    def set_hand_visibility(self, setting: HandVisibilitySetting):
        self.hand_visibility_setting = setting

    @return_self_wrapper
    def set_deck(self, deck: Deck) -> "GameSetting":
        self.deck = deck

    def validate_money_for_game_settings(self, money: float) -> None:
        required_amount = 0

        if self.big_blind_enabled:
            required_amount += self.big_blind_bet
        elif self.small_blind_enabled:
            required_amount += self.small_blind_bet

        if self.ante_enabled:
            required_amount += self.ante_bet

        if money < required_amount or money <= 0:
            raise InvalidMoneyForSettingsException(
                "The player that you are trying to add has less money than required to enter the game!\n" + 
                f"At least {required_amount} is needed to enter the game!")