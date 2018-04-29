"""
Game data module.
"""


import sw.background as bg
import sw.const.globvars as gv
import sw.misc as misc
import sw.species as sp


class GameData():
    """ A container for game data and strings. """

    def __init__(self):
        self.backgrounds = _read_backgrounds()
        self.doodad_recipes = _read_doodad_recipes()
        self.monster_recipes = _read_monster_recipes()
        self.species = _read_species()
        self.strings = _read_strings()
        self.uniques_recipes = _read_uniques_recipes()
        globvars = _read_globals()
        self.message_limit = globvars[gv.MESSAGE_LIMIT]

    def doodad_recipe_by_id(self, doodad_id):
        """ Return a doodad recipe with the given ID. """
        import sw.const.doodad as constd
        for recipe in self.doodad_recipes:
            if recipe[constd.ID] == doodad_id:
                return recipe
        raise ValueError(f"Unknown doodad ID '{doodad_id}'")

    def monster_recipe_by_id(self, recipe_id):
        """ Return a monster recipe with the given ID. """
        import sw.const.monster as constm
        for recipe in self.monster_recipes:
            if recipe[constm.ID] == recipe_id:
                return recipe
        raise ValueError(f"Unknown monster ID '{recipe_id}'")

    def unique_recipe_by_id(self, recipe_id):
        """ Return a unique monster recipe with the given ID. """
        import sw.const.monster as constm
        for recipe in self.uniques_recipes:
            if recipe[constm.ID] == recipe_id:
                return recipe
        raise ValueError(f"Unknown unique ID '{recipe_id}'")


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


def _read_globals():
    """ Read globals configuration parameters. """
    res = misc.read({}, "data", gv.GLOBALS_FILE)
    return res


def _read_monster_recipes():
    """ Read monster recipes from the data files. """
    import sw.const.monster as constm
    res = misc.read([], "data", constm.MONSTER_RECIPES_FILE)
    return res


def _read_species():
    """ Read species from the data files. """
    import sw.const.species as constsp
    res = [sp.Species(data) for data in misc.read([], "data", constsp.SPECIES_FILE)]
    return res


def _read_strings():
    """ Read strings from the data files. """
    import sw.const.strings as conststr
    res = misc.read({}, "data", conststr.STRINGS_FILE)
    return res


def _read_uniques_recipes():
    """ Read unique monster recipes from the data files. """
    import sw.const.monster as constm
    res = misc.read([], "data", constm.UNIQUES_RECIPES_FILE)
    return res
