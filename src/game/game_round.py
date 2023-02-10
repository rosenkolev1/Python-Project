from enum import Enum

class GameRound(Enum):
    Pre_Flop = "Pre-Flop"
    Flop = "Flop"
    Turn = "Turn"
    River = "River"
    Showdown = "Showdown"

    def next_round(self):
        values = [e for e in GameRound]

        cur_index = values.index(self)
        next_index = cur_index + 1

        if next_index == len(values):
            next_index = 0

        return values[next_index]
