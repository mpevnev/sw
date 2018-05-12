"""
Monster module.

Provides base Monster class and several subclasses.
"""


import random as rand


from sw.character import Character
from sw.const.message import Channel
import sw.const.ai as aiconst
import sw.const.entity as entconst
import sw.const.visibility as visconst
import sw.const.monster as const
import sw.const.strings as conststr
import sw.misc as misc


#--------- base class ---------#


class Monster(Character):
    """ A monster or some other NPC. """

    def __init__(self, recipe_id):
        """
        Initialize a monster.

        :param string recipe_id: ID of the recipe from which the monster is
        being created.
        """
        super().__init__()
        self.recipe_id = recipe_id
        self.action_points = 0
        self.ai = None
        self.death_message = None
        self.do_award_xp = True
        self.xp_award = 0
        self.add_blocked_by(entconst.CollisionGroup.CHARACTER)
        self.add_blocks(entconst.CollisionGroup.CHARACTER)

    #--------- stuff inherited from Entity ---------#

    def death_action(self, state):
        visinfo = state.area.visibility_matrix[self.position]
        visible = visconst.VisibilityLevel.VISIBLE in visinfo.levels
        if self.do_award_xp:
            state.player.xp += self.xp_award
        if visible:
            state.ui.message(self.death_message, Channel.MONSTER_DEATH)
            state.ui.death_animation(self)
        elif self.do_award_xp:
            state.ui.message(state.data.strings[conststr.FEEL_MORE_EXPERIENCED], 
                             Channel.MONSTER_DEATH)

    #--------- other logic ---------#

    def alarm(self):
        """ Raise the AI 'alarmed' flag. """
        self.ai.alarmed = True


#--------- subclasses ---------#


class GenericMonster(Monster):
    """
    A generic monster with no special attributes or behaviour.
    """

    def __init__(self, recipe_id):
        super().__init__(recipe_id)
        self.add_blocked_by(entconst.CollisionGroup.WALL)


#--------- monster creation from recipes ---------#


def monster_from_recipe(recipe, other_game_data):
    """
    Create a monster from a recipe (and maybe use some other game data).

    :param dict recipe: a recipe to base the new monster on.
    :param other_game_data: game data to use when populating the monster.
    :type other_game_data: sw.gamedata.GameData

    :return: the freshly created monster.
    :rtype: Monster
    """
    recipe_id = recipe[const.ID]
    montype = recipe[const.TYPE]
    if montype == const.MonsterType.GENERIC.value:
        res = GenericMonster(recipe_id)
        _read_common_recipe_parameters(res, recipe, other_game_data)
        return res
    raise ValueError(f"Unknown monster type '{montype}'")


#--------- monster creation from saves ---------#


def monster_from_save(save):
    """
    Create a monster from a save.

    :param dict save: a dictionary with the info about a saved monster.

    :return: a regenerated monster
    :rtype: Monster
    """
    raise NotImplementedError


#--------- helper things ---------#


def _read_common_recipe_parameters(monster, recipe, other_game_data):
    """
    Read common parameters from a recipe into a Monster instance.

    :param Monster monster: read into.
    :param dict recipe: read from.
    """
    monster.ai = other_game_data.ai_by_id(recipe[const.AI_TYPE])
    #
    monster.base_skills = misc.convert_skill_dict(recipe[const.SKILLS])
    monster.base_stats = misc.convert_stat_dict(recipe[const.STATS])
    monster.death_message = recipe[const.DEATH_MESSAGE]
    monster.xp_award = recipe[const.XP_AWARD]
