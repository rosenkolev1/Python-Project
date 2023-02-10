from enum import Enum

class PlayerActionType(Enum):
    FOLD = "Fold"
    CHECK = "Check"
    CALL = "Call"
    BET = "Bet"
    RAISE = "Raise"
    ALL_IN = "All-in"