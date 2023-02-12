from enum import Enum

class Rank(Enum):
    TWO = ["Two", 2]
    THREE = ["Three", 3]
    FOUR = ["Four", 4]
    FIVE = ["Five", 5]
    SIX = ["Six", 6]
    SEVEN = ["Seven", 7]
    EIGHT = ["Eight", 8]
    NINE = ["Nine", 9]
    TEN = ["Ten", 10]
    JACK = ["Jack", 11]
    QUEEN = ["Queen", 12]
    KING = ["King", 13]
    ACE = ["Ace", 14]

    @property
    def strength(self):
        return self.value[1]

    @property
    def name(self):
        return self.value[0]