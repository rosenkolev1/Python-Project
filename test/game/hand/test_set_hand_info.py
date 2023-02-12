
import pytest
from src.game.deck.card import Card
from src.game.deck.rank import Rank
from src.game.deck.suit import Suit
from src.game.hand.hand import Hand
from src.game.hand.hand_combination import HandCombination

def test_set_hand_info_straight():

    hand: Hand = Hand(
        [
            Card(Rank.SEVEN, Suit.DIAMONDS),
            Card(Rank.NINE, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.DIAMONDS),
            Card(Rank.TEN, Suit.DIAMONDS),
            Card(Rank.EIGHT, Suit.SPADES),
        ]
    )

    assert hand.combination == HandCombination.STRAIGHT
    assert hand.kickers_ranks == [
        Rank.SEVEN,
        Rank.EIGHT,
        Rank.NINE,
        Rank.TEN,
        Rank.JACK
    ]

def test_set_hand_info_high_ace_straight():

    hand: Hand = Hand(
        [
            Card(Rank.TEN, Suit.HEARTS),
            Card(Rank.KING, Suit.HEARTS),
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.QUEEN, Suit.CLUBS),
        ]
    )

    assert hand.combination == HandCombination.STRAIGHT
    assert hand.kickers_ranks == [
        Rank.TEN,
        Rank.JACK,
        Rank.QUEEN,
        Rank.KING,
        Rank.ACE
    ]

def test_set_hand_info_low_ace_straight():

    hand: Hand = Hand(
        [
            Card(Rank.THREE, Suit.CLUBS),
            Card(Rank.ACE, Suit.DIAMONDS),
            Card(Rank.FIVE, Suit.HEARTS),
            Card(Rank.TWO, Suit.SPADES),
            Card(Rank.FOUR, Suit.HEARTS)
        ]
    )

    assert hand.combination == HandCombination.STRAIGHT
    assert hand.kickers_ranks == [
        Rank.ACE,
        Rank.TWO,
        Rank.THREE,
        Rank.FOUR,
        Rank.FIVE
    ]

if __name__ == "__main__":
    retcode = pytest.main(["test/game/hand/test_set_hand_info.py"])