"""
Doodad constants.
"""


from enum import Enum


DOODAD_RECIPES_FILE = "doodads.yaml"


class DoodadType(Enum):
    """ Doodad types enum. """

    WALL = "wall"


# Recipe and save dicts keys
ID = "id"
TYPE = "type"
