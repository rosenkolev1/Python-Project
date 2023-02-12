from typing import List

from src.game.deck.preset_deck import PresetDeck
from src.game.setting.game_setting import GameSetting
from src.game.setting.hand_visibility_setting import HandVisibilitySetting

def default_game_settings(preset_deck: PresetDeck) -> GameSetting:
    game_settings = (GameSetting()
        .enable_big_blind(50, 2)
        .enable_small_blind(25, 1)
        .set_dealer(0)
        .set_hand_visibility(HandVisibilitySetting.ALL)
        .set_deck(preset_deck))

    return game_settings