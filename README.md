## To run the app, you are going to have to create a virtual environment and download all the necessary requirement from the requirement.txt

I followed the steps at bottom of https://github.com/fmipython/PythonCourse2022/blob/main/13%20-%20Modules/13%20-%20Modules.ipynb
For setting up the VENV.

You can the run the main.py file with F5 or run the pytest tests in the test directory

Check the 'main.py' file for more info on how the app works! 

*The docs in the Moodle zip are not finished because I ran out of time. You can read the full docs from the GitHub repo, 
or alternatively download the project from the repo itself.

DOCS, RIPPED OUT OF THE DOCSTRINGS OF THE FILES:

"""
    Hi, this is the doc about the project. I originally wanted this project to be a PyGame poker app,
    but I had no time to make the PyGame part, nor to make fully fleshed out console UI game.
    So instead, you can treat this as an unfinished console UI poker game. 
    
    It only supports Texas Hold'em poker
    
    By unfinished, I mean that I have not added
    a functionality for creating users with money and tables and games with users and players from the console.
    However, actually playing the poker game itself from the console with commands does work
    
    You can also treat this project as some kind of poker game API as well I guess, since I made it somewhat customizable!
    
    Check out the examples below and the tests as well for more info!
"""

"""
    The User class contains a name and money
"""

```
user_1 = User("Roskata", 1000)
user_2 = User("Stefan", 1000)
user_3 = User("Kris", 1000)
user_4 = User("Miro", 1000)
user_5 = User("Ge6a", 1000)
user_6 = User("Pe6o", 1000)
```

"""
    The BotPlayer is a player who is, well, not controlled by a human, but is a bot.
    It plays on it's own. The moves it makes on any given turn depend on the 'choose_action' function that you give to the bot
    The bot(or any player for that matter) needs to be tied to a user
    
    The abstract Player class, which is the base class of the BotPlayer, represents an entity that is a part of a game.
    
    It contains 3 major functions:
        - 'get_possible_actions', which determines the legal moves that a player can make at this time
        
        - 'choose_action', which determines which of the legal moves the player will make. It is an abstract method.
        
        - 'predefine_choose_action', which allows us to pass an implementation of a 'choose_action' function as a parameter and 
            and reassign 'choose_action' to use the given function for handling the choice. It is an abstract method.
            
    The class contains the fields:
        - 'user' - The user behind of the player.
    
        - 'stake' - The stake of the player in the current pot
        
        - 'cards' - The 2 cards that the player has in his hand.
        
        - 'best_hand' - The best 5 card hand that the player has based on the 5 community cards and his pocket cards
        
    
    The BotPlayer predefines the 'choose_action' method with whatever method we desire. We can pass said method either via the
    'predefine_choose_action' function or by passing the 'choose_action' in the constructor as a second parameter
    
    The HumanPlayer is a player who is controlled by a human through the console. 
    The default implementation contains some extra functions for receiving the input from the console and parsing it into commands.
    Unlike the BotPlayer, the 'choose_action' method is predefined only via the 'predefine_choose_action' function.
    
    However, like the BotPlayer, the 'choose_action' method can be predefined. The difference between predefining a human player's
    'choose action' and a BotPlayer's 'choose_action' is that, for the human player, the 'receive_input' function can be predefined.
    The 'receive_input' function gets the input from the console by default. By predefining it, we can simulate an actual human player
    typing the command in the console! 
    For example, if we try to force human player to make an illegal move, then we will get an infinite loop of the console 
    responding to us that the attempted move is illegal
    (I would have liked to raise an error in such cases, but I had no time to implement it).
    
    A bot player, on the other hand, can be forced to make even illegal actions (I wanted to raise an error for that as well).
    We also get the 'enter a command' prompt written on the console that we would normally get for a HumanPlayer,
    which we do not get for a bot player
    
    A 'choose action' function must look like this: 
        def choose_action(self: Player, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo) -> PlayerAction:
        
        *arguments:
            - 'self' - The player who calls the function.
            - 'possible_actions' - A list of the possible action types that the player can choose from.
            - 'action_info' - A somewhat DTO object which contains information that may be needed for the 'choose_action' method. 
                More info in the 'choose_action_info.py' module
    
    The ChooseActionFactory class contains some static methods for easily creating 'choose_action' functions.
    More info on these methods in the 'choose_action_factor.py' module
"""
```
bot_player_1 = BotPlayer(user_1) 
bot_player_2 = BotPlayer(user_2)
bot_player_3 = BotPlayer(user_3)
bot_player_4 = BotPlayer(user_4)
bot_player_5 = BotPlayer(user_5)
bot_player_6 = BotPlayer(user_6)

human_player_1 = HumanPlayer(user_1)
human_player_2 = HumanPlayer(user_2)
human_player_3 = HumanPlayer(user_3)
human_player_4 = HumanPlayer(user_4)
human_player_5 = HumanPlayer(user_5)
human_player_6 = HumanPlayer(user_6)

bot_player_1.predefine_choose_action(ChooseActionFactory.create_choose_action_always_random(
    [PlayerActionType.FOLD, PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
))
bot_player_2.predefine_choose_action(ChooseActionFactory.create_choose_action_always_random(
    [PlayerActionType.FOLD, PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
))
bot_player_3.predefine_choose_action(ChooseActionFactory.create_choose_action_always_random(
    [PlayerActionType.FOLD, PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
))
bot_player_4.predefine_choose_action(ChooseActionFactory.create_choose_action_always_random(
    [PlayerActionType.FOLD, PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
))
bot_player_5.predefine_choose_action(ChooseActionFactory.create_choose_action_always_random(
    [PlayerActionType.FOLD, PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
))
bot_player_6.predefine_choose_action(ChooseActionFactory.create_choose_action_always_random(
    [PlayerActionType.FOLD, PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
))
```

