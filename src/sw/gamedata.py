"""
Game data module.
"""


import sw.background as bg
import sw.const as const
import sw.misc as misc
import sw.species as sp


class GameData():
    """ A container for game data and strings. """

    def __init__(self):
        self.backgrounds = _read_backgrounds()
        self.doodad_recipes = _read_doodad_recipes()
        self.species = _read_species()
        self.strings = _read_strings()

    def doodad_by_id(self, doodad_id):
        """ Return a doodad recipe with the given ID. """
        import sw.const.doodad as constd
        for recipe in self.doodad_recipes:
            if recipe[constd.ID] == doodad_id:
                return recipe
        raise ValueError(f"Unknown doodad ID '{doodad_id}'")


#--------- helper things ---------#


def _read_backgrounds():
    """ Read backgrounds from the data files. """
    import sw.const.background as constbg
    res = [bg.Background(data) for data in misc.read([], "data", constbg.BACKGROUNDS_FILE)]
    return res


def _read_doodad_recipes():
    """ Read doodad recipes from the data files. """
    import sw.const.doodad as constd
    res = misc.read([], "data", constd.DOODAD_RECIPES_FILE)
    return res


def _read_species():
    """ Read species from the data files. """
    import sw.const.species as constsp
    res = [sp.Species(data) for data in misc.read([], "data", constsp.SPECIES_FILE)]
    return res


def _read_strings():
    """ Read strings from the data files. """
    res = {}
    return res
