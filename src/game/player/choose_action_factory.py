import random
from typing import List
from src.game.player.human_player import HumanPlayer

from src.game.player.player_action import PlayerAction
from src.game.player.player_action_type import PlayerActionType
from src.game.player.player import Player
from src.game.user_interface.game_ui import GameUI

class ChooseActionFactory:

    @staticmethod
    def create_choose_action_predetermined_human_player(actions: List[(PlayerAction)]):
        action_index = 0
            
        def mock_choose_action(self: HumanPlayer, possible_actions: List[PlayerActionType], call_amount: float,
                               original_choose_action, original_receive_input):
            nonlocal action_index     

            #If we have run out of predetermined moves, then give back control to the user
            if action_index >= len(actions):
                self.receive_input = original_receive_input

                return original_choose_action(possible_actions, call_amount)

            predetermined_action = actions[action_index]
            
            predetermined_action_command_string = (
                {v: k for k, v in GameUI.PLAYER_COMMAND_ACTION_MAP.items()}[predetermined_action.type]
            )

            predetermined_action_amount_string = str(predetermined_action.amount) 

            predetermined_action_string = predetermined_action_command_string + " " + predetermined_action_amount_string

            action_index += 1

            def fake_receive_input(*args, **kwargs) -> str:
                print(GameUI.choose_actions_command_prompt(self, possible_actions, call_amount))
                return predetermined_action_string

            #Replace the receive_input function so that it gives us the appropriate preset input
            self.receive_input = fake_receive_input

            #Call the original choose_action function which now has the fake_receive_input
            return original_choose_action(possible_actions, call_amount)
        
        return mock_choose_action

    @staticmethod
    def create_choose_action_predetermined(actions: List[(PlayerAction)]):
        action_index = 0
            
        def mock_choose_action(self: Player, possible_actions: List[PlayerActionType], call_amount: float):
            nonlocal action_index     
            predetermined_action = actions[action_index]
            
            amount: float = predetermined_action.amount

            if predetermined_action.type == PlayerActionType.RAISE:
                amount += call_amount

            action_index += 1
            
            return PlayerAction(predetermined_action.type, amount)
        
        return mock_choose_action

    @staticmethod
    def choose_action_always_random(self: Player, possible_actions: List[PlayerActionType], call_amount: float) -> PlayerActionType:
        #Choose randomly
        action_type: PlayerActionType = possible_actions[random.randint(0, len(possible_actions) - 1)]
        amount: float = min(call_amount + random.randint(1, 50), self.user.money)

        if action_type == PlayerActionType.CALL:
            amount = call_amount
        elif action_type == PlayerActionType.ALL_IN:
            amount = self.user.money

        return PlayerAction(action_type, amount)

    @staticmethod
    def choose_action_always_raise_if_possible(self: Player, possible_actions: List[PlayerActionType], call_amount: float) -> PlayerActionType:
        action_type: PlayerActionType = None
        
        if PlayerActionType.RAISE in possible_actions:        
            action_type = PlayerActionType.RAISE
        elif PlayerActionType.BET in possible_actions:
            action_type = PlayerActionType.BET
        elif PlayerActionType.CALL in possible_actions:
            action_type = PlayerActionType.CALL
        elif PlayerActionType.BET in possible_actions:
            action_type = PlayerActionType.ALL_IN

        if action_type == PlayerActionType.CALL:
            return PlayerAction(action_type, call_amount)
        elif action_type == PlayerActionType.ALL_IN:
            return PlayerAction(action_type, self.user.money)
 
        amount: float = min(call_amount + random.randint(1, 50), self.user.money)

        if amount == self.user.money:
            action_type = PlayerActionType.ALL_IN

        return PlayerAction(action_type, amount)