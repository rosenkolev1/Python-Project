import random
from typing import List

from game.player.player_action import PlayerAction
from game.player.player_action_type import PlayerActionType
from game.player.player import Player

class ChooseActionFactory:
    
    @staticmethod
    def create_choose_action_predetermined(actions: List[(PlayerAction)]):
        sample = []
        
        def inner_mean(number):
            sample.append(number)
            return sum(sample) / len(sample)
            
        action_index = 0
            
        def mock_choose_action(self: Player, possible_actions: List[PlayerActionType], call_amount: float):
            nonlocal action_index     
            predetermined_action = actions[action_index]
            
            action_index += 1
            
            return predetermined_action
        
        return mock_choose_action

    @staticmethod
    def choose_action_always_raise_if_possible(self: Player, possible_actions: List[PlayerActionType], call_amount: float) -> PlayerActionType:
        action_type: PlayerActionType = None
        
        if PlayerActionType.RAISE in possible_actions:        
            action_type: PlayerActionType = PlayerActionType.RAISE
        elif PlayerActionType.BET in possible_actions:
            action_type: PlayerActionType = PlayerActionType.BET
        elif PlayerActionType.CALL in possible_actions:
            action_type: PlayerActionType = PlayerActionType.CALL

        if action_type == PlayerActionType.CALL:
            return PlayerAction(action_type, call_amount) 

        amount: float = min(call_amount + random.randint(1, 50), self.user.money)

        return PlayerAction(action_type, amount)