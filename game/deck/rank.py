from enum import Enum

class Rank(Enum):
    TWO = ["Two", 1]
    THREE = ["Three", 2]
    FOUR = ["Four", 3]
    FIVE = ["Five", 4]
    SIX = ["Six", 5]
    SEVEN = ["Seven", 6]
    EIGHT = ["Eight", 7]
    NINE = ["Nine", 8]
    TEN = ["Ten", 9]
    JACK = ["Jack", 10]
    QUEEN = ["Queen", 11]
    KING = ["King", 12]
    ACE = ["Ace", 13]

    @property
    def strength(self):
        return self.value[1]

    @property
    def name(self):
        return self.value[0]