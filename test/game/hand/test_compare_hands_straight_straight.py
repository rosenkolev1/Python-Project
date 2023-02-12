import pytest
from src.game.deck.card import Card
from src.game.deck.rank import Rank
from src.game.deck.suit import Suit

from src.game.hand.hand import Hand

def test_compare_hands_straight_straight_not_equal():
    first_hand: Hand = Hand(
        [
            Card(Rank.SEVEN, Suit.DIAMONDS),
            Card(Rank.NINE, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.DIAMONDS),
            Card(Rank.TEN, Suit.DIAMONDS),
            Card(Rank.EIGHT, Suit.SPADES),
        ]
    ) 

    second_hand: Hand = Hand(
        [
            Card(Rank.FIVE, Suit.HEARTS),
            Card(Rank.SIX, Suit.HEARTS),
            Card(Rank.SEVEN, Suit.HEARTS),
            Card(Rank.EIGHT, Suit.HEARTS),
            Card(Rank.NINE, Suit.CLUBS),
        ]
    )

    assert Hand.compare_hands(first_hand, second_hand) > 0
    assert Hand.compare_hands(second_hand, first_hand) < 0

def test_compare_hands_straight_straight_equal():
    first_hand: Hand = Hand(
        [
            Card(Rank.SEVEN, Suit.DIAMONDS),
            Card(Rank.NINE, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.DIAMONDS),
            Card(Rank.TEN, Suit.DIAMONDS),
            Card(Rank.EIGHT, Suit.SPADES),
        ]
    ) 

    second_hand: Hand = Hand(
        [
            Card(Rank.NINE, Suit.HEARTS),
            Card(Rank.TEN, Suit.HEARTS),
            Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.EIGHT, Suit.HEARTS),
            Card(Rank.SEVEN, Suit.CLUBS),
        ]
    )

    assert Hand.compare_hands(first_hand, second_hand) == 0
    assert Hand.compare_hands(second_hand, first_hand) == 0

def test_compare_hands_high_ace_straight_high_ace_straight():
    first_hand: Hand = Hand(
        [
            Card(Rank.KING, Suit.DIAMONDS),
            Card(Rank.QUEEN, Suit.DIAMONDS),
            Card(Rank.TEN, Suit.DIAMONDS),
            Card(Rank.ACE, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.SPADES),
        ]
    ) 

    second_hand: Hand = Hand(
        [
            Card(Rank.TEN, Suit.HEARTS),
            Card(Rank.KING, Suit.HEARTS),
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.QUEEN, Suit.CLUBS),
        ]
    )

    assert Hand.compare_hands(first_hand, second_hand) == 0
    assert Hand.compare_hands(second_hand, first_hand) == 0

def test_compare_hands_low_ace_straight_high_ace_straight():
    first_hand: Hand = Hand(
        [
            Card(Rank.THREE, Suit.DIAMONDS),
            Card(Rank.FOUR, Suit.DIAMONDS),
            Card(Rank.ACE, Suit.DIAMONDS),
            Card(Rank.FIVE, Suit.DIAMONDS),
            Card(Rank.TWO, Suit.SPADES),
        ]
    ) 

    second_hand: Hand = Hand(
        [
            Card(Rank.TEN, Suit.HEARTS),
            Card(Rank.KING, Suit.HEARTS),
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.QUEEN, Suit.CLUBS),
        ]
    )

    assert Hand.compare_hands(first_hand, second_hand) < 0
    assert Hand.compare_hands(second_hand, first_hand) > 0

def test_compare_hands_low_ace_straight_low_ace_straight():
    first_hand: Hand = Hand(
        [
            Card(Rank.THREE, Suit.DIAMONDS),
            Card(Rank.FOUR, Suit.DIAMONDS),
            Card(Rank.ACE, Suit.DIAMONDS),
            Card(Rank.FIVE, Suit.DIAMONDS),
            Card(Rank.TWO, Suit.SPADES),
        ]
    ) 

    second_hand: Hand = Hand(
        [
            Card(Rank.FIVE, Suit.HEARTS),
            Card(Rank.FOUR, Suit.HEARTS),
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.TWO, Suit.HEARTS),
            Card(Rank.THREE, Suit.CLUBS),
        ]
    )

    assert Hand.compare_hands(first_hand, second_hand) == 0
    assert Hand.compare_hands(second_hand, first_hand) == 0

def test_compare_hands_high_ace_straight_straight():
    first_hand: Hand = Hand(
        [
            Card(Rank.SEVEN, Suit.DIAMONDS),
            Card(Rank.NINE, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.DIAMONDS),
            Card(Rank.TEN, Suit.DIAMONDS),
            Card(Rank.EIGHT, Suit.SPADES),
        ]
    )

    
    second_hand: Hand = Hand(
        [
            Card(Rank.TEN, Suit.HEARTS),
            Card(Rank.KING, Suit.HEARTS),
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.QUEEN, Suit.CLUBS),
        ]
    )

    assert Hand.compare_hands(first_hand, second_hand) < 0
    assert Hand.compare_hands(second_hand, first_hand) > 0

def test_compare_hands_low_ace_straight_straight():
    first_hand: Hand = Hand(
        [
            Card(Rank.SEVEN, Suit.DIAMONDS),
            Card(Rank.NINE, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.DIAMONDS),
            Card(Rank.TEN, Suit.DIAMONDS),
            Card(Rank.EIGHT, Suit.SPADES),
        ]
    )

    
    second_hand: Hand = Hand(
        [
            Card(Rank.FIVE, Suit.HEARTS),
            Card(Rank.FOUR, Suit.HEARTS),
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.TWO, Suit.HEARTS),
            Card(Rank.THREE, Suit.CLUBS),
        ]
    )

    assert Hand.compare_hands(first_hand, second_hand) > 0
    assert Hand.compare_hands(second_hand, first_hand) < 0

if __name__ == "__main__":
    retcode = pytest.main(["test/game/hand/test_compare_hands_straight_straight.py"])