from typing import List
from game.pot_player import PotPlayer

class Pot:

    def __init__(self) -> None:
        self.pot_players: List[PotPlayer] = []
        self.total_money: float = 0

        self.current_highest_stake = 0

    def get_stake_for_player(self, player: PotPlayer):
        if player not in self.pot_players:
            return 0
        
        return player.stake

    def place_bet(self, player: PotPlayer, amount: float) -> None:
        if player not in self.pot_players:
            self.pot_players.append(player)

        player.stake += amount  

        player_stake = self.get_stake_for_player(player)

        if player_stake > self.current_highest_stake:
            self.current_highest_stake = player_stake

        self.total_money += amount
        player.user.money -= amount

    def bet_is_matched_all(self) -> bool:
        for pot_player in self.pot_players:
            stake = self.get_stake_for_player(pot_player)

            if not pot_player.has_folded and (not pot_player.has_played_turn or stake != self.current_highest_stake):
                return False

        return True

    def all_players_have_folded(self) -> bool:
        return len(self.get_players_not_folded()) > 0

    def all_players_have_played(self) -> bool:
        return len(self.get_players_not_played()) > 0

    def get_players_not_played(self) -> List[PotPlayer]:
        return [pot_player for pot_player in self.pot_players if pot_player.has_played_turn == False]

    def get_players_not_folded(self) -> List[PotPlayer]:
        return [pot_player for pot_player in self.pot_players if not pot_player.has_folded]
             
    # def get_stake_for_player(self, player: Player):
    #     players_list = [pot_player.player for pot_player in self.pot_players]

    #     if player not in players_list:
    #         return 0
        
    #     pot_player_index = players_list.index(player)

    #     return self.pot_players[pot_player_index].stake

    # def place_bet(self, player: Player, amount: float) -> None:
    #     players_list = [pot_player.player for pot_player in self.pot_players]

    #     if player not in players_list:
    #         self.pot_players.append(PotPlayer(player, amount))
    #     else:
    #         pot_player_index = players_list.index(player)
    #         self.pot_players[pot_player_index].stake += amount

    #     self.total_money += amount
    #     player.money -= amount
