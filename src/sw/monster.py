"""
Monster module.

Provides base Monster class and several subclasses.
"""


import random as rand


from sw.ai import select_ai
from sw.character import Character
from sw.const.message import Channel
import sw.const.ai as aiconst
import sw.const.area as arconst
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
        self.see_through_types = set()
        self.xp_award = 0

    #--------- stuff inherited from Entity ---------#

    def add_to_area(self, area):
        area.monsters.append(self)

    def remove_from_area(self, area):
        area.monsters.remove(self)

    def death_action(self, state):
        visinfo = state.area.visibility_matrix[self.position]
        visible = arconst.VisibilityLevel.VISIBLE in visinfo.levels
        if self.do_award_xp:
            state.player.xp += self.xp_award
        if visible:
            ui.message(self.death_message, Channel.MONSTER_DEATH)
            ui.death_animation(self)
        elif self.do_award_xp:
            ui.message(state.data.strings[conststr.FEEL_MORE_EXPERIENCED], Channel.NORMAL)

    #--------- visibility logic ---------#

    def can_see_through(self, entity):
        return entity.transparent_for_monster(self)

    #--------- other logic ---------#

    def alarm(self):
        """ Raise the AI 'alarmed' flag. """
        self.ai.alarmed = True

    def perform_task(self, task, state):
        """
        Perform a task.

        :param task: a task to be performed with arguments.
        :type task: tuple(aiconst.Task, ...)
        :param state: a global game environment the monster may factor in when
        executing the task.
        :type state: sw.gamestate.GameState

        :raises ValueError: if the task to be performed is unknown.
        """
        taskid = task[0]
        if taskid == aiconst.Task.ATTACK:
            self.attack(task[1], state)
        elif taskid == aiconst.Task.CAST_SPELL:
            self.cast_spell(task[1], task[2], state)
        elif taskid == aiconst.Task.EXPLORE:
            self.explore(state)
        elif taskid == aiconst.Task.FOLLOW:
            self.follow(task[1], state)
        elif taskid == aiconst.Task.INVESTIGATE:
            self.investigate(task[1], state)
        elif taskid == aiconst.Task.PURSUE:
            self.pursue(task[1], state)
        elif taskid == aiconst.Task.REST:
            self.rest(state)
        elif taskid == aiconst.Task.RETREAT:
            self.retreat(state)
        elif taskid == aiconst.Task.STEP_ASIDE:
            self.step_aside(state)
        else:
            raise ValueError(f"Unknown task '{taskid}")

    #--------- task implementations ---------#

    def attack(self, target, state):
        """
        Attack a given character.

        :param target: what to attack.
        :type target: sw.character.Character
        :param state: a global game state that the monster might factor in when
        attacking.
        :type state: sw.gamestate.GameState
        """
        raise NotImplementedError

    def cast_spell(self, target, spell, state):
        """
        Cast a given spell at a given target.

        :param target: position at which to cast.
        :type target: tuple(int, int)
        :param spell: which spell to cast.
        :type spell: sw.spell.Spell
        :param state: a global game state that the monster might factor in when
        casting a spell.
        :type state: sw.gamestate.GameState
        """
        raise NotImplementedError

    def explore(self, state):
        """
        Explore the floor.

        :param state: a global game state that the monster can factor in when
        exploring.
        :type state: sw.gamestate.GameState
        """
        raise NotImplementedError

    def follow(self, who, state):
        """
        Follow a friendly character somewhere.

        :param who: follow who.
        :type who: sw.const.Character
        :param state: a global game state that the monster can factor in when
        following.
        :type state: sw.gamestate.GameState
        """
        raise NotImplementedError

    def investigate(self, x, y, state):
        """
        Look around a given position.

        :param int x: X coordinate of a point to investigate.
        :param int y: Y coordinate of a point to investigate.
        :param state: a global game state that the monster might factor in when
        investigating.
        :type state: sw.gamestate.GameState
        """
        raise NotImplementedError

    def pursue(self, who, state):
        """
        Pursue a hostile character.

        :param who: pursue who.
        :type who: sw.character.Character
        :param state: a global game state that the monster might factor in when
        pursuing.
        :type state: sw.gamestate.GameState
        """
        raise NotImplementedError

    def rest(self, state):
        """
        Do nothing, just regenerate.

        :param state: a global game state that the monster might factor in when
        resting.
        :type state: sw.gamestate.GameState
        """
        raise NotImplementedError

    def retreat(self, state):
        """
        Find a safe spot away from enemies.

        :param state: a global game state that the monster might factor in when
        retreating.
        :type state: sw.gamestate.GameState
        """
        raise NotImplementedError

    def step_aside(self, state):
        """
        Let allies pass through the position this monster currenly occupies.

        :param state: a global game state that the monster can factor in when
        stepping aside
        :type state: sw.gamestate.GameState
        """
        raise NotImplementedError


#--------- subclasses ---------#


class GenericMonster(Monster):
    """
    A generic monster with no special attributes or behaviour.
    """

    #--------- tasks ---------#

    def attack(self, target, state):
        pass

    def cast_spell(self, target, spell, state):
        pass

    def explore(self, state):
        state.area.shift_entity(self, rand.randint(-1, 1), rand.randint(-1, 1))

    def follow(self, who, state):
        dx = 1 if who.position[0] - self.position[0] >= 0 else -1
        dy = 1 if who.position[1] - self.position[1] >= 0 else -1
        state.area.shift_entity(self, dx, dy)

    def investigate(self, x, y, state):
        pass

    def pursue(self, who, state):
        dx = 1 if who.position[0] - self.position[0] >= 0 else -1
        dy = 1 if who.position[1] - self.position[1] >= 0 else -1
        state.area.shift_entity(self, dx, dy)

    def rest(self, state):
        pass

    def retreat(self, state):
        dx = -1 if state.player.position[0] - self.position[0] >= 0 else 1
        dy = -1 if state.player.position[1] - self.position[1] >= 0 else 1
        state.area.shift_entity(self, dx, dy)

    def step_aside(self, state):
        pass


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
        _read_common_recipe_parameters(res, recipe)
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


def _read_common_recipe_parameters(monster, recipe):
    """
    Read common parameters from a recipe into a Monster instance.

    :param Monster monster: read into.
    :param dict recipe: read from.
    """
    monster.ai = select_ai(recipe[const.AI_TYPE])
    #
    monster.base_skills = misc.convert_skill_dict(recipe[const.SKILLS])
    monster.base_stats = misc.convert_stat_dict(recipe[const.STATS])
    monster.death_message = recipe[const.DEATH_MESSAGE]
    monster.xp_award = recipe[const.XP_AWARD]
