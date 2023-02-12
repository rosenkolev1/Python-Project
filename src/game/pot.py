from typing import List
from src.game.player.player import Player
from src.game.setting.game_setting import GameSetting

class Pot:

    def __init__(self) -> None:
        self.players: List[Player] = []
        self.total_money: float = 0

        self.current_highest_stake = 0
        self.highest_bet_amount = 0

        self.player_who_opened_pot = None

    def get_stake_for_player(self, player: Player):
        if player not in self.players:
            return 0
        
        return player.stake

    def place_bet(self, player: Player, amount: float, settings: GameSetting) -> None:
        if player not in self.players:
            self.players.append(player)

        player.stake = round(player.stake + amount, 2)  

        player_stake = self.get_stake_for_player(player)

        if player_stake > self.current_highest_stake:
            
            # If the minimum bet/raise is 20, the call is 10 and a player goes all-in with 20$, then his raise of 10$ over the call
            # Does not reopen the pot, instead it is treated as a 'call with extra money'
            # This means that the person who originally raised the bet can not re-raise it again if all others before him call/fold
            bet_min_amount_to_open: float = self.highest_bet_amount if settings.bet_minimum_enabled else 0  
            bet_opens_pot: bool = (player_stake > self.current_highest_stake + bet_min_amount_to_open and
                                   amount >= bet_min_amount_to_open)

            # stake_diff: float = round(self.current_highest_stake - player_stake, 2)

            # bet_opens_pot: bool = amount >= bet_min_amount_to_open

            if bet_opens_pot:
                # This check is so that the highest bet amount is calculated properly at the start of a new round after the first bet
                if self.player_who_opened_pot is None:
                    self.highest_bet_amount = amount
                
                # This check is so that the highest bet amount is calculated properly at the start of a new round after 
                # Somebody goes all-in with an incomplete bet/raise
                else:
                    self.highest_bet_amount = round(player_stake - self.current_highest_stake, 2)

                self.player_who_opened_pot = player

            self.current_highest_stake = player_stake

        self.total_money = round(self.total_money + amount, 2)
        player.user.money = round(player.user.money - amount, 2)
        
        # if self.highest_bet_amount < amount:
        #     self.highest_bet_amount = amount

    def bet_is_matched_all(self) -> bool:
        for player in self.players:
            stake = self.get_stake_for_player(player)

            if not player.has_folded and (not player.has_played_turn or stake != self.current_highest_stake):
                return False

        return True

    def should_be_split(self) -> bool:
        active_players: List[Player] = self.get_players_not_folded()

        players_all_in: List[Player] = list(map(lambda player: player.is_all_in, active_players))

        should_split_condition_1: bool = any(players_all_in) and not all(players_all_in)

        if should_split_condition_1:
            return True

        active_players_have_same_stakes: bool = True

        for i in range(0, len(active_players) - 1):
            player_1: Player = active_players[i]
            player_2: Player = active_players[i+1]

            if player_1.stake != player_2.stake:
                return True
        
        return False

    def all_players_have_folded(self) -> bool:
        return len(self.get_players_not_folded()) > 0

    def all_players_have_played(self) -> bool:
        return len(self.get_players_not_played()) > 0
    
    def all_players_are_all_in(self) -> bool:
        players_all_in: List[Player] = list(map(lambda player: player.is_all_in, self.players))
        
        return all(players_all_in)

    def get_players_have_played(self) -> List[Player]:
        return [player for player in self.players if player.has_played_turn]

    def get_players_not_played(self) -> List[Player]:
        return [player for player in self.players if player.has_played_turn == False]

    def get_players_not_folded(self) -> List[Player]:
        return [player for player in self.players if not player.has_folded]
    
    def get_players_not_folded_and_not_all_in(self) -> List[Player]:
        return [player for player in self.players if not player.has_folded and not player.is_all_in]
