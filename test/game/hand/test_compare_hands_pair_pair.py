
import pytest
from src.game.deck.card import Card
from src.game.deck.rank import Rank
from src.game.deck.suit import Suit
from src.game.hand.hand import Hand

def test_compare_hands_pair_pair_stronger_pair():

    first_hand: Hand = Hand(
        [
            Card(Rank.SEVEN, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.QUEEN, Suit.SPADES),
            Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.JACK, Suit.SPADES),
        ]
    ) 

    second_hand: Hand = Hand(
        [
            Card(Rank.TEN, Suit.CLUBS),
            Card(Rank.JACK, Suit.CLUBS),
            Card(Rank.QUEEN, Suit.CLUBS),
            Card(Rank.SEVEN, Suit.DIAMONDS),
            Card(Rank.SEVEN, Suit.CLUBS),
        ]
    )

    assert Hand.compare_hands(first_hand, second_hand) > 0
    assert Hand.compare_hands(second_hand, first_hand) < 0

def test_compare_hands_pair_pair_stronger_kickers_first():

    first_hand: Hand = Hand(
        [
            Card(Rank.SEVEN, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.QUEEN, Suit.SPADES),
            Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.JACK, Suit.SPADES),
        ]
    ) 

    second_hand: Hand = Hand(
        [
            Card(Rank.SEVEN, Suit.CLUBS),
            Card(Rank.TEN, Suit.CLUBS),
            Card(Rank.ACE, Suit.CLUBS),
            Card(Rank.JACK, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.CLUBS),
        ]
    )

    assert Hand.compare_hands(first_hand, second_hand) < 0
    assert Hand.compare_hands(second_hand, first_hand) > 0

def test_compare_hands_pair_pair_stronger_kickers_second():

    first_hand: Hand = Hand(
        [
            Card(Rank.SEVEN, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.QUEEN, Suit.SPADES),
            Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.JACK, Suit.SPADES),
        ]
    ) 

    second_hand: Hand = Hand(
        [
            Card(Rank.SEVEN, Suit.CLUBS),
            Card(Rank.KING, Suit.CLUBS),
            Card(Rank.QUEEN, Suit.CLUBS),
            Card(Rank.JACK, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.CLUBS),
        ]
    )

    assert Hand.compare_hands(first_hand, second_hand) < 0
    assert Hand.compare_hands(second_hand, first_hand) > 0

def test_compare_hands_pair_pair_stronger_kickers_third():

    first_hand: Hand = Hand(
        [
            Card(Rank.SEVEN, Suit.SPADES),
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.QUEEN, Suit.SPADES),
            Card(Rank.JACK, Suit.HEARTS),
            Card(Rank.JACK, Suit.SPADES),
        ]
    ) 

    second_hand: Hand = Hand(
        [
            Card(Rank.EIGHT, Suit.CLUBS),
            Card(Rank.TEN, Suit.CLUBS),
            Card(Rank.QUEEN, Suit.CLUBS),
            Card(Rank.JACK, Suit.DIAMONDS),
            Card(Rank.JACK, Suit.CLUBS),
        ]
    )

    assert Hand.compare_hands(first_hand, second_hand) < 0
    assert Hand.compare_hands(second_hand, first_hand) > 0

def test_compare_hands_pair_pair_equal():

    first_hand: Hand = Hand(
        [
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.SEVEN, Suit.SPADES),
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.JACK, Suit.CLUBS),
            Card(Rank.JACK, Suit.SPADES),
        ]
    ) 

    second_hand: Hand = Hand(
        [
            Card(Rank.TEN, Suit.SPADES),
            Card(Rank.SEVEN, Suit.SPADES),
            Card(Rank.ACE, Suit.HEARTS),
            Card(Rank.JACK, Suit.CLUBS),
            Card(Rank.JACK, Suit.SPADES),
        ]
    )

    assert Hand.compare_hands(first_hand, second_hand) == 0
    assert Hand.compare_hands(second_hand, first_hand) == 0

if __name__ == "__main__":
    retcode = pytest.main(["test/game/hand/test_compare_hands_pair_pair.py"])