```
class ChooseActionFactory:

    @staticmethod
    def __create_action_command_string_human_player(action: PlayerAction) -> str:            
        predetermined_action_command_string = (
            {v: k for k, v in GameUI.PLAYER_COMMAND_ACTION_MAP.items()}[action.type]
        )

        predetermined_action_amount_string = str(action.amount) 

        predetermined_action_string = predetermined_action_command_string + " " + predetermined_action_amount_string

        return predetermined_action_string

    @staticmethod
    def __create_default_fake_receive_input_human_player(self: HumanPlayer, 
            possible_actions: List[PlayerActionType], 
            action_info: ChooseActionInfo,
            action_string: str) -> str:

        def fake_receive_input(*args, **kwargs) -> str:
                print(GameUI.choose_actions_command_prompt(self, possible_actions, action_info))
                return action_string

        return fake_receive_input

    """
        Creates a 'choose_action' with the list of given predetermined moves. 
        If one of these moves is illegal or otherwise fails the error handling checks, it will cause an infinite loop, so be wary. 
        
        If there are more moves than necessary given to the player, then these moves are ignored and the game continues as normal.
        (For example, specifying a fold action and then something else afterwards, obviously you cannot play after folding)
        
        If there are less moves than necessary, i.e. the player runs out of predetermined moves, then the default 'choose_action'
        method functionality is restored and any subsequent calls to it will trigger the player to have to enter the command manually
        from the console. This is useful if you want to partially simulate the player's actions up to a point 
    """
    @staticmethod
    def create_choose_action_predetermined_human_player(actions: List[(PlayerAction)]):
        action_index = 0
            
        def mock_choose_action(self: HumanPlayer, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo):
            nonlocal action_index     

            #If we have run out of predetermined moves, then give back control to the user
            if action_index >= len(actions):
                self.receive_input = self.original_receive_input

                return self.original_choose_action(possible_actions, action_info)

            predetermined_action = actions[action_index]
            predetermined_action_string = ChooseActionFactory.__create_action_command_string_human_player(predetermined_action)

            action_index += 1

            #Replace the receive_input function so that it gives us the appropriate preset input
            self.receive_input = ChooseActionFactory.__create_default_fake_receive_input_human_player(
                self, possible_actions, action_info,
                predetermined_action_string
            )

            #Call the original choose_action function which now has the fake_receive_input
            return self.original_choose_action(possible_actions, action_info)
        
        return mock_choose_action

    
    """
        Creates a 'choose_action' which will randomly select moves, with the exception of the specified excluded actions.
        If there are no legal actions for the player to make, then it will try to play the provided default action!
        If that action is also illegal, then this will cause an infinite loop.
        
        The All-In action can be forced if the raise action is legal and the amount to raise is >= user's money, regardless of
        whether or not it is in the excluded actions list! 
    """
    @staticmethod
    def create_choose_action_always_random_human_player(excluding_actions: List[PlayerActionType] = [], 
                                           back_up_action: PlayerActionType = PlayerActionType.FOLD) -> PlayerActionType:
        
        def mock_choose_action(self: HumanPlayer, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo):
            #Filter available actions
            possible_actions_filtered: List[PlayerActionType] = list(filter(lambda x: x not in excluding_actions, possible_actions))

            #Choose randomly
            action_type: PlayerActionType = None

            if len(possible_actions_filtered) == 0:
                action_type = back_up_action
            else:
                action_type = possible_actions_filtered[random.randint(0, len(possible_actions_filtered) - 1)] 

            min_bet_amount: float = action_info.pot.highest_bet_amount if action_info.game.settings.bet_minimum_enabled else 1

            amount: float = min(action_info.call_amount + (round(random.random() % 50 + min_bet_amount, 2)), self.user.money)

            if action_type == PlayerActionType.CALL:
                amount = action_info.call_amount
            elif action_type == PlayerActionType.ALL_IN:
                amount = self.user.money
            # Force an all-in if the action is a raise and the amount is equal to all the remaining money of the user
            # Regardless of whether or not the All-In is an excluded action 
            elif action_type == PlayerActionType.RAISE and amount == self.user.money:
                return PlayerAction(PlayerActionType.ALL_IN, amount)

            action = PlayerAction(action_type, amount)
            action_string = ChooseActionFactory.__create_action_command_string_human_player(action)

            # Replace the receive_input function so that it gives us the appropriate preset input
            self.receive_input = ChooseActionFactory.__create_default_fake_receive_input_human_player(
                self, possible_actions, action_info,
                action_string
            )

            return self.original_choose_action(possible_actions, action_info)

        return mock_choose_action

    """
        Creates a 'choose_action' with the list of given predetermined moves. 
        If one of these moves is illegal or otherwise fails the error handling checks, it will cause an infinite loop, so be wary. 
        
        If there are more moves than necessary given to the player, then these moves are ignored and the game continues as normal.
        (For example, specifying a fold action and then something else afterwards, obviously you cannot play after folding)
        
        If there are less moves than necessary, i.e. the player runs out of predetermined moves, then an error will occur! 
    """
    @staticmethod
    def create_choose_action_predetermined(actions: List[(PlayerAction)]):
        action_index = 0
            
        def mock_choose_action(self: Player, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo):
            nonlocal action_index     
            predetermined_action = actions[action_index]
            
            amount: float = predetermined_action.amount

            if predetermined_action.type == PlayerActionType.RAISE:
                amount += action_info.call_amount

            if predetermined_action.type == PlayerActionType.CALL:
                amount = action_info.call_amount

            action_index += 1
            
            return PlayerAction(predetermined_action.type, amount)
        
        return mock_choose_action

    """
        Creates a 'choose_action' which will randomly select moves, with the exception of the specified excluded actions.
        If there are no legal actions for the player to make, then it will try to play the provided default action!
        If that action is also illegal, then this will cause an infinite loop.
        
        The All-In action can be forced if the raise action is legal and the amount to raise is >= user's money, regardless of
        whether or not it is in the excluded actions list! 
    """
    @staticmethod
    def create_choose_action_always_random(excluding_actions: List[PlayerActionType] = [], 
                                           back_up_action: PlayerActionType = PlayerActionType.FOLD) -> PlayerActionType:
        
        def mock_choose_action(self: Player, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo):
            #Filter available actions
            possible_actions_filtered: List[PlayerActionType] = list(filter(lambda x: x not in excluding_actions, possible_actions))

            #Choose randomly
            action_type: PlayerActionType = None

            if len(possible_actions_filtered) == 0:
                action_type = back_up_action
            else:
                action_type = possible_actions_filtered[random.randint(0, len(possible_actions_filtered) - 1)] 

            min_bet_amount: float = action_info.pot.highest_bet_amount if action_info.game.settings.bet_minimum_enabled else 1

            amount: float = min(action_info.call_amount + (round(random.random() % 50 + min_bet_amount, 2)), self.user.money)

            if action_type == PlayerActionType.CALL:
                amount = action_info.call_amount
            elif action_type == PlayerActionType.ALL_IN:
                amount = self.user.money
            #Force an all-in if the action is a raise and the amount is equal to all the remaining money of the user
            elif action_type == PlayerActionType.RAISE and amount == self.user.money:
                return PlayerAction(PlayerActionType.ALL_IN, amount)

            return PlayerAction(action_type, amount)

        return mock_choose_action


    """
        Creates a 'choose_action' which will try to raise a random amount at all times.
        If raising is not possible, but betting is, then it will bet instead.
        If raising and betting is not possible, it will call instead.
        If raising, betting or calling is not possible, it will go all-in instead.
        
        If it tries raising an amount >= the users' money, then it will go all-in instead.
    """
    @staticmethod
    def create_choose_action_always_raise_if_possible() -> PlayerActionType:
        
        def mock_choose_action(self: Player, possible_actions: List[PlayerActionType], action_info: ChooseActionInfo):
            action_type: PlayerActionType = None
            
            if PlayerActionType.RAISE in possible_actions:        
                action_type = PlayerActionType.RAISE
            elif PlayerActionType.BET in possible_actions:
                action_type = PlayerActionType.BET
            elif PlayerActionType.CALL in possible_actions:
                action_type = PlayerActionType.CALL
            elif PlayerActionType.BET in possible_actions:
                action_type = PlayerActionType.ALL_IN

            if action_type == PlayerActionType.CALL:
                return PlayerAction(action_type, action_info.call_amount)
            elif action_type == PlayerActionType.ALL_IN:
                return PlayerAction(action_type, self.user.money)
    
            min_bet_amount = action_info.pot.highest_bet_amount if action_info.game.settings.bet_minimum_enabled else 1

            amount: float = round(min(action_info.call_amount + (random.random() % 50 + min_bet_amount), self.user.money), 2)

            if amount == self.user.money:
                action_type = PlayerActionType.ALL_IN

            return PlayerAction(action_type, amount)

        return mock_choose_action
```

