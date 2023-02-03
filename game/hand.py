import itertools
from typing import Dict, List, Set
from game.deck.card import Card
from game.deck.rank import Rank
from game.hand_combination import HandCombination

class Hand:

    def __init__(self, cards: List[Card]) -> None:
        self.cards: List[Card] = cards

        self.combination: HandCombination = None
        self.highest_card_rank: Rank = None
        self.highest_fours_card_rank: Rank = None
        self.highest_triple_card_rank: Rank = None  
        self.highest_first_pair_rank: Rank = None
        self.highest_second_pair_rank: Rank = None

        self.set_hand_info()

    @staticmethod
    def compare_hands(first, second):
        if first.combination.value > second.combination.value:
            return 1
        elif first.combination.value < second.combination.value:
            return -1
        else:
            combination: HandCombination = first.combination

            if combination == HandCombination.STRAIGHT_FLUSH or combination == HandCombination.STRAIGHT:
                return first.highest_card_rank - second.highest_card_rank

            elif combination == HandCombination.FOUR_OF_A_KIND:
                fours_comparison: int = first.highest_fours_card_rank - second.highest_fours_card_rank

                if fours_comparison == 0:
                    return first.highest_card_rank - second.highest_card_rank
                else:
                    return fours_comparison
                
            elif combination == HandCombination.FULL_HOUSE:
                triples_comparison: int = first.highest_triple_card_rank - second.highest_triple_card_rank

                if triples_comparison == 0:
                    return first.highest_first_pair_rank - second.highest_first_pair_rank
                else:
                    return fours_comparison

            elif combination == HandCombination.STRAIGHT or combination == HandCombination.FLUSH:
                return first.highest_first_pair_rank - second.highest_first_pair_rank

            elif combination == HandCombination.THREE_OF_A_KIND:
                triples_comparison: int = first.highest_triple_card_rank - second.highest_triple_card_rank

                if triples_comparison == 0:
                    return first.highest_card_rank - second.highest_card_rank
                else:
                    return fours_comparison

            elif combination == HandCombination.TWO_PAIR:    
                first_pair_comparison: int = first.highest_first_pair_rank - second.highest_first_pair_rank

                if first_pair_comparison == 0:
                    second_pair_comparison: int = first.highest_second_pair_rank - second.highest_second_pair_rank

                    if second_pair_comparison == 0:
                        return first.highest_card_rank - second.highest_card_rank
                    else:
                        return second_pair_comparison
                else:
                    return first_pair_comparison

            elif combination == HandCombination.PAIR:
                first_pair_comparison: int = first.highest_first_pair_rank - second.highest_first_pair_rank

                if first_pair_comparison == 0:
                    return first.highest_card_rank - second.highest_card_rank
                else:
                    return fours_comparison

            else:
                return first.highest_card_rank - second.highest_card_rank 

    def set_hand_info(self) -> None:
        ranks: List[Rank] = [card.rank for card in self.cards]
        ranks.sort(key=lambda r: r.value[1])

        ranks_set: Set[Rank] = set(ranks)

        #Check if there are repeating ranks of cards
        repeating_cards: bool = 5 == len(ranks_set) 

        is_straight: bool = not repeating_cards
                
        is_flush: bool = len(set([card.suit for card in self.cards])) == 5

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
            is_two_pair = 2 in ranks_counts.values() and len(set(ranks_counts.values())) == 2

            #Check for pair
            is_pair = 2 in ranks_counts.values()

        ranks_count_values_list = list(ranks_counts.values())

        if is_straight and is_flush:
            self.combination = HandCombination.STRAIGHT_FLUSH
            self.highest_card_rank = ranks[-1]

        elif is_four_of_a_kind:
            rank_index = ranks_count_values_list.index(4)

            self.combination = HandCombination.FOUR_OF_A_KIND
            self.highest_fours_card_rank = ranks[rank_index]
            self.highest_card_rank = ranks[1 if rank_index == 0 else 0]
            
        elif is_full_house:
            rank_index_triple = ranks_count_values_list.index(3)
            rank_index_pair = ranks_count_values_list.index(2)

            self.combination = HandCombination.FULL_HOUSE
            self.highest_triple_card_rank = ranks[rank_index_triple]
            self.highest_first_pair_rank = ranks[rank_index_pair]

        elif is_flush:
            self.combination = HandCombination.FLUSH
            self.highest_card_rank = ranks[-1]

        elif is_straight:
            self.combination = HandCombination.STRAIGHT
            self.highest_card_rank = ranks[-1]

        elif is_three_of_a_kind:
            rank_index_triple = ranks_count_values_list.index(3)

            self.combination = HandCombination.THREE_OF_A_KIND
            self.highest_triple_card_rank = ranks[rank_index_triple]
            self.highest_card_rank = ranks[1] if ranks[-1] == self.highest_triple_card_rank else ranks[-1]

        elif is_two_pair:            
            self.combination = HandCombination.TWO_PAIR

            for key in ranks_counts:
                if ranks_counts[key] == 2:
                    self.highest_first_pair_rank = key
                    if self.highest_second_pair_rank is None:
                        self.highest_second_pair_rank = key
                else:
                    self.highest_card_rank = key

        elif is_pair:
            self.combination = HandCombination.PAIR

            for key in ranks_counts:
                if ranks_counts[key] == 2:
                    self.highest_first_pair_rank = key
            
            self.highest_card_rank = ranks[-1]

        else:
            self.combination = HandCombination.HIGH_CARD
            self.highest_card_rank = ranks[-1]

    def __ranks_are_straight(self, ranks: List[Rank]):
        for i in range(1, 5):
            if ranks[i - 1].value[1] + 1 != ranks[i]:
                return False

        return True

    @staticmethod
    def get_all_5_card_hands(cards_list: List[Card]):
        hands: List[Hand] = [Hand(cards) for cards in itertools.combinations(cards_list, 5)]

        return hands

    def __repr__(self) -> str:
        return "|".join(self.cards.__repr__())
