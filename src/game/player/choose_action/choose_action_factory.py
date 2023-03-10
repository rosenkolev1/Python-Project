import random
from typing import List
from src.game.player.choose_action.choose_action_info import ChooseActionInfo
from src.game.player.human_player import HumanPlayer

from src.game.player.player_action.player_action import PlayerAction
from src.game.player.player_action.player_action_type import PlayerActionType
from src.game.player.player import Player
from src.game.pot import Pot
from src.game.setting.game_setting import GameSetting
from src.game.user_interface.game_ui import GameUI

class ChooseActionFactory:

    @staticmethod
    def __create_action_command_string_human_player(action: PlayerAction) -> str:            
        predetermined_action_command_string = (
            {v: k for k, v in GameUI.PLAYER_COMMAND_ACTION_MAP.items()}[action.type]
        )

        predetermined_action_amount_string = str(action.amount) 

        predetermined_action_string = predetermined_action_command_string + " " + predetermined_action_amount_string

        return predetermined_action_string

    @staticmethod
    def __create_default_fake_receive_input_human_player(self: HumanPlayer, 
            possible_actions: List[PlayerActionType], 
            action_info: ChooseActionInfo,
            action_string: str) -> str:

        def fake_receive_input(*args, **kwargs) -> str:
                print(GameUI.choose_actions_command_prompt(self, possible_actions, action_info))
                return action_string

        return fake_receive_input

    """
        Creates a 'choose_action' with the list of given predetermined moves. 
        If one of these moves is illegal or otherwise fails the error handling checks, it will cause an infinite loop, so be wary. 
        
        If there are more moves than necessary given to the player, then these moves are ignored and the game continues as normal.
        (For example, specifying a fold action and then something else afterwards, obviously you cannot play after folding)
        
        If there are less moves than necessary, i.e. the player runs out of predetermined moves, then the default 'choose_action'
        method functionality is restored and any subsequent calls to it will trigger the player to have to enter the command manually
        from the console. This is useful if you want to partially simulate the player's actions up to a point 
    """
    @staticmethod
    def create_choose_action_predetermined_human_player(actions: List[(PlayerAction)]):
        action_index = 0
            
        def mock_choose_action(self: HumanPlayer, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo):
            nonlocal action_index     

            #If we have run out of predetermined moves, then give back control to the user
            if action_index >= len(actions):
                self.receive_input = self.original_receive_input

                return self.original_choose_action(possible_actions, action_info)

            predetermined_action = actions[action_index]
            predetermined_action_string = ChooseActionFactory.__create_action_command_string_human_player(predetermined_action)

            action_index += 1

            #Replace the receive_input function so that it gives us the appropriate preset input
            self.receive_input = ChooseActionFactory.__create_default_fake_receive_input_human_player(
                self, possible_actions, action_info,
                predetermined_action_string
            )

            #Call the original choose_action function which now has the fake_receive_input
            return self.original_choose_action(possible_actions, action_info)
        
        return mock_choose_action

    
    """
        Creates a 'choose_action' which will randomly select moves, with the exception of the specified excluded actions.
        If there are no legal actions for the player to make, then it will try to play the provided default action!
        If that action is also illegal, then this will cause an infinite loop.
        
        The All-In action can be forced if the raise action is legal and the amount to raise is >= user's money, regardless of
        whether or not it is in the excluded actions list! 
    """
    @staticmethod
    def create_choose_action_always_random_human_player(excluding_actions: List[PlayerActionType] = [], 
                                           back_up_action: PlayerActionType = PlayerActionType.FOLD) -> PlayerActionType:
        
        def mock_choose_action(self: HumanPlayer, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo):
            #Filter available actions
            possible_actions_filtered: List[PlayerActionType] = list(filter(lambda x: x not in excluding_actions, possible_actions))

            #Choose randomly
            action_type: PlayerActionType = None

            if len(possible_actions_filtered) == 0:
                action_type = back_up_action
            else:
                action_type = possible_actions_filtered[random.randint(0, len(possible_actions_filtered) - 1)] 

            min_bet_amount: float = action_info.pot.highest_bet_amount if action_info.game.settings.bet_minimum_enabled else 1

            amount: float = min(action_info.call_amount + (round(random.random() % 50 + min_bet_amount, 2)), self.user.money)

            if action_type == PlayerActionType.CALL:
                amount = action_info.call_amount
            elif action_type == PlayerActionType.ALL_IN:
                amount = self.user.money
            # Force an all-in if the action is a raise and the amount is equal to all the remaining money of the user
            # Regardless of whether or not the All-In is an excluded action 
            elif action_type == PlayerActionType.RAISE and amount == self.user.money:
                return PlayerAction(PlayerActionType.ALL_IN, amount)

            action = PlayerAction(action_type, amount)
            action_string = ChooseActionFactory.__create_action_command_string_human_player(action)

            # Replace the receive_input function so that it gives us the appropriate preset input
            self.receive_input = ChooseActionFactory.__create_default_fake_receive_input_human_player(
                self, possible_actions, action_info,
                action_string
            )

            return self.original_choose_action(possible_actions, action_info)

        return mock_choose_action

    """
        Creates a 'choose_action' with the list of given predetermined moves. 
        If one of these moves is illegal or otherwise fails the error handling checks, it will cause an infinite loop, so be wary. 
        
        If there are more moves than necessary given to the player, then these moves are ignored and the game continues as normal.
        (For example, specifying a fold action and then something else afterwards, obviously you cannot play after folding)
        
        If there are less moves than necessary, i.e. the player runs out of predetermined moves, then an error will occur! 
    """
    @staticmethod
    def create_choose_action_predetermined(actions: List[(PlayerAction)]):
        action_index = 0
            
        def mock_choose_action(self: Player, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo):
            nonlocal action_index     
            predetermined_action = actions[action_index]
            
            amount: float = predetermined_action.amount

            if predetermined_action.type == PlayerActionType.RAISE:
                amount += action_info.call_amount

            if predetermined_action.type == PlayerActionType.CALL:
                amount = action_info.call_amount

            action_index += 1
            
            return PlayerAction(predetermined_action.type, amount)
        
        return mock_choose_action

    """
        Creates a 'choose_action' which will randomly select moves, with the exception of the specified excluded actions.
        If there are no legal actions for the player to make, then it will try to play the provided default action!
        If that action is also illegal, then this will cause an infinite loop.
        
        The All-In action can be forced if the raise action is legal and the amount to raise is >= user's money, regardless of
        whether or not it is in the excluded actions list! 
    """
    @staticmethod
    def create_choose_action_always_random(excluding_actions: List[PlayerActionType] = [], 
                                           back_up_action: PlayerActionType = PlayerActionType.FOLD) -> PlayerActionType:
        
        def mock_choose_action(self: Player, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo):
            #Filter available actions
            possible_actions_filtered: List[PlayerActionType] = list(filter(lambda x: x not in excluding_actions, possible_actions))

            #Choose randomly
            action_type: PlayerActionType = None

            if len(possible_actions_filtered) == 0:
                action_type = back_up_action
            else:
                action_type = possible_actions_filtered[random.randint(0, len(possible_actions_filtered) - 1)] 

            min_bet_amount: float = action_info.pot.highest_bet_amount if action_info.game.settings.bet_minimum_enabled else 1

            amount: float = min(action_info.call_amount + (round(random.random() % 50 + min_bet_amount, 2)), self.user.money)

            if action_type == PlayerActionType.CALL:
                amount = action_info.call_amount
            elif action_type == PlayerActionType.ALL_IN:
                amount = self.user.money
            #Force an all-in if the action is a raise and the amount is equal to all the remaining money of the user
            elif action_type == PlayerActionType.RAISE and amount == self.user.money:
                return PlayerAction(PlayerActionType.ALL_IN, amount)

            return PlayerAction(action_type, amount)

        return mock_choose_action


    """
        Creates a 'choose_action' which will try to raise a random amount at all times.
        If raising is not possible, but betting is, then it will bet instead.
        If raising and betting is not possible, it will call instead.
        If raising, betting or calling is not possible, it will go all-in instead.
        
        If it tries raising an amount >= the users' money, then it will go all-in instead.
    """
    @staticmethod
    def create_choose_action_always_raise_if_possible() -> PlayerActionType:
        
        def mock_choose_action(self: Player, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo):
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
                return PlayerAction(action_type, action_info.call_amount)
            elif action_type == PlayerActionType.ALL_IN:
                return PlayerAction(action_type, self.user.money)
    
            min_bet_amount = action_info.pot.highest_bet_amount if action_info.game.settings.bet_minimum_enabled else 1

            amount: float = round(min(action_info.call_amount + (random.random() % 50 + min_bet_amount), self.user.money), 2)

            if amount == self.user.money:
                action_type = PlayerActionType.ALL_IN

            return PlayerAction(action_type, amount)

        return mock_choose_action