"""
    The Deck class represents all of the 52 cards in a deck.
    It contains a method 'shuffle_deck', which determines the order of the cards in the deck. 
    The default implementation, that is, an instance created with Deck(), will randomly shuffle the deck
    
    The PresetDeck class represents a deck where the cards can be preset to be whatever is desired. It inherits from Deck.
    
    The constructor contains 2 parameters
        - 'players_count' - The number of players that will play in game with this deck
        - 'player_cards_count' - The number of cards each player has in their hand. 
            The program works correctly only when it is set to 2, as is the default for Texas Hold'em poker.
            
    The class also contains these important functions:
        - 'preset_player_cards' - Determines what cards each player will get.
            *arguments:
                - 'player_turn' - The index of the player from the list of players of the game who will receive the cards
                - 'cards' - The cards that the player will receiver
            
        - 'preset_community' - Determines what the community cards will be. 
            The community cards are the 5 cards that are dealt on the field.
            *arguments:
                - 'cards' - The community cards that will be dealt
            
        - 'preset_flop' - Determines what the cards dealt during the 'Flop' round will be.
            *arguments:
                - 'cards' - The cards that will be dealt
                
        - 'preset_turn' - Determines what the cards dealt during the 'Turn'(4th street) round will be.
            *arguments:
                - 'cards' - The cards that will be dealt
                
        - 'preset_river' - Determines what the cards dealt during the 'River' round will be.
            *arguments:
                - 'cards' - The cards that will be dealt
"""

