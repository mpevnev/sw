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


#--------- base class ---------#


class Monster(Character):
    """ A monster or some other NPC. """

    def __init__(self, recipe_id):
        super().__init__()
        self.recipe_id = recipe_id
        self.action_points = 0
        self.ai = None
        self.do_award_xp = True
        self.xp_award = 0
        self.death_message = None
        self.see_through_types = set()

    #--------- stuff inherited from Entity ---------#

    def add_to_area(self, area):
        area.monsters.append(self)

    def remove_from_area(self, area):
        area.monsters.remove(self)

    def death_action(self, state, area, ui):
        visinfo = area.visibility_matrix[self.position]
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

    def perform_task(self, task, state, area, ui):
        """ Perform a given task. """
        taskid = task[0]
        if taskid == aiconst.Task.ATTACK:
            self.attack(state, area, ui, task[1])
        elif taskid == aiconst.Task.CAST_SPELL:
            self.cast_spell(state, area, ui, task[1], task[2])
        elif taskid == aiconst.Task.EXPLORE:
            self.explore(state, area, ui)
        elif taskid == aiconst.Task.FOLLOW:
            self.follow(state, area, ui, task[1])
        elif taskid == aiconst.Task.INVESTIGATE:
            self.investigate(state, area, ui, task[1])
        elif taskid == aiconst.Task.PURSUE:
            self.pursue(state, area, ui, task[1])
        elif taskid == aiconst.Task.REST:
            self.rest(state, area, ui)
        elif taskid == aiconst.Task.RETREAT:
            self.retreat(state, area, ui)
        elif taskid == aiconst.Task.STEP_ASIDE:
            self.step_aside(state, area, ui)
        else:
            raise ValueError(f"Unknown task '{taskid}")

    def tick(self, state, area, player, ui):
        raise NotImplementedError

    #--------- task implementations ---------#

    def attack(self, state, area, ui, target):
        """ Attack a given character. """
        raise NotImplementedError

    def cast_spell(self, state, area, ui, spell, target):
        """ Cast a given spell at a given target. """
        raise NotImplementedError

    def explore(self, state, area, ui):
        """ Explore the floor. """
        raise NotImplementedError

    def follow(self, state, area, ui, who):
        """ Follow a friendly character somewhere. """
        raise NotImplementedError

    def investigate(self, state, area, ui, position):
        """ Look aroung a given position. """
        raise NotImplementedError

    def pursue(self, state, area, ui, who):
        """ Pursue a hostile character. """
        raise NotImplementedError

    def rest(self, state, area, ui):
        """ Do nothing, just regenerate. """
        raise NotImplementedError

    def retreat(self, state, area, ui):
        """ Find a safe spot away from enemies. """
        raise NotImplementedError

    def step_aside(self, state, area, ui):
        """
        Let allies pass through the position this monster currenly occupies.
        """
        raise NotImplementedError


#--------- subclasses ---------#


class GenericMonster(Monster):
    """
    A generic monster with no special attributes or behaviour.
    """

    def tick(self, state, area, player, ui):
        pass

    #--------- tasks ---------#

    def attack(self, state, area, ui, target):
        pass

    def cast_spell(self, state, area, ui, spell, target):
        pass

    def explore(self, state, area, ui):
        area.shift_entity(self, rand.randint(-1, 1), rand.randint(-1, 1))

    def follow(self, state, area, ui, who):
        dx = 1 if who.position[0] - self.position[0] >= 0 else -1
        dy = 1 if who.position[1] - self.position[1] >= 0 else -1
        area.shift_entity(self, dx, dy)

    def investigate(self, state, area, ui, position):
        pass

    def pursue(self, state, area, ui, who):
        dx = 1 if who.position[0] - self.position[0] >= 0 else -1
        dy = 1 if who.position[1] - self.position[1] >= 0 else -1
        area.shift_entity(self, dx, dy)

    def rest(self, state, area, ui):
        pass

    def retreat(self, state, area, ui):
        dx = -1 if state.player.position[0] - self.position[0] >= 0 else 1
        dy = -1 if state.player.position[1] - self.position[1] >= 0 else 1
        area.shift_entity(self, dx, dy)

    def step_aside(self, state, area, ui):
        pass


#--------- monster creation from recipes ---------#


def monster_from_recipe(recipe, other_game_data):
    """
    Create a monster from a recipe (and maybe use some other game data).
    """
    recipe_id = recipe[const.ID]
    montype = recipe[const.TYPE]
    if montype == const.MonsterType.GENERIC.value:
        res = GenericMonster(recipe_id)
        _read_common_recipe_parameters(res, recipe)
        return res
    raise ValueError(f"Unknown monster type '{montype}'")


#--------- monster creation from saves ---------#


def monster_from_save(save_dict):
    """ Create a monster from a saved dict. """
    raise NotImplementedError


#--------- helper things ---------#


def _read_common_recipe_parameters(monster, recipe):
    """ Read common parameters from a recipe into a Monster instance. """
    monster.ai = select_ai(recipe[const.AI_TYPE])
    monster.xp_award = recipe[const.XP_AWARD]
    monster.death_message = recipe[const.DEATH_MESSAGE]
