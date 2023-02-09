import functools
from typing import List, Tuple
from multipledispatch import dispatch

from game.deck.card import Card
from game.hand.hand import Hand
from game.player.player_action import PlayerAction
from game.player.player_action_type import PlayerActionType

from game.player.player import Player
from game.deck.deck import Deck
from game.game_round import GameRound
from game.pot import Pot
from game.user import User

class Game:

    def __init__(self, deck: Deck, small_blind_bet: float, big_blind_bet: float) -> None:
        self.deck: Deck = deck
        self.__players: List[Player] = []
        self.round: GameRound = GameRound.Pre_Flop

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

        if self.two_player_game:
            self.small_blind_holder = 0
            self.big_blind_holder = 1

        print(f"The dealer is: {self.dealer_player.user.name}")
        print(f"The small blind player is: {self.small_blind_player.user.name}")
        print(f"The big blind player is: {self.big_blind_player.user.name}\n")
        
        print(f"The players, starting from the dealer, are: {' --> '.join(map(lambda p: p.user.name, self.players))}\n")
        
        main_pot: Pot = Pot()

        main_pot.place_bet(self.small_blind_player, self.small_blind_bet)
        main_pot.place_bet(self.big_blind_player, self.big_blind_bet)
        
        #Debug
        print(f"Player: {self.small_blind_player.user.name} is entering the small blind amount of {self.small_blind_bet}! Their current balance is {self.small_blind_player.user.money}")
        print(f"Player: {self.big_blind_player.user.name} is entering the big blind amount of {self.big_blind_bet}! Their current balance is {self.big_blind_player.user.money}\n")

        self.pots.append(main_pot)
        self.current_pot_index = 0

        #Debug
        print(f"Game is starting...\n")
            
        #Shuffle deck
        self.deck.shuffle_deck()

        self.play_round()

        #Debug
        print(f"Game has ended...\n\n")

    def _validate_money_for_big_blind_bet(self, money: float) -> None:
        if money < self.big_blind_bet:
            raise ValueError("The player that you are trying to add has less money than required to enter the game!")
        
    @dispatch(Player)
    def add_player(self, player: Player) -> None:
        self._validate_money_for_big_blind_bet(player.user.money)

        self.players.append(player)
        self.two_player_game = len(self.players) == 2

    @dispatch(User)
    def add_player(self, user: User) -> None:
        self._validate_money_for_big_blind_bet(user.money)

        self.players.append(Player(user))
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
        while True:
            self.turn = self.__next_index(self.turn)
            
            if not self.current_player.has_played_turn:
                break
       
    def _deal_players_cards(self):
        #Give out a card to each player once and then twice(because that is how you deal poker hands, one at a time)
        for i in range(2):         
            for player in self.players:
                player.cards.append(self.deck.cards.pop())
            
        #Debug
        for player in self.players: 
            print(f"Player: {player.user.name} has drawn cards: {player.cards}")
            
        print()

    def _deal_flop(self):
        self.deck.cards.pop()
        
        for i in range(0, 3):
            self.community_cards.append(self.deck.cards.pop())

        #Debug
        print(f"During the flop round these cards were drawn: {self.community_cards}\n")
        
    def _deal_turn_or_river(self):
        self.deck.cards.pop()
        
        self.community_cards.append(self.deck.cards.pop())

        #Debug
        print(f"During the turn(4th street) round or the River round, these were the cards: {self.community_cards}\n")

    def deal_cards(self):
        if self.round == GameRound.Pre_Flop:
            self._deal_players_cards()

        if self.round == GameRound.Flop:
            self._deal_flop()
            
        elif self.round == GameRound.Turn or self.round == GameRound.River:
            self._deal_turn_or_river()
            
    def deal_until_showdown(self):
        while len(self.community_cards) != 5:
            self.deal_cards()
            self.next_round()        

    def start_round(self): 
        #Debug
        print(f"{self.round} is starting...\n")

        #Set the current highest stake for the current pot for this round to 0 to reset it
        if (self.round != GameRound.Pre_Flop):
            self.current_pot.current_highest_stake = 0

        #Reset the has_played_turn status for all the players who have not folded and are not all-in
        for player in self.current_pot.get_players_not_folded_and_not_all_in():
            player.has_played_turn = False

        #Set the first person to act during the round. If we are in pre-flop, then that is the person after the big_blind_holder.
        #Else, it is the person after the dealer(the small_blind_holder, who is inbetween the dealer and the big_blind_holder)
        if self.round == GameRound.Pre_Flop:
            self.turn = self.big_blind_holder
        else:
            self.turn = self.dealer_index    

        self.deal_cards()

        self.next_turn()  

    def get_possible_actions(self, player: Player, pot: Pot) -> Tuple[List[PlayerActionType], float]:
        #Determine the possible actions
        call_amount: float = 0
        possible_actions: List[PlayerActionType] = []

        if not player.has_folded and not player.is_all_in:

            possible_actions.append(PlayerActionType.FOLD)
            stake = pot.get_stake_for_player(player)

            #In this case, there has been a bet this round already
            if stake != pot.current_highest_stake:
                possible_actions.append(PlayerActionType.CALL)

                highest_stake_diff: float = pot.current_highest_stake - stake
                call_amount: float = min(highest_stake_diff, player.user.money)

                can_raise: bool = highest_stake_diff <= player.user.money and any(map(lambda x: x != player and not x.is_all_in, pot.players))

                if can_raise:
                    possible_actions.append(PlayerActionType.RAISE)
            #In this case, nobody has bet thus far this round
            else:
                possible_actions.append(PlayerActionType.CHECK)
                
                #This is only possible for the big_blind_holder during the pre-flop, where can either choose to Check or to raise the big_blind
                if stake == pot.current_highest_stake and stake == 0:                    
                    possible_actions.append(PlayerActionType.RAISE)
                else:
                    possible_actions.append(PlayerActionType.BET)

        return (possible_actions, call_amount)

    def play_turn(self) -> bool:
        player = self.current_player
        pot = self.current_pot
        
        #This should normally be impossible, but just in case
        if player.is_all_in:
            #Debug
            print(f"Player: {player.user.name} is all in with amount {pot.get_stake_for_player(player)}! Their current balance is {player.user.money}\n")
        #This should normally be impossible, but just in case
        elif player.has_folded:
            #Debug
            print(f"Player: {player.user.name} has folded! Their current balance is {player.user.money}\n")
        else:
            #Determine the possible actions
            possible_actions, call_amount = self.get_possible_actions(player, pot)

            action: PlayerAction = player.choose_action(possible_actions, call_amount)

            if action.type == PlayerActionType.FOLD:
                player.has_folded = True
            elif action.type == PlayerActionType.RAISE or action.type == PlayerActionType.BET:
                #For each player that has not folded or is not all-in, reset their has_played_turn state
                for other_player in self.players:
                    if not other_player.has_folded and not other_player.is_all_in:
                        other_player.has_played_turn = False

            if action.type != PlayerActionType.FOLD and action.type != PlayerActionType.CHECK:
                pot.place_bet(player, action.amount)
                
                #In this case, we are not all-in
                if player.user.money != 0:
                    #Debug
                    print(f"Player: {player.user.name} is doing {action.type.name} with amount {action.amount}! Their current balance is {player.user.money}\n")
                if player.user.money == 0:
                    #Debug
                    print(f"Player: {player.user.name} is going all-in! Their current balance is {player.user.money}\n")
                    
            elif action.type == PlayerActionType.FOLD:
                #Debug
                print(f"Player: {player.user.name} has folded! Their current balance is {player.user.money}\n")
            elif action.type == PlayerActionType.CHECK:
                #Debug
                print(f"Player: {player.user.name} has checked! Their current balance is {player.user.money}\n")

        player.has_played_turn = True
        
        players_not_played: List[Player] = pot.get_players_not_played()
        players_not_folded: List[Player] = pot.get_players_not_folded()

        if len(players_not_played) == 0:
            return True
        elif len(players_not_folded) == 1:
            return True

        self.next_turn()
        return False       

    def play_showdown(self):
        #Debug
        print(f"Showdown is starting...\n")

        # players_not_folded = self.pots[0].get_players_not_folded()
        
        #Debug
        print(f"Community cards: {self.community_cards}\n")
        
        self.payout()

        
    def calc_best_hand(self, player: Player):
        if player.best_hand is not None:
            return
        
        player_cards: List[Card] = self.community_cards.copy()
        for card in player.cards.copy():
            player_cards.append(card)

        possible_hands = Hand.get_all_5_card_hands(player_cards)

        possible_hands_sorted = sorted(possible_hands, key=functools.cmp_to_key(Hand.compare_hands))

        player.best_hand = possible_hands_sorted[-1]
        
    def calc_best_hands(self, players: List[Player]):
        #Set best hand for each player
        for player in players:
            self.calc_best_hand(player)

    def payout_winner(self, pot: Pot, ordered_players: List[Player]):
        all_winners: List[Player] = list(filter(
            lambda player: Hand.compare_hands(player.best_hand, ordered_players[-1].best_hand) == 0, 
            ordered_players)) if len(ordered_players) != 1 else ordered_players

        #Split the prize between all the winning players
        has_single_winner = len(all_winners) == 1
        per_player_winnings: float = pot.total_money / len(all_winners)

        #Debug
        if not has_single_winner:
            print(f"Players: {', '.join(map(lambda x: x.user.name, all_winners))} are tied winners for Pot #{self.pots.index(pot)}\n")

        for winning_player in all_winners:
            
            winning_player.user.money += per_player_winnings
            
            #Debug
            if has_single_winner:
                print(f"Player: {winning_player.user.name} has won Pot #{self.pots.index(pot)} and claimed {per_player_winnings}$ from the pot\n")
            else:
                print(f"Player: {winning_player.user.name} has claimed {per_player_winnings}$ from the pot\n")

    def payout(self) -> None:
        unnecessary_pots_filter = lambda pot: len(pot.players) == 1 or pot.total_money == 0

        #Payout the money from the unnecessary pots silently(without showing it in the UI)
        unnecessary_pots: List[Pot] = list(filter(unnecessary_pots_filter, self.pots))

        for pot in unnecessary_pots:
            if pot.total_money != 0:
                pot.players[0].user.money += pot.total_money

        #Remove the unnecessary pots with only one player or with no money in them
        filtered_pots: List[Pot] = list(filter(lambda pot: not unnecessary_pots_filter(pot), self.pots))

        #Reverse the pots, because we need to start from the most recent side pot and then move down the main pot
        filtered_pots.reverse()
        
        for pot in filtered_pots:
            #Debug
            print(f"Resolving Pot #{self.pots.index(pot)} -- Money in pot: {pot.total_money}$\n")
            
            players_not_folded = pot.get_players_not_folded()
            
            #Debug
            print(f"Players: {', '.join(map(lambda x: x.user.name, players_not_folded))}\n")                
            
            #In this case, we have all 5 community cards needed to calculate the best cards, because there are at least 2 people who got to showdown round
            if len(players_not_folded) > 1:
                for player in players_not_folded:
                    self.calc_best_hand(player)   
                    
                    print(f"Player: {player.user.name}\nCards: {player.cards}\nBest Hand: {player.best_hand}\nCombination:{player.best_hand.combination.name}\n")
                   
                #Order the players by their hand strengths
                ordered_players: List[Player] = sorted(players_not_folded, key=lambda p: functools.cmp_to_key(Hand.compare_hands)(p.best_hand))

                self.payout_winner(pot, ordered_players)
                
            #In this case, all but one players have folded, so no need to calc best card
            #(which may not be calculateable anyway because it is not guaranteed that all 5 community cards have appeared) 
            else:
                self.payout_winner(pot, players_not_folded)
            

    def split_current_pot(self) -> None:
        #Order the players in the pot by their stakes
        self.current_pot.players.sort(key=lambda p: p.stake)
        
        while self.current_pot.should_be_split():
            pot: Pot = self.current_pot
            players: List[Player] = self.current_pot.get_players_not_folded()
            
            for player in players:
                if player.is_all_in:
                    player_stake = player.stake
                    pot.total_money = len(players) * player_stake
                    
                    side_pot: Pot = Pot()                     
                    side_players = filter(lambda x: x != player, players)
                    
                    #Add the left over players to the side pot and transfer their remaining stakes to the side pot
                    for side_player in side_players:
                        side_pot.players.append(side_player)
                        side_player.stake -= player_stake
                        side_pot.total_money += side_player.stake
                        
                    self.pots.append(side_pot)
                    self.current_pot_index += 1
                    
                    break

    def play_round(self) -> None:
        self.start_round()

        while True:
            round_over = self.play_turn()

            if round_over:
                self.split_current_pot()
                self.next_round()

            if round_over and self.round == GameRound.Showdown:
                self.play_showdown()
                break
            elif round_over and len(self.current_pot.get_players_not_folded()) == 1:          
                # In this case, there is only the main pot and all but one players have folded it, so no need to get all 5 community cards
                if len(self.pots) == 1:           
                    self.payout()
                
                # In this case, there is one remaining person on the main pot, but there is at least one other person who is all-in on a side pot
                # This means that we have to deal all the community cards
                else:
                    self.deal_until_showdown()
                    self.play_showdown()                  
                break
            #In this case, all the players of the main pot are all-in, so just proceed to get all the community cards out and play the showdown
            elif round_over and self.current_pot.all_players_are_all_in():
                self.deal_until_showdown()
                self.play_showdown()
                break   
                
            elif round_over:
                self.play_round()
                break

    def next_round(self):
        #Debug
        print(f"{self.round} is over...\n{'-'.join(['']*100)}\n")
        self.round = self.round.next_round()

    @property
    def is_two_player_game(self) -> bool:
        return len(self.players) == 2

    @property
    def current_pot(self) -> Pot:
        return self.pots[self.current_pot_index]

    @property
    def current_player(self) -> Player:
        return self.players[self.turn]

    @property
    def big_blind_player(self) -> Player:
        return self.players[self.big_blind_holder]

    @property
    def small_blind_player(self) -> Player:
        return self.players[self.small_blind_holder]
    
    @property
    def dealer_player(self) -> Player:
        return self.players[self.dealer_index]
        
    @property
    def players(self) -> List[Player]:
        return self.__players    