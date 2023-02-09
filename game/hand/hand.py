import itertools
from typing import Dict, List, Set

from game.deck.card import Card
from game.deck.rank import Rank
from game.hand.hand_combination import HandCombination


class Hand:

    def __init__(self, cards: List[Card]) -> None:
        self.cards: List[Card] = cards

        self.combination: HandCombination = None
        self.kickers_ranks: List[Rank] = []
        self.quads_rank: Rank = None
        self.triple_rank: Rank = None  
        self.high_pair_rank: Rank = None
        self.low_pair_rank: Rank = None

        self.set_hand_info()

    @staticmethod
    def compare_kickers(first: List[Card], second: List[Card]) -> int:
        for i in range(len(first) - 1, -1, -1):
            first_rank: Rank = first[i]
            second_rank: Rank = second[i]
            diff: int = first_rank.strength - second_rank.strength

            if diff !=0:
                return diff
        
        return 0


    @staticmethod
    def compare_hands(first: 'Hand', second: 'Hand'):
        if first.combination.value > second.combination.value:
            return 1
        elif first.combination.value < second.combination.value:
            return -1
        else:
            combination: HandCombination = first.combination

            if {combination == HandCombination.STRAIGHT_FLUSH or combination == HandCombination.STRAIGHT
                or combination == HandCombination.FLUSH}:

                return Hand.compare_kickers(first.kickers_ranks, second.kickers_ranks)

            elif combination == HandCombination.FOUR_OF_A_KIND:
                fours_comparison: int = first.quads_rank - second.quads_rank

                if fours_comparison == 0:
                    return Hand.compare_kickers(first.kickers_ranks, second.kickers_ranks)
                else:
                    return fours_comparison
                
            elif combination == HandCombination.FULL_HOUSE:
                triples_comparison: int = first.triple_rank - second.triple_rank

                if triples_comparison == 0:
                    return first.high_pair_rank - second.high_pair_rank
                else:
                    return triples_comparison

            elif combination == HandCombination.THREE_OF_A_KIND:
                triples_comparison: int = first.triple_rank - second.triple_rank

                if triples_comparison == 0:
                    return Hand.compare_kickers(first.kickers_ranks, second.kickers_ranks)
                else:
                    return triples_comparison

            elif combination == HandCombination.TWO_PAIR:    
                high_pair_comparison: int = first.high_pair_rank - second.high_pair_rank

                if high_pair_comparison == 0:
                    low_pair_comparison: int = first.low_pair_rank - second.low_pair_rank

                    if low_pair_comparison == 0:
                        return Hand.compare_kickers(first.kickers_ranks, second.kickers_ranks)
                    else:
                        return low_pair_comparison
                else:
                    return high_pair_comparison

            elif combination == HandCombination.PAIR:
                high_pair_comparison: int = first.high_pair_rank - second.high_pair_rank

                if high_pair_comparison == 0:
                    return Hand.compare_kickers(first.kickers_ranks, second.kickers_ranks)
                else:
                    return high_pair_comparison

            elif combination == HandCombination.HIGH_CARD:
                return Hand.compare_kickers(first.kickers_ranks, second.kickers_ranks)

        raise ValueError("No appropriate combination for these 2 hands has been found")

    def set_hand_info(self) -> None:
        ranks: List[Rank] = [card.rank for card in self.cards]
        ranks.sort(key=lambda r: r.strength)

        ranks_set: Set[Rank] = set(ranks)

        #Check if there are repeating ranks of cards
        repeating_cards: bool = 5 != len(ranks_set) 

        is_straight: bool = not repeating_cards
                
        is_flush: bool = len(set([card.suit for card in self.cards])) == 1

        is_four_of_a_kind: bool = False

        is_full_house: bool = False

        is_three_of_a_kind: bool = False

        is_two_pair: bool = False

        is_pair: bool = False

        ranks_counts: Dict[(Rank, int)] = {}

        if not repeating_cards:
            #Check for straight
            is_straight = self.__ranks_are_straight(ranks)
            
            #If the hand contains an ace, then try a different straight that starts from the ace 
            if not is_straight and Rank.ACE in ranks:
                ranks.insert(0, Rank.ACE)
                ranks.pop()

                is_straight = self.__ranks_are_straight(ranks)

                ranks.append(Rank.ACE)
                ranks.pop(0)
        else:
            for rank in ranks:
                if rank not in ranks_counts.keys():
                    ranks_counts[rank] = 1
                else:
                    ranks_counts[rank] += 1

            #Check for 4 of a kind
            is_four_of_a_kind = 4 in ranks_counts.values()

            #Check for a full-house
            is_full_house = 3 in ranks_counts.values() and 2 in ranks_counts.values()

            #Check for 3 of a kind
            is_three_of_a_kind = 3 in ranks_counts.values()

            #Check for 2 pairs
            is_two_pair = len([strength for (_, strength) in ranks_counts.items() if strength == 2]) == 2

            #Check for pair
            is_pair = 2 in ranks_counts.values()

        ranks_count_values_list = list(ranks_counts.values())

        if is_straight and is_flush:
            self.combination = HandCombination.STRAIGHT_FLUSH
            self.kickers_ranks = ranks

        elif is_four_of_a_kind:
            rank_index = ranks_count_values_list.index(4)

            self.combination = HandCombination.FOUR_OF_A_KIND
            self.quads_rank = ranks[rank_index]
            self.kickers_ranks = [ranks[1 if rank_index == 0 else 0]]
            
        elif is_full_house:
            rank_index_triple = ranks_count_values_list.index(3)
            rank_index_pair = ranks_count_values_list.index(2)

            self.combination = HandCombination.FULL_HOUSE
            self.triple_rank = ranks[rank_index_triple]
            self.high_pair_rank = ranks[rank_index_pair]

        elif is_flush:
            self.combination = HandCombination.FLUSH
            self.kickers_ranks = ranks

        elif is_straight:
            self.combination = HandCombination.STRAIGHT
            self.kickers_ranks = ranks

        elif is_three_of_a_kind:
            rank_index_triple = ranks_count_values_list.index(3)

            self.combination = HandCombination.THREE_OF_A_KIND
            self.triple_rank = ranks[rank_index_triple]
            self.kickers_ranks = [r for r in ranks if r != self.triple_rank]

        elif is_two_pair:            
            self.combination = HandCombination.TWO_PAIR

            for key in ranks_counts:
                if ranks_counts[key] == 2:
                    self.high_pair_rank = key
                    if self.low_pair_rank is None:
                        self.low_pair_rank = key
                else:
                    self.kickers_ranks = [key]

            if self.low_pair_rank.strength > self.high_pair_rank.strength:
                self.low_pair_rank, self.high_pair_rank = self.high_pair_rank, self.low_pair_rank

        elif is_pair:
            self.combination = HandCombination.PAIR

            not_pair_ranks: List[Rank] = []

            for key in ranks_counts:
                if ranks_counts[key] == 2:
                    self.high_pair_rank = key
                else:
                    not_pair_ranks.append(key)
            
            self.kickers_ranks = not_pair_ranks

        else:
            self.combination = HandCombination.HIGH_CARD
            self.kickers_ranks = ranks

    def __ranks_are_straight(self, ranks: List[Rank]):
        for i in range(1, 5):
            if ranks[i - 1].strength + 1 != ranks[i].strength:
                return False

        return True

    @staticmethod
    def get_all_5_card_hands(cards_list: List[Card]) -> List['Hand']:
        hands: List[Hand] = [Hand(cards) for cards in itertools.combinations(cards_list, 5)]

        return hands

    def __repr__(self) -> str:
        return "|".join(map(lambda c: c.__repr__(), self.cards))
