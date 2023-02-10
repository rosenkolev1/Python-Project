import functools
from typing import List, Tuple
from multipledispatch import dispatch

from src.game.deck.card import Card
from src.game.hand.hand import Hand
from src.game.player.player_action import PlayerAction
from src.game.player.player_action_type import PlayerActionType

from src.game.player.player import Player
from src.game.deck.deck import Deck
from src.game.game_round import GameRound
from src.game.pot import Pot
from src.game.setting.game_setting import GameSetting
from src.game.user_interface.game_ui import GameUI

class Game:

    def __init__(self, game_setting: GameSetting) -> None:
        # self.deck: Deck = game_setting.deck

        # self.turn: int = game_setting.turn
        # self.dealer_index: int = game_setting.dealer_index

        # self.small_blind_bet: float = game_setting.small_blind_bet
        # self.small_blind_holder: int = game_setting.small_blind_holder

        # self.big_blind_bet: float = game_setting.big_blind_bet
        # self.big_blind_holder: int = game_setting.big_blind_holder

        self.settings: GameSetting = game_setting
        
        self.community_cards: List[Card] = []
        
        self.pots: List[Pot] = []
        self.current_pot_index: int = 0 

        self.players: List[Player] = []
        self.round: GameRound = GameRound.Pre_Flop

        self.table = None

    def start_game(self):
        self.round = GameRound.Pre_Flop

        self.pots.clear()

        #TODO: Change depending on the game setting
        if self.is_two_player_game and self.table is None:
            self.settings.small_blind_holder = 0
            self.settings.big_blind_holder = 1

        print(GameUI.dealer_info_prompt(self))
        print(GameUI.small_blind_player_info_prompt(self))
        print(GameUI.big_blind_player_info_prompt(self))
        print(GameUI.players_list_info_prompt(self))
        
        main_pot: Pot = Pot()

        main_pot.place_bet(self.small_blind_player, self.settings.small_blind_bet)
        main_pot.place_bet(self.big_blind_player, self.settings.big_blind_bet)
        
        print(GameUI.small_blind_entered_info_prompt(self))
        print(GameUI.big_blind_entered_info_prompt(self))

        self.pots.append(main_pot)
        self.current_pot_index = 0

        print(GameUI.GAME_STARTING_INFO_PROMPT)
            
        #Shuffle deck
        self.settings.deck.shuffle_deck()

        self.play_round()

        print(GameUI.GAME_ENDING_INFO_PROMPT)

    def _validate_money_for_big_blind_bet(self, money: float) -> None:
        if money < self.settings.big_blind_bet:
            raise ValueError("The player that you are trying to add has less money than required to enter the game!")
        
    def add_player(self, player: Player) -> None:
        self._validate_money_for_big_blind_bet(player.user.money)

        self.players.append(player)
        self.two_player_game = len(self.players) == 2

    def pot_number(self, pot: Pot) -> int:
        return self.pots.index(pot) + 1

    def __next_index(self, indexer: int) -> int:
        indexer += 1

        if indexer == len(self.players):
            indexer = 0

        return indexer

    def next_pot(self) -> None:
        self.current_pot_index = self.__next_index(self.current_pot_index)

    def next_turn(self) -> None:
        while True:
            self.settings.turn = self.__next_index(self.settings.turn)
            
            if not self.current_player.has_played_turn:
                break
       
    def _deal_players_cards(self):
        #Give out a card to each player once and then twice(because that is how you deal poker hands, one at a time)
        for i in range(2):         
            for player in self.players:
                player.cards.append(self.settings.deck.cards.pop())
            
        for player in self.players: 
            print(GameUI.player_dealt_cards_info_prompt(player))
            
        print()

    def _deal_flop(self):
        self.settings.deck.cards.pop()
        
        for i in range(0, 3):
            self.community_cards.append(self.settings.deck.cards.pop())

        print(GameUI.flop_dealing_cards_from_deck_info_prompt(self))
        
    def _deal_turn_or_river(self):
        self.settings.deck.cards.pop()
        
        self.community_cards.append(self.settings.deck.cards.pop())

        print(GameUI.dealing_cards_from_deck_turn_river_info_prompt(self))

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
        print(GameUI.round_starting_info_prompt(self))

        #Set the current highest stake for the current pot for this round to 0 to reset it
        if (self.round != GameRound.Pre_Flop):
            self.current_pot.current_highest_stake = 0

        #Reset the has_played_turn status for all the players who have not folded and are not all-in
        for player in self.current_pot.get_players_not_folded_and_not_all_in():
            player.has_played_turn = False

        #Set the first person to act during the round. If we are in pre-flop, then that is the person after the big_blind_holder.
        #Else, it is the person after the dealer(the small_blind_holder, who is inbetween the dealer and the big_blind_holder)
        if self.round == GameRound.Pre_Flop:
            self.settings.turn = self.settings.big_blind_holder
        else:
            self.settings.turn = self.settings.dealer_index    

        self.deal_cards()

        self.next_turn()  

    def get_possible_actions(self, player: Player, pot: Pot) -> Tuple[List[PlayerActionType], float]:
        #Determine the possible actions
        call_amount: float = 0
        possible_actions: List[PlayerActionType] = []

        if not player.has_folded and not player.is_all_in:

            possible_actions.append(PlayerActionType.FOLD)
            stake = pot.get_stake_for_player(player)

            #The player can always choose to go all-in
            possible_actions.append(PlayerActionType.ALL_IN)

            #In this case, there has been a bet this round already (big blind during pre-flop counts as a bet)
            if 0 != pot.current_highest_stake:
                highest_stake_diff: float = pot.current_highest_stake - stake

                calling_is_all_in = highest_stake_diff >= player.user.money

                call_amount: float = min(highest_stake_diff, player.user.money)   

                #This happens at the start of the new rounds, i.e. when there is not bet to call on
                if call_amount < 0:
                    call_amount = 0

                can_raise: bool = not calling_is_all_in and any(map(lambda x: x != player and not x.is_all_in, pot.players))

                if not calling_is_all_in:
                    possible_actions.append(PlayerActionType.CALL)

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
            pass
            #Debug
            # print(f"Player: {player.user.name} is all in with amount {pot.get_stake_for_player(player)}! Their current balance is {player.user.money}\n")
        #This should normally be impossible, but just in case
        elif player.has_folded:
            pass
            #Debug
            # print(f"Player: {player.user.name} has folded! Their current balance is {player.user.money}\n")
        else:
            #Determine the possible actions
            possible_actions, call_amount = self.get_possible_actions(player, pot)

            action: PlayerAction = player.choose_action(possible_actions, call_amount)

            is_all_in: bool = action.type == PlayerActionType.ALL_IN
            is_all_in_and_raise: bool = is_all_in and pot.get_stake_for_player(player) + action.amount > pot.current_highest_stake

            if action.type == PlayerActionType.FOLD:
                player.has_folded = True
            elif action.type == PlayerActionType.RAISE or action.type == PlayerActionType.BET or is_all_in_and_raise:
                #For each player that has not folded or is not all-in, reset their has_played_turn state
                for other_player in self.players:
                    if not other_player.has_folded and not other_player.is_all_in:
                        other_player.has_played_turn = False

            if action.type != PlayerActionType.FOLD and action.type != PlayerActionType.CHECK:
                pot.place_bet(player, action.amount)
                
                #In this case, we are not all-in
                if not is_all_in:
                    if action.type == PlayerActionType.RAISE:
                        print(GameUI.player_raising_info_prompt(player, action, call_amount))
                    else:
                        print(GameUI.player_bet_or_call_info_prompt(player, action))
                else:
                    print(GameUI.player_all_in_info_prompt(player, action))
                    
            elif action.type == PlayerActionType.FOLD:
                print(GameUI.player_fold_info_prompt(player))
            elif action.type == PlayerActionType.CHECK:
                print(GameUI.player_check_info_prompt(player))

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
        print(GameUI.SHOWDOWN_STARTING_INFO_PROMPT)
        
        print(GameUI.community_cards_info_prompt(self))
        
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

        if not has_single_winner:
            print(GameUI.pot_winners_tied_info_prompt(self, all_winners, pot))

        for winning_player in all_winners:
            
            winning_player.user.money += per_player_winnings
            
            if has_single_winner:
                print(GameUI.pot_single_winner_claim_winnings_info_prompt(self, winning_player, per_player_winnings, pot))
            else:
                print(GameUI.pot_tied_winners_claim_split_winnings_info_prompt(winning_player, per_player_winnings))

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
            print(GameUI.resolving_pot_info_prompt(self, pot))
            
            players_not_folded = pot.get_players_not_folded()
            
            print(GameUI.resolving_pot_players_list_info_prompt(players_not_folded))                
            
            #In this case, we have all 5 community cards needed to calculate the best cards, because there are at least 2 people who got to showdown round
            if len(players_not_folded) > 1:
                for player in players_not_folded:
                    self.calc_best_hand(player)   
                    
                    print(GameUI.player_hand_info_prompt(player))
                   
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
        print(GameUI.round_over_line_separator(self))
        self.round = self.round.next_round()

    @property
    def is_two_player_game(self) -> bool:
        return len(self.players) == 2

    @property
    def current_pot(self) -> Pot:
        return self.pots[self.current_pot_index]

    @property
    def current_player(self) -> Player:
        return self.players[self.settings.turn]

    @property
    def big_blind_player(self) -> Player:
        return self.players[self.settings.big_blind_holder]

    @property
    def small_blind_player(self) -> Player:
        return self.players[self.settings.small_blind_holder]
    
    @property
    def dealer_player(self) -> Player:
        return self.players[self.settings.dealer_index]