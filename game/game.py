import functools
from typing import List, Tuple, Union
from game.deck.card import Card

from game.deck.deck import Deck
from game.hand import Hand
from game.player_action import PlayerAction
from game.player_action_type import PlayerActionType

from game.pot import Pot
from game.game_round import GameRound
from game.user import User
from game.pot_player import PotPlayer


class Game:

    def __init__(self, small_blind_bet: float, big_blind_bet: float) -> None:
        self.deck: Deck = Deck()
        self.__players: List[PotPlayer] = []
        self.round: GameRound = GameRound.Pre_Flop
        # self.allowed_actions: List[PlayerActionType] = []

        self.community_cards: List[Card] = []

        self.turn: int = 0
        self.dealer_index: int = -1

        self.pots: List[Pot] = []
        self.current_pot_index: int = 0 

        self.small_blind_bet: float = small_blind_bet
        self.small_blind_holder: int = 0

        self.big_blind_bet: float = big_blind_bet
        self.big_blind_holder: int = 1 

    def start_game(self):
        self.round = GameRound.Pre_Flop

        self.next_dealer()
        self.next_small_blind_holder()
        self.next_big_blind_holder()

        self.pots.clear()

        main_pot: Pot = Pot()

        main_pot.place_bet(self.small_blind_player, self.small_blind_bet)
        main_pot.place_bet(self.big_blind_player, self.big_blind_bet)

        self.pots.append(main_pot)
        self.current_pot_index = 0

        if self.two_player_game:
            self.big_blind_holder = 0
        else:
            self.big_blind_holder = 2

        print(f"The big blind player is: {self.big_blind_player.user.name}")
        print(f"The small blind player is: {self.small_blind_player.user.name}\n")

        #Debug
        print(f"Game is starting...\n\n")
            
        #Shuffle deck
        self.deck.shuffle_deck()

        self.play_round()

        #Debug
        print(f"Game has ended...\n\n")

    def add_player(self, user: User) -> None:
        if user.money < self.big_blind_bet:
            raise ValueError("The player that you are trying to add has less money than required to enter the game!")

        self.players.append(PotPlayer(user))
        self.two_player_game = len(self.players) == 2

    def __next_index(self, indexer: int) -> int:
        indexer += 1

        if indexer == len(self.players):
            indexer = 0

        return indexer

    def next_pot(self) -> None:
        self.current_pot_index = self.__next_index(self.current_pot_index)

    def next_big_blind_holder(self) -> None:
        self.big_blind_holder = self.__next_index(self.big_blind_holder)

    def next_small_blind_holder(self) -> None:
        self.small_blind_holder = self.__next_index(self.small_blind_holder)

    def next_dealer(self) -> None:
        self.dealer_index = self.__next_index(self.dealer_index)

    def next_turn(self) -> None:
        self.turn = self.__next_index(self.turn)

    def start_round(self): 
        #Debug
        print(f"{self.round} is starting...\n")

        #Set the current highest stake for the current pot for this round to 0 to reset it
        if (self.round != GameRound.Pre_Flop):
            self.current_pot.current_highest_stake = 0

        #Reset the has_played status for all the players who have not folded
        for player in self.current_pot.get_players_not_folded():
            player.has_played_turn = False

        if self.round == GameRound.Pre_Flop:
            self.turn = self.big_blind_holder
        else:
            self.turn = self.dealer_index    

        if self.round == GameRound.Pre_Flop:
            #Give out 2 cards to each player
            for player in self.players:
                player.cards.append(self.deck.cards.pop())
                player.cards.append(self.deck.cards.pop())

                #Debug
                print(f"Player: {player.user.name} has drawn cards: {player.cards}\n")
        else:
            self.deck.cards.pop()

        if self.round == GameRound.Flop:
            for i in range(0, 3):
                self.community_cards.append(self.deck.cards.pop())

            #Debug
            print(f"During the flop round these cards were drawn: {self.community_cards}")
        elif self.round == GameRound.Turn or self.round == GameRound.River:
            self.community_cards.append(self.deck.cards.pop())

            #Debug
            print(f"During the turn(4th street) round or the River round, these were the cards: {self.community_cards}")

        self.next_turn()

    def play_showdown(self):
        #Debug
        print(f"Showdown is starting...\n\n")

        players_not_folded = self.pots[0].get_players_not_folded()

        #Set best hand for each player
        for player in players_not_folded:
            player_cards: List[Card] = self.community_cards.copy()
            for card in player.cards.copy():
                player_cards.append(card)

            possible_hands = Hand.get_all_5_card_hands(player_cards)

            possible_hands_sorted = sorted(possible_hands, key=functools.cmp_to_key(Hand.compare_hands))

            player.best_hand = possible_hands_sorted[-1]

        #Order the players by their hand strengths
        ordered_players: List[PotPlayer] = sorted(players_not_folded, key=lambda p: functools.cmp_to_key(Hand.compare_hands)(p.best_hand))

        # #Debug
        # for player in players_not_folded:
        #     print(f"Player:{player.user.name} has hand {player.best_hand}")

        #Debug
        print(f"Community cards: {self.community_cards}\n")

        for player in ordered_players:
            print(f"Player: {player.user.name}\nCards: {player.cards}\nBest Hand: {player.best_hand}\nCombination:{player.best_hand.combination.name}\n")

        #TODO: Add functionality for side pots
        winning_player: PotPlayer = ordered_players[-1]
        total_winnings = self.current_pot.total_money
        
        winning_player.user.money += total_winnings

        #Debug
        print(f"Player: {winning_player.user.name} has won the round and claimed {total_winnings}$ from the pot")          

    def get_possible_actions(self, player, pot) -> Tuple[List[PlayerActionType], float]:
        #Determine the possible actions
        call_amount: float = 0
        possible_actions: List[PlayerActionType] = []

        if not player.has_folded and not player.is_all_in:

            possible_actions.append(PlayerActionType.FOLD)
            stake = pot.get_stake_for_player(player)

            #In this case, there has been a bet this round already
            if stake != pot.current_highest_stake:
                possible_actions.append(PlayerActionType.CALL)

                call_amount = min(pot.current_highest_stake - stake, player.user.money)

                can_raise: bool = call_amount <= player.user.money

                if can_raise:
                    possible_actions.append(PlayerActionType.RAISE)
            #In this case, nobody has bet thus far this round
            else:
                possible_actions.append(PlayerActionType.CHECK)
                possible_actions.append(PlayerActionType.BET)

        return (possible_actions, call_amount)

    def play_turn(self) -> bool:
        player = self.current_player
        pot = self.current_pot

        if player.is_all_in:
            #Debug
            print(f"Player: {player.user.name} is all in with amount {pot.get_stake_for_player(player)}! Their current balance is {player.user.money}\n")
        else:
            #Determine the possible actions
            possible_actions, call_amount = self.get_possible_actions(player, pot)

            #TODO: Change this to be polymorphic for different possible players
            action: PlayerAction = player.choose_action(possible_actions, call_amount)

            if action.type == PlayerActionType.FOLD:
                player.has_folded = True
            elif action.type == PlayerActionType.RAISE or action.type == PlayerActionType.BET:
                #For each player that has not folded, reset their has_played_turn state
                for other_player in self.players:
                    if not other_player.has_folded:
                        other_player.has_played_turn = False

            if action.type != PlayerActionType.FOLD and action.type != PlayerActionType.CHECK:
                pot.place_bet(player, action.amount)

            #Debug
            print(f"Player: {player.user.name} is doing {action.type} with amount {action.amount}! Their current balance is {player.user.money}\n")

        player.has_played_turn = True
        
        # bet_is_matched_all = pot.bet_is_matched_all()

        players_not_played: List[PotPlayer] = pot.get_players_not_played()
        players_not_folded: List[PotPlayer] = pot.get_players_not_folded()

        if len(players_not_played) == 0:
            return True
        elif len(players_not_folded) == 1 and self.round == GameRound.Pre_Flop:
            return True
        # if bet_is_matched_all and self.round != GameRound.Pre_Flop:
        #     return True
        # elif bet_is_matched_all and self.round == GameRound.Pre_Flop and len(pot.get_players_not_played()) == 1:
        #     return True
        # elif bet_is_matched_all and self.round == GameRound.Pre_Flop and pot.current_highest_stake == self.big_blind_bet and player == self.big_blind_player:
        #     return True

        self.next_turn()
        return False       

    def payout_on_fold(self) -> None:
        winning_player: PotPlayer = self.current_pot.get_players_not_folded()[0]

        #TODO: Add support for side pots
        total_winnings = self.current_pot.total_money
        
        #Debug
        print(f"Player: {winning_player.user.name} has won the hand and claimed {total_winnings}$ from the pot!\n")
        winning_player.user.money += total_winnings

    def play_round(self) -> None:
        self.start_round()

        while True:
            round_over = self.play_turn()

            if round_over:
                self.round = self.round.next_round()

            if round_over and self.round == GameRound.Showdown:
                self.play_showdown()
                break
            elif round_over and len(self.current_pot.get_players_not_folded()) == 1:
                self.payout_on_fold()
                break
            elif round_over:
                self.play_round()
                break

    @property
    def is_two_player_game(self) -> bool:
        return len(self.players) == 2

    @property
    def current_pot(self) -> Pot:
        return self.pots[self.current_pot_index]

    @property
    def current_player(self) -> PotPlayer:
        return self.players[self.turn]

    @property
    def big_blind_player(self) -> PotPlayer:
        return self.players[self.big_blind_holder]

    @property
    def small_blind_player(self) -> PotPlayer:
        return self.players[self.small_blind_holder]
        
    @property
    def players(self) -> List[PotPlayer]:
        return self.__players

        
            