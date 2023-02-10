from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Tuple

from src.game.deck.card import Card
from src.game.player.player_action import PlayerAction
from src.game.player.player_action_type import PlayerActionType
from src.user.user import User

if TYPE_CHECKING:
    from src.game.pot import Pot

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

    def get_possible_actions(self, pot: Pot) -> Tuple[List[PlayerActionType], float]:
        #Determine the possible actions
        call_amount: float = 0
        possible_actions: List[PlayerActionType] = []

        if not self.has_folded and not self.is_all_in:

            possible_actions.append(PlayerActionType.FOLD)
            stake = pot.get_stake_for_player(self)

            #The player can always choose to go all-in
            possible_actions.append(PlayerActionType.ALL_IN)

            #In this case, there has been a bet this round already (big blind and small blind during pre-flop counts as a bet)
            if 0 != pot.current_highest_stake:
                highest_stake_diff: float = pot.current_highest_stake - stake

                calling_is_all_in = highest_stake_diff >= self.user.money

                call_amount: float = min(highest_stake_diff, self.user.money)   

                #This happens at the start of the new rounds, i.e. when there is not bet to call on
                if call_amount < 0:
                    call_amount = 0

                can_raise: bool = not calling_is_all_in and any(map(lambda x: x != self and not x.is_all_in, pot.players))

                if call_amount > 0 and not calling_is_all_in:
                    possible_actions.append(PlayerActionType.CALL)

                if call_amount == 0:
                    possible_actions.append(PlayerActionType.CHECK)

                if can_raise:
                    possible_actions.append(PlayerActionType.RAISE)
            #In this case, nobody has bet thus far this round
            else:
                possible_actions.append(PlayerActionType.CHECK)
                
                #This is only possible for the big_blind_holder during the pre-flop, 
                #Where they can either choose to Check or to raise the big_blind
                if stake == pot.current_highest_stake:                    
                    possible_actions.append(PlayerActionType.RAISE)
                else:
                    possible_actions.append(PlayerActionType.BET)

        return (possible_actions, call_amount)

    @abstractmethod
    def choose_action(self, possible_actions: List[PlayerActionType], call_amount: float) -> PlayerAction:
        pass

        