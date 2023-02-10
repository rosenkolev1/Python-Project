from typing import List
from src.game.player.player import Player

class Pot:

    def __init__(self) -> None:
        self.players: List[Player] = []
        self.total_money: float = 0

        self.current_highest_stake = 0

    def get_stake_for_player(self, player: Player):
        if player not in self.players:
            return 0
        
        return player.stake

    def place_bet(self, player: Player, amount: float) -> None:
        if player not in self.players:
            self.players.append(player)

        player.stake += amount  

        player_stake = self.get_stake_for_player(player)

        if player_stake > self.current_highest_stake:
            self.current_highest_stake = player_stake

        self.total_money += amount
        player.user.money -= amount

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
