from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Tuple

from src.game.deck.card import Card
from src.game.player.choose_action_info import ChooseActionInfo
from src.game.player.player_action import PlayerAction
from src.game.player.player_action_type import PlayerActionType
from src.game.setting.game_setting import GameSetting
from src.user.user import User

if TYPE_CHECKING:
    from src.game.pot import Pot
    from src.game.game import Game

class Player(ABC):

    def __init__(self, user: User, stake:float = 0) -> None:
        self.user = user
        self.stake = stake
        self.has_folded = False
        self.has_played_turn = False
        self.cards: List[Card] = []
        self.best_hand: Card = None 

    @property
    def is_all_in(self) -> bool:
        return self.user.money == 0

    def reset_player(self):
        self.stake = 0
        self.has_folded = False
        self.has_played_turn = False
        self.cards: List[Card] = []
        self.best_hand: Card = None 

    def _enough_money_for_min_bet_or_raise(self, settings: GameSetting, minimum_bet_money_required: float) -> bool:
        return not settings.bet_minimum_enabled or self.user.money >= minimum_bet_money_required

    def get_possible_actions(self, pot: Pot, game: Game) -> Tuple[List[PlayerActionType], ChooseActionInfo]:
        #Determine the possible actions
        call_amount: float = 0
        possible_actions: List[PlayerActionType] = []

        if not self.has_folded and not self.is_all_in:

            possible_actions.append(PlayerActionType.FOLD)
            stake = pot.get_stake_for_player(self)

            #In this case, there has been a bet this round already 
            # Big blind and Small blind during pre-flop counts as a bet
            # Antes do not count as bets
            if pot.current_highest_stake != 0:
                highest_stake_diff: float = pot.current_highest_stake - stake

                calling_is_all_in = highest_stake_diff >= self.user.money

                call_amount: float = min(highest_stake_diff, self.user.money)   

                #This happens at the start of the new rounds, i.e. when there is no bet to call on
                # if call_amount < 0:
                #     call_amount = 0

                minimum_raise_money_needed: float = pot.highest_bet_amount if game.settings.bet_minimum_enabled else call_amount

                can_raise_regardless_of_minimum: bool = (not calling_is_all_in
                            and any(map(lambda x: x != self and not x.is_all_in, pot.get_players_not_folded())))

                can_raise: bool = can_raise_regardless_of_minimum and self.user.money >= minimum_raise_money_needed

                if call_amount > 0 and not calling_is_all_in:
                    possible_actions.append(PlayerActionType.CALL)

                if call_amount == 0:
                    possible_actions.append(PlayerActionType.CHECK)

                if calling_is_all_in or can_raise_regardless_of_minimum:
                    possible_actions.append(PlayerActionType.ALL_IN)

                if can_raise:
                    possible_actions.append(PlayerActionType.RAISE)
            #In this case, nobody has bet thus far this round
            else:
                possible_actions.append(PlayerActionType.ALL_IN)
                possible_actions.append(PlayerActionType.CHECK)

                # You can only bet >= minimum bet requirement if it is enabled
                if self._enough_money_for_min_bet_or_raise(game.settings, pot.highest_bet_amount):
                    possible_actions.append(PlayerActionType.BET)

        return (possible_actions, ChooseActionInfo(call_amount, pot, game))

    @abstractmethod
    def choose_action(self, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo) -> PlayerAction:
        pass

        