
from typing import List

import pytest
from src.game.deck.card import Card
from src.game.deck.rank import Rank
from src.game.deck.suit import Suit
from src.game.hand.hand import Hand

def test_compare_kickers_first_diff():
    first_hand: List[Rank] = [
            Rank.SEVEN,
            Rank.TEN,
            Rank.JACK, 
            Rank.QUEEN,
            Rank.KING, 
        ]

    second_hand: List[Card] = [
            Rank.SEVEN,
            Rank.TEN,  
            Rank.JACK, 
            Rank.QUEEN,
            Rank.ACE,  
        ]

    assert Hand.compare_kickers(first_hand, second_hand) < 0
    assert Hand.compare_kickers(second_hand, first_hand) > 0

def test_compare_kickers_second_diff():
    first_hand: List[Card] = [
            Rank.SEVEN,
            Rank.TEN,
            Rank.JACK,
            Rank.NINE,
            Rank.ACE
        ]

    second_hand: List[Card] = [
            Rank.SEVEN,
            Rank.TEN,  
            Rank.JACK, 
            Rank.QUEEN,
            Rank.ACE,  
        ]

    assert Hand.compare_kickers(first_hand, second_hand) < 0
    assert Hand.compare_kickers(second_hand, first_hand) > 0

def test_compare_kickers_third_diff():
    first_hand: List[Card] = [
            Rank.SEVEN,
            Rank.TEN,  
            Rank.NINE, 
            Rank.QUEEN,
            Rank.ACE,  
        ]

    second_hand: List[Card] = [
            Rank.SEVEN,
            Rank.TEN,  
            Rank.JACK, 
            Rank.QUEEN,
            Rank.ACE,  
        ]

    assert Hand.compare_kickers(first_hand, second_hand) < 0
    assert Hand.compare_kickers(second_hand, first_hand) > 0

def test_compare_kickers_fourth_diff():
    first_hand: List[Card] = [
            Rank.SEVEN,
            Rank.NINE, 
            Rank.JACK, 
            Rank.QUEEN,
            Rank.ACE,  
        ]

    second_hand: List[Card] = [
            Rank.SEVEN,
            Rank.TEN,  
            Rank.JACK, 
            Rank.QUEEN,
            Rank.ACE,  
        ]

    assert Hand.compare_kickers(first_hand, second_hand) < 0
    assert Hand.compare_kickers(second_hand, first_hand) > 0

def test_compare_kickers_fifth_diff():
    first_hand: List[Card] = [
            Rank.SIX,  
            Rank.TEN,  
            Rank.JACK, 
            Rank.QUEEN,
            Rank.ACE,  
        ]

    second_hand: List[Card] = [
            Rank.SEVEN,
            Rank.TEN,  
            Rank.JACK, 
            Rank.QUEEN,
            Rank.ACE,  
        ]

    assert Hand.compare_kickers(first_hand, second_hand) < 0
    assert Hand.compare_kickers(second_hand, first_hand) > 0

def test_compare_kickers_equal():
    first_hand: List[Card] = [
            Rank.SEVEN,
            Rank.TEN,  
            Rank.JACK, 
            Rank.QUEEN,
            Rank.ACE,  
        ]

    second_hand: List[Card] = [
            Rank.SEVEN,
            Rank.TEN,  
            Rank.JACK, 
            Rank.QUEEN,
            Rank.ACE,  
        ]

    assert Hand.compare_kickers(first_hand, second_hand) == 0
    assert Hand.compare_kickers(second_hand, first_hand) == 0

if __name__ == "__main__":
    retcode = pytest.main(["test/game/hand/test_compare_kickers.py"])