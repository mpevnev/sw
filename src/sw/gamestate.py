"""
Game state module.

Provides GameState class to bundle together information about player, world,
and various other game data.
"""


from collections import deque


class GameState():
    """ A container with all game information. """

    def __init__(self):
        self.data = None
        self.player = None
        self.world = None
        self.player_position = None
        self.turn = 0
        self.messages = None

    def current_overworld_header(self):
        """ Return the header of the area where the player is located. """
        return self.world.area_headers[self.player_position]


#--------- reading game state from a saved YAML dict ---------#


def game_state_from_save(gamedata, yaml_dict):
    """ Read game state from a saved YAML dict. """
    raise NotImplementedError


#--------- creating game state from bottom up ---------#


def game_state_from_scratch(gamedata, player, world):
    """ Create a GameState instance from separate parts. """
    res = GameState()
    res.data = gamedata
    res.player = player
    res.world = world
    res.player_position = (0, 0)
    res.turn = 0
    res.messages = deque(maxlen=gamedata.message_limit)
    return res