"""
    The Hand class represents a players' 5 card hand.
    
    The constructor contains 1 parameter:
        - 'cards' - The cards that the hand will contain.
        
    The class contains the fields/properties:
        - 'cards' - The cards that the hand contains.

        - 'combination' - The combination that the hand has 
    
        - 'kickers_ranks' - The list of the kicker cards that the hand has. 
            These are used to decide tie breaks when the combinations are equal. They are different depending on the combination.
        
        - 'quads_rank' - The rank of the same 4 cards in a 4 of a kind combination. May be None if the combination is not 4 of a kind.
        
        - 'triple_rank' - The rank of the same 3 cards in a 3 of a kind combination. May be None if the combination is not 3 of a kind.
        
        - 'high_pair_rank' - The rank of the higher pair in a two pair combination, or the pair in a pair combiantion. 
            May be None if the combination is not a 2 pair or a pair.
        
        - 'low_pair_rank' - The rank of the lower pair in a two pair combination. May be None if the combination is not a 2 pair.
        
    The class contains these important functions:
        - 'set_hand_info' - Sets all the fields of the hand depending on the cards it has. Used for initialization in the constructor
        
        @static methods
        
        - 'compare_hands' - Compares 2 hands based on their strength. 
            Returns < 0 if the first has lower strength, > 0 if the second has lower strength, 0 if their strengths are equal.
            *arguments:
                - first - The first Hand
                - second - The second Hand
                
        - 'get_all_5_card_hands' - Returns a list of all 21 possible hands from a given list of 7 cards (5 community + 2 pocket)
            *arguments:
                - cards_list - The list of 7 cards.    
"""

