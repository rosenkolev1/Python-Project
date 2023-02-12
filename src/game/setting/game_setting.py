
from src.game.deck.deck import Deck
from src.game.setting.hand_visibility_setting import HandVisibilitySetting
from src.game.setting.invalid_money_for_settings_exception import InvalidMoneyForSettingsException

"""
    The GameSetting class contains variables which determine various settings for the game:
        - deck - The Deck with which the game will be played
        
        - dealer_index - The index of the player who holds the so-called 'dealer button', i.e. the dealer. 
            In casinos, he doesn't actually deal the cards, but the 'dealer button' is still used.  
            The rounds typically start from the first player after the dealer, except for the Pre-Flop round
            (but only if there are small or big blinds)
        
        - small_blind_enabled - Determines whether or not there will be a small blind in the game
        - small_blind_bet - The amount of the small blind bet.
        - small_blind_holder - The index of the player who will have to pay the small blind in the game. 
            Typically that is the person right after the dealer!
            
        - big_blind_enabled - Determines whether or not there will be a big blind in the game
        - big_blind_bet - The amount of the big blind bet.
        - big_blind_holder - The index of the player who will have to pay the big blind in the game. 
            Typically that is the person right after the one who has to pay the small blind!
        
        - ante_enabled - Determines whether or not there will be antes in the game
        - ante_bet - The amount of the ante bet.
        
        - bet_maximum_enabled - Determines whether or not there will be a minimum amount by which to bet or raise
            Enabling this makes the game a typical No Limit game. Read https://en.wikipedia.org/wiki/Betting_in_poker#No_limit for info.
        - bet_minimum_amount - The min amount of the opening bet.
        
        - hand_visibility_setting - Determines which players' 2 card hand will be shown in the console upon being dealt.
            Check the 'hand_visibility_setting.py' module for more info!
"""
class GameSetting:

    def __init__(self) -> None:
        self.deck: Deck = None

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

        # These do not work because I have not implemented them
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
                f"At least {required_amount}$ is needed to enter the game!")