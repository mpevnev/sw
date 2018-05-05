"""
Game data module.
"""


import sw.ai as ai
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

    def ai_by_id(self, ai_id):
        """
        Get an AI by its ID.

        :param str ai_id: the ID to look for.

        :return: an AI with the given ID.
        :rtype: sw.ai.AI

        :raises ValueError: if there's no AI with this ID.
        """
        return ai.create_ai(ai_id)

    def doodad_recipe_by_id(self, doodad_id):
        """
        Get a doodad recipe by its ID.

        :param str doodad_id: the ID to look for.

        :return: a doodad recipe with the given ID.
        :rtype: dict

        :raises ValueError: if there's no recipe with such ID.
        """
        import sw.const.doodad as constd
        for recipe in self.doodad_recipes:
            if recipe[constd.ID] == doodad_id:
                return recipe
        raise ValueError(f"Unknown doodad ID '{doodad_id}'")

    def monster_recipe_by_id(self, recipe_id):
        """
        Get a monster recipe by its ID.

        :param str recipe_id: the ID to look for.

        :return: a monster recipe with the given ID.
        :rtype: dict

        :raises ValueError: if there's no recipe with such ID.
        """
        import sw.const.monster as constm
        for recipe in self.monster_recipes:
            if recipe[constm.ID] == recipe_id:
                return recipe
        raise ValueError(f"Unknown monster ID '{recipe_id}'")

    def unique_recipe_by_id(self, recipe_id):
        """
        Get a unique monster's recipe by its ID.

        :param str recipe_id: the ID to look for.

        :return: a unique monster's recipe with the given ID.
        :rtype: dict

        :raises ValueError: if there's no recipe with such ID.
        """
        import sw.const.monster as constm
        for recipe in self.uniques_recipes:
            if recipe[constm.ID] == recipe_id:
                return recipe
        raise ValueError(f"Unknown unique ID '{recipe_id}'")


#--------- helper things ---------#


def _read_backgrounds():
    """
    Read backgrounds from the data files.
    
    :return: a backgrounds list.
    :rtype: list[sw.background.Background]
    """
    import sw.const.background as constbg
    res = [bg.Background(data) for data in misc.read([], "data", constbg.BACKGROUNDS_FILE)]
    return res


def _read_doodad_recipes():
    """
    Read doodad recipes from the data files.
    
    :return: a list of recipes.
    :rtype: list[dict]
    """
    import sw.const.doodad as constd
    res = misc.read([], "data", constd.DOODAD_RECIPES_FILE)
    return res


def _read_globals():
    """
    Read globals configuration parameters.
    
    :return: a dict with global configuration parameters.
    :rtype: dict
    """
    res = misc.read({}, "data", gv.GLOBALS_FILE)
    return res


def _read_monster_recipes():
    """
    Read monster recipes from the data files.

    :return: a list with recipes.
    :rtype: list[dict]
    """
    import sw.const.monster as constm
    res = misc.read([], "data", constm.MONSTER_RECIPES_FILE)
    return res


def _read_species():
    """
    Read species from the data files.
    
    :return: a list of species.
    :rtype: list[sw.species.Species]
    """
    import sw.const.species as constsp
    res = [sp.Species(data) for data in misc.read([], "data", constsp.SPECIES_FILE)]
    return res


def _read_strings():
    """
    Read strings from the data files.

    :return: a dict with strings.
    :rtype: dict(str, str)
    """
    import sw.const.strings as conststr
    res = misc.read({}, "data", conststr.STRINGS_FILE)
    return res


def _read_uniques_recipes():
    """
    Read unique monster recipes from the data files.
    
    :return: a list of uniques recipes.
    :rtype: list[dict]
    """
    import sw.const.monster as constm
    res = misc.read([], "data", constm.UNIQUES_RECIPES_FILE)
    return res
