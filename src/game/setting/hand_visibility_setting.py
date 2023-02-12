from enum import Enum

"""
    Determines which players' 2 card hand will be shown in the console upon being dealt.
    
        - ALL - Will show all players' hands in the console.
        - NONE - Will not show any players' hands in the console
        - HUMANS_ONLY - Will only show the human player's (instance of HumanPlayer) hands in the console.
        - BOTS_ONLY - Will only show the bot player's (intance of BotPlayer) hands in the console
"""
class HandVisibilitySetting(Enum):
    ALL = 0,
    NONE = 1
    HUMANS_ONLY = 2,
    BOTS_ONLY = 3,
