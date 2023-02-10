from typing import List

from src.game.deck.preset_deck import PresetDeck
from src.game.setting.game_setting import GameSetting
from src.game.setting.hand_visibility_setting import HandVisibilitySetting

def default_game_settings(preset_deck: PresetDeck) -> GameSetting:
    game_settings = GameSetting()
    game_settings.enable_big_blind(50)
    game_settings.enable_small_blind(25)
    game_settings.set_dealer(0)
    game_settings.set_small_blind_holder(1)
    game_settings.set_big_blind_holder(2)
    game_settings.set_hand_visibility(HandVisibilitySetting.ALL)
    game_settings.set_deck(preset_deck)

    return game_settings