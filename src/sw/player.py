"""
Player module.

Provides Player class used to represent the player character.
"""


from sw.character import Character


class Player(Character):
    """ Player character. """

    def __init__(self):
        super().__init__()
        self.name = None
        self.species = None
        self.background = None

    def death_action(self, state, area, ui):
        """
        Do nothing, player death is handled by the flows directly.
        """
        pass


#--------- generating a player from a saved dict ---------#


def player_from_data(data):
    """ Generate a player from a YAML dict. """
    raise NotImplementedError


#--------- generating a player from scratch ---------#


def player_from_scratch(name, species, background):
    """ Generate a player from user-supplied info. """
    res = Player()
    res.name = name
    res.species = species
    res.background = background
    _apply_species(res)
    _apply_background(res)
    return res

def _apply_species(player):
    """ Apply species' modifiers to the player. """
    player.add_innate_modifiers(*player.species.modifiers)

def _apply_background(player):
    """ Apply background's modifiers to the player. """
    player.add_temp_modifiers(*player.background.modifiers)