```
preset_deck = PresetDeck(6, 2) # Deck() for default random deck, PresetEmptyDeck() for an empty deck

preset_deck.preset_player_cards(0, [
    Card(Rank.JACK, Suit.HEARTS),
    Card(Rank.FOUR, Suit.DIAMONDS)
])

preset_deck.preset_player_cards(1, [
    Card(Rank.ACE, Suit.CLUBS),
    Card(Rank.THREE, Suit.DIAMONDS)
])

preset_deck.preset_player_cards(2, [
    Card(Rank.SEVEN, Suit.CLUBS),
    Card(Rank.SEVEN, Suit.DIAMONDS)
])

preset_deck.preset_player_cards(3, [
    Card(Rank.EIGHT, Suit.CLUBS),
    Card(Rank.EIGHT, Suit.DIAMONDS)
])

preset_deck.preset_player_cards(4, [
    Card(Rank.ACE, Suit.SPADES),
    Card(Rank.ACE, Suit.SPADES)
])

preset_deck.preset_player_cards(5, [
    Card(Rank.ACE, Suit.SPADES),
    Card(Rank.ACE, Suit.SPADES)
])

preset_deck.preset_community(
    [
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.FIVE, Suit.HEARTS),
        Card(Rank.JACK, Suit.CLUBS),
        Card(Rank.NINE, Suit.DIAMONDS)
    ]
)
```

