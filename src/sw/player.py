"""
Player module.

Provides Player class used to represent the player character.
"""


from sw.const.entity import CollisionGroup
from sw.character import Character


class Player(Character):
    """ Player character. """

    def __init__(self):
        super().__init__()
        self.add_collision_group(CollisionGroup.CHARACTER)
        self.add_collision_group(CollisionGroup.WALL)
        self.name = None
        self.species = None
        self.background = None
        self.xp = 0
        self.sight_range = 5

    #--------- death logic ---------#

    def death_action(self, state):
        """
        Do nothing, player death is handled by the flows directly.
        """
        pass


#--------- generating a player from a saved dict ---------#


def player_from_save(save):
    """
    Generate a player from a save.

    :param dict save: info used to regenerate the player.

    :return: a regenerated Player object.
    :rtype: Player
    """
    raise NotImplementedError


#--------- generating a player from scratch ---------#


def player_from_scratch(name, species, background):
    """
    Generate a player from user-supplied info.

    :param str name: the name of the player being created.
    :param species: the species the player will belong to.
    :type species: sw.species.Species
    :param background: player's background.
    :type background: sw.background.Background

    :return: a freshly created Player object.
    :rtype: Player
    """
    res = Player()
    res.name = name
    res.species = species
    res.background = background
    _apply_species(res)
    _apply_background(res)
    return res

def _apply_species(player):
    """
    Apply species' modifiers to a player.

    :param player: a player to apply the species modifiers to.
    :type player: Player
    """
    player.base_stats = player.species.base_stats
    player.add_innate_modifiers(*player.species.modifiers)

def _apply_background(player):
    """
    Apply background's modifiers to a player.

    :param player: a player to apply the background's modifiers to.
    :type player: Player
    """
    player.add_temp_modifiers(*player.background.modifiers)
