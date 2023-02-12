from __future__ import annotations
from typing import TYPE_CHECKING, List
from src.game.player.choose_action_info import ChooseActionInfo

from src.game.player.player import Player
from src.game.player.player_action import PlayerAction
from src.game.player.player_action_type import PlayerActionType
from src.game.pot import Pot

if TYPE_CHECKING:
    from src.game.game import Game

class GameUI:
    PLAYER_COMMAND_ACTION_MAP = {
        "fold": PlayerActionType.FOLD,
        "check": PlayerActionType.CHECK,
        "call": PlayerActionType.CALL,
        "bet": PlayerActionType.BET,
        "raise": PlayerActionType.RAISE,
        "all-in": PlayerActionType.ALL_IN,
    }

    INVALID_COMMAND: str = "\nThe given command is invalid, try again!\n"

    INVALID_COMMAND_MISSING_AMOUNT_ARGUMENT = "\nThe given command is invalid because you have not specified an amount!\n"

    INVALID_BET_AMOUNT_IS_NEGATIVE_OR_ZERO = "\nInvalid action! Cannot bet or raise 0$ or less!\n"

    INVALID_RAISE_AMOUNT_BELOW_MINIMUM = "\nInvalid raise. You cannot raise less than the minimum required!\n"

    GAME_STARTING_INFO_PROMPT = "Game is starting...\n"

    GAME_ENDING_INFO_PROMPT = "Game has ended...\n\n"

    SHOWDOWN_STARTING_INFO_PROMPT = f"Showdown is starting...\n"

    @staticmethod
    def invalid_raise_amount_below_minimum(amount: float):
        return f"Invalid raise. You cannot raise less than the minimum required! The minimum raise is: {amount}$\n"

    @staticmethod
    def invalid_bet_amount_below_minimum(amount: float):
        return f"Invalid bet. You cannot bet less than the minimum required! The minimum bet is: {amount}$\n"

    @staticmethod
    def dealer_info_prompt(game: Game) -> str:
        return f"The dealer is: {game.dealer_player.user.name}"

    @staticmethod
    def small_blind_player_info_prompt(game: Game) -> str:
        return f"The small blind player is: {game.small_blind_player.user.name}"

    @staticmethod
    def big_blind_player_info_prompt(game: Game) -> str:
        return f"The big blind player is: {game.big_blind_player.user.name}"

    @staticmethod
    def players_list_info_prompt(game: Game) -> str:
        players: List[Player] = []

        for i in range(game.settings.dealer_index, len(game.players)):
            players.append(game.players[i])

        for i in range(0, game.settings.dealer_index):
            players.append(game.players[i])

        return f"The players, starting from the dealer, are: {' --> '.join(map(lambda p: p.user.name, players))}\n"
    
    @staticmethod
    def small_blind_entered_info_prompt(game: Game) -> str:
        return (
            f"Player: {game.small_blind_player.user.name} is entering the small blind amount of" + 
            f" {game.settings.small_blind_bet}! Their current balance is {game.small_blind_player.user.money}")

    @staticmethod
    def big_blind_entered_info_prompt(game: Game) -> str:
        return (f"Player: {game.big_blind_player.user.name} is entering the big blind amount of" + 
               f" {game.settings.big_blind_bet}! Their current balance is {game.big_blind_player.user.money}") 

    @staticmethod
    def ante_entered_info_prompt(player: Player, ante_amount: float) -> str:
        return (f"Player: {player.user.name} is entering the ante of" + 
               f" {ante_amount}! Their current balance is {player.user.money}")

    @staticmethod
    def player_dealt_cards_info_prompt(player: Player) -> str:
        return f"Player: {player.user.name} has been dealt these cards: {player.cards}"

    @staticmethod
    def flop_dealing_cards_from_deck_info_prompt(game: Game) -> str:
        return f"During the {game.round.value} round these cards were dealt: {game.community_cards}\n"

    @staticmethod
    def dealing_cards_from_deck_turn_river_info_prompt(game: Game) -> str:
        return f"During the {game.round.value}, these were the cards: {game.community_cards}\n"

    @staticmethod
    def round_starting_info_prompt(game: Game) -> str:
        return f"{game.round} is starting...\n"

    @staticmethod
    def player_raising_info_prompt(player: Player, action: PlayerAction, call_amount: float) -> str:
        return f"Player: {player.user.name} is doing {action.type.name} by amount {round(action.amount - call_amount, 2)}$! Their current balance is {player.user.money}$\n"

    @staticmethod
    def player_bet_or_call_info_prompt(player: Player, action: PlayerAction) -> str:
        return f"Player: {player.user.name} is doing {action.type.name} with amount {action.amount}$! Their current balance is {player.user.money}$\n"

    @staticmethod
    def player_fold_info_prompt(player: Player) -> str:
        return f"Player: {player.user.name} has folded! Their current balance is {player.user.money}\n"

    @staticmethod
    def player_all_in_info_prompt(player: Player, action: PlayerAction) -> str:
        return f"Player: {player.user.name} is all-in with {action.amount}$! Their current balance is {player.user.money}$\n"

    @staticmethod
    def player_check_info_prompt(player: Player):
        return f"Player: {player.user.name} has checked! Their current balance is {player.user.money}\n"

    @staticmethod
    def community_cards_info_prompt(game: Game) -> str:
        return f"Community cards: {game.community_cards}\n"

    @staticmethod
    def pot_winners_tied_info_prompt(game: Game, all_winners: List[Player], pot: Pot) -> str:
        return f"Players: {', '.join(map(lambda x: x.user.name, all_winners))} are tied winners for Pot #{game.pot_number(pot)}\n"

    @staticmethod
    def pot_single_winner_claim_winnings_info_prompt(game: Game, winning_player: Player, amount_won: float,  pot: Pot) -> str:
        return f"Player: {winning_player.user.name} has won Pot #{game.pot_number(pot)} and claimed {amount_won}$ from the pot\n"

    @staticmethod
    def pot_tied_winners_claim_split_winnings_info_prompt(winning_player: Player, amount_won: float) -> str:
        return f"Player: {winning_player.user.name} has claimed {amount_won}$ from the pot\n"

    @staticmethod
    def resolving_pot_info_prompt(game: Game, pot: Pot) -> str:
        return f"Resolving Pot #{game.pot_number(pot)} -- Money in pot: {pot.total_money}$\n"

    @staticmethod
    def resolving_pot_players_list_info_prompt(players_not_folded: List[Player]) -> str:
        return f"Players: {', '.join(map(lambda x: x.user.name, players_not_folded))}\n"

    @staticmethod
    def player_hand_info_prompt(player: Player) -> str:
        return f"Player: {player.user.name}\nCards: {player.cards}\nBest Hand: {player.best_hand}\nCombination:{player.best_hand.combination.name}\n"

    @staticmethod
    def round_over_line_separator(game: Game) -> str:
        return f"{game.round} is over...\n{'-'.join(['']*100)}\n"

    @staticmethod
    def action_command_prompt(player: Player, action: PlayerActionType, action_info: ChooseActionInfo):
        if action == PlayerActionType.FOLD:
            return "Fold"
        elif action == PlayerActionType.CHECK:
            return "Check"
        elif action == PlayerActionType.RAISE:
            if action_info.game.settings.bet_minimum_enabled:
                return f"Raise <amount-to-raise-by({action_info.pot.highest_bet_amount}$ or more)>"

            return "Raise <amount-to-raise-by>"
        elif action == PlayerActionType.BET:
            if action_info.game.settings.bet_minimum_enabled:
                return f"Bet <amount-to-bet({action_info.pot.highest_bet_amount}$ or more)>"

            return"Bet <amount-to-bet>"
        elif action == PlayerActionType.ALL_IN:
            return f"All-in {player.user.money}$"
        elif action == PlayerActionType.CALL:
            return f"Call {action_info.call_amount}$"
            
        raise ValueError("Invalid action command!")

    @staticmethod
    def choose_actions_command_prompt(player: Player, actions: List[PlayerActionType], action_info: ChooseActionInfo) -> str:
        sorted_actions = sorted(actions, key=lambda x: x.value)
        action_strings: List[str] = []

        for action in sorted_actions:
            action_str = GameUI.action_command_prompt(player, action, action_info)
            action_strings.append(action_str)

        res = f"Player: {player.user.name}, it is your turn. Choose an action ({' | '.join(action_strings)}): "
        return res