"""
    The GameSetting class contains variables which determine various settings for the game.    
    More info in the game_setting.py
"""

```
game_settings = (GameSetting()
            .enable_big_blind(50, 2)
            .enable_small_blind(25, 1)
            .enable_ante(10)
            .set_dealer(0)
            .enable_minimum_bet(50)
            .set_hand_visibility(HandVisibilitySetting.ALL)
            )

game_settings.set_deck(Deck())
# game_settings.set_deck(preset_deck)
```

"""
    The GameSetting class contains variables which determine various settings for the game:
        - deck - The Deck with which the game will be played
        
        - dealer_index - The index of the player who holds the so-called 'dealer button', i.e. the dealer. 
            In casinos, he doesn't actually deal the cards, but the 'dealer button' is still used.  
            The rounds typically start from the first player after the dealer, except for the Pre-Flop round
            (but only if there are small or big blinds)
        
        - small_blind_enabled - Determines whether or not there will be a small blind in the game
        - small_blind_bet - The amount of the small blind bet.
        - small_blind_holder - The index of the player who will have to pay the small blind in the game. 
            Typically that is the person right after the dealer!
            
        - big_blind_enabled - Determines whether or not there will be a big blind in the game
        - big_blind_bet - The amount of the big blind bet.
        - big_blind_holder - The index of the player who will have to pay the big blind in the game. 
            Typically that is the person right after the one who has to pay the small blind!
        
        - ante_enabled - Determines whether or not there will be antes in the game
        - ante_bet - The amount of the ante bet.
        
        - bet_maximum_enabled - Determines whether or not there will be a minimum amount by which to bet or raise
            Enabling this makes the game a typical No Limit game. Read https://en.wikipedia.org/wiki/Betting_in_poker#No_limit for info.
        - bet_minimum_amount - The min amount of the opening bet.
        
        - hand_visibility_setting - Determines which players' 2 card hand will be shown in the console upon being dealt.
            Check the 'hand_visibility_setting.py' module for more info!
"""

"""
    Determines which players' 2 card hand will be shown in the console upon being dealt.
    
        - ALL - Will show all players' hands in the console.
        - NONE - Will not show any players' hands in the console
        - HUMANS_ONLY - Will only show the human player's (instance of HumanPlayer) hands in the console.
        - BOTS_ONLY - Will only show the bot player's (intance of BotPlayer) hands in the console
"""

"""
    The Game class contains all the information needed to play a game.
    
    The constructor contains 1 parameter:
        - 'game_settings' - The settings that the game will use.
        
    The class contains the properties/fields :
        - 'settings' - The game settings for the game
        
        - 'turn' - The index of the player who has to play the current turn
        
        - 'community_cards' - The community cards for the game
        
        - 'pots' - All the pots of the game
        
        - 'current_pot_index' - The index of the most recent side pot of the game(i.e. the pot in which the players are currently actively betting)  
        
        - 'players' - The players who are playing in the game
        
        - 'round' - The current round of the game
        
        - 'table' - The table to which the game belongs. May be None if the game does not belong to any table.
        
        @properties
        
        - 'is_two_player_game' - returns True if the game consists of only 2 players, otherwise False.
        
        - 'current_pot' - returns the most recent side pot of the game(i.e. the pot in which the players are currently actively betting)
        
        - 'current_player' - returns the player whose turn it is to play
        
        - 'big_blind_player' - returns the player who has to pay the big blind. 
            If the big blind is not enabled, then behaviour is undefined.
            
        - 'small_blind_player' - returns the player who has to pay the small blind. 
            If the small blind is not enabled, then behaviour is undefined.
            
        - 'dealer_player' - returns the player who currently has the dealer button.
        
    The class contains these important functions:
        - 'add_player' - Adds a player to the game. 
            If the player does not have enough money to enter the game (because of big blinds, small blinds, antes etc...)
            then an InvalidMoneyForSettingsException exception is thrown
        
        - 'start_game' - Starts the game with the current players and settings
            *arguments:
                - 'initial_pot_money' - Determines the amount of money there is in the pot before the game starts.
                    Default is 0.
"""

"""
    The Pot class represents a betting pot that is part of a game.
        
    The class contains the fields/properties:
        - 'players' - The players that participate in the pot.

        - 'total_money' - The total money put into the pot.
    
        - 'current_highest_stake' - The highest player stake that has been put into the pot in the current round 
        
        - 'highest_bet_amount' - The highest bet/raise that has been made for this round.
        
        - 'player_who_opened_pot' - The player who most recently opened the pot for betting.
        
    The class contains this important function:
        - 'place_bet' - Places a bet in the pot, updating the inner pot state as necessary.
            *arguments:
                - player - The player who bets the money (more precisely, whose user bets the money)
                - amount - Amount to bet
                - settings - The game settings, in accordance with which to place the bet    
"""

"""
    Uncomment everything below to run and see an example of 6 human players playing the game. 
    Reduce the number of players as necessary by just not adding them. 
"""

```
# game_1 = Game(game_settings)
# game_1.add_player(human_player_1)
# game_1.add_player(human_player_2)
# game_1.add_player(human_player_3)
# game_1.add_player(human_player_4)
# game_1.add_player(human_player_5)
# game_1.add_player(human_player_6)

# game_1.start_game()
```

"""
    The Table class is a class for managing many games.
    
    The constructor contains 1 parameter:
        - game_settings - The settings that the games on this table will use.    
    
    The class contains the fields/properties:
        - 'game_settings' - The game settings that all future games on the table will abide by. 
    
        - 'users' - The list of users that are sat at the table
        
        - 'game_history' - A list of all the games that have been played on this table.
        
        - 'current_game' - The current game that is setup on the table. 
            It may not have been played yet, it may be played at the moment, or it may have already been finished.
        
        @properties
        
        - 'big_blind_user' - returns the user who has to pay the big blind. 
            If the big blind is not enabled, then returns None.
            
        - 'small_blind_user' - returns the user who has to pay the small blind. 
            If the small blind is not enabled, then returns None.
            
        - 'dealer_user' - returns the user who currently has the dealer button.
        
    The class contains these important functions:
        - 'add_user' - Adds a user to the table. 
            This does not automatically add a player to the games as well. 
            For each new game on the table, the players have to be added manually.
            
            @throws
            - InvalidMoneyForSettingsException - If the user does not have enough money to enter the game 
                (because of big blinds, small blinds, antes etc...)
                
        - 'remove_user' - Removes a user from the table. 
            The order of the dealer/big blind/small blind players is preserved accoding to the following link:
            https://laderalife.com/upload/FormsAndDocument/Document/2019-02/Ladera_Ranch_Poker_Club_-_Forward_Moving_Button%20(1).pdf
        
        - 'start_game' - Starts the game with the current players and settings
            *arguments:
                - 'initial_pot_money' - Determines the amount of money there is in the pot before the game starts.
                    Default is 0.
                    
        - 'rotate_button' - Moves the dealer button, the small blind button and the big blind button once to the next player.
            Directly alters the 'dealer_index', 'big_blind_holder' and 'small_blind_holder' fields of the game_settings 
            
"""

"""
    Uncomment everything below and run to see an example of making a tournament with many games played on one table, where the 
    dealer button and the blinds (if there are any, as per the game settings) are rotated and the blinds are raised after every 5 games.   
"""

```
# # Create a table and play games until there is a single winner left, while rotating the big and small blind buttons and increasing
# # The big and small blinds periodically

# table_1 = Table(game_settings)

# table_1.add_user(user_1)
# table_1.add_user(user_2)
# table_1.add_user(user_3)
# table_1.add_user(user_4)
# table_1.add_user(user_5)
# table_1.add_user(user_6)

# #Redirect output to a file for fun
# with open('tournament_games.txt', mode='w', encoding="utf-8") as sys.stdout:
#     print("The tournament begins!\n\n")

#     has_rotated_button: bool = False

#     while True:
#         game_settings.set_deck(Deck())
#         table_1.new_game()

#         removed_table_users = []
        
#         pot_start_money: float = 0

#         for i in range(0, len(table_1.users)):
#             user = table_1.users[i]

#             try:
#                 # You can uncomment this and comment the human player and have the players be bots instead
                
#                 bot_player = BotPlayer(user, ChooseActionFactory.create_choose_action_always_random(
#                             [PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
#                         ))

#                 table_1.current_game.add_player(bot_player)  

#                 # human_player = HumanPlayer(user)

#                 # human_player.predefine_choose_action(ChooseActionFactory.create_choose_action_always_random_human_player(
#                 #             [PlayerActionType.ALL_IN], PlayerActionType.ALL_IN
#                 #         ))

#                 # table_1.current_game.add_player(human_player)  

#             except InvalidMoneyForSettingsException as e:
#                 removed_table_users.append(user)
#                 print(f"\nPlayer: {user.name} has been eliminated from the tournament!!!\n")
                
#                 # Add the money left from the player into the next pot
#                 pot_start_money = round(pot_start_money + user.money, 2)
                
#                 print(f"Adding {user.money}$ to the stakes of the next pot!\n")

#         for user in removed_table_users:
#             table_1.remove_user(user)  
#             user.money = 0

#         if len(table_1.users) == 1:
#             print(f"The winner of the tournament is {table_1.users[0].name}!!! 0_0")
            
#             table_1.users[0].money = round(table_1.users[0].money + pot_start_money)
            
#             break

#         if has_rotated_button:
#             table_1.rotate_button()

#         # This is only possible if the tournament begins with 2 players only
#         if table_1.current_game.is_two_player_game and not has_rotated_button:
#             table_1.game_settings.set_small_blind_holder(0)
#             table_1.game_settings.set_big_blind_holder(1)

#         # Handle anomalies with the dealer, small_blind and big_blind holders when the game consists of only 2 players
#         if table_1.current_game.is_two_player_game:
#             if table_1.game_settings.dealer_index == table_1.game_settings.big_blind_holder:
#                 table_1.next_big_blind_holder()

#             if table_1.game_settings.small_blind_holder == table_1.game_settings.big_blind_holder:
#                 table_1.game_settings.set_small_blind_holder(table_1.game_settings.dealer_index)

#         print(f"{'*' * 100} Game #{len(table_1.game_history) + 1} {'*' * 100}")
#         table_1.start_game(pot_start_money)
#         print(f"{'*' * 100} End of Game #{len(table_1.game_history)} {'*' * 100}")

#         if not has_rotated_button:
#             has_rotated_button = True

#         if len(table_1.game_history) % 5 == 0:
#             if game_settings.big_blind_enabled:
#                 game_settings.big_blind_bet += 5

#                 if game_settings.small_blind_enabled:
#                     game_settings.small_blind_bet = game_settings.big_blind_bet / 2

#             elif game_settings.small_blind_enabled:
#                 game_settings.small_blind_bet += 2.5

#             print(f"\nBig blind increased to: {game_settings.big_blind_bet}")
#             print(f"Small blind increased to: {game_settings.small_blind_bet}\n")
        
total_money: float = round(
    user_1.money + 
    user_2.money +
    user_3.money +
    user_4.money +
    user_5.money +
    user_6.money, 2
)

# Assert that no money was lost during the course of the games
assert total_money == 6_000
```

"""
    Feel free to check out the test modules for other example of how to create games, players, decks, etc...
    
    The unit tests are not exhaustive because I did not have time to make them exhaustive. 
    Also, doing exhaustive tests for all cases in poker tough.
"""
