"""
Monster module.

Provides base Monster class and several subclasses.
"""


from sw.character import Character
from sw.const.message import Channel
import sw.const.monster as const


#--------- base class ---------#


class Monster(Character):
    """ A monster or some other NPC. """

    def __init__(self, recipe_id):
        super().__init__()
        self.recipe_id = recipe_id
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
        ui.message(self.death_message, Channel.MONSTER_DEATH)
        ui.death_animation(self)
        if self.do_award_xp:
            state.player.xp += self.xp_award

    #--------- visibility logic ---------#

    def can_see_through(self, entity):
        return entity.transparent_for_monster(self)

    #--------- other logic ---------#

    def tick(self, state, area, player, ui):
        raise NotImplementedError


#--------- subclasses ---------#


class NormalMeleeMonster(Monster):
    """
    A monster with normal melee AI.
    """

    def tick(self, state, area, player, ui):
        pass


#--------- monster creation from recipes ---------#


def monster_from_recipe(recipe, other_game_data):
    """
    Create a monster from a recipe (and maybe use some other game data).
    """
    recipe_id = recipe[const.ID]
    montype = recipe[const.TYPE]
    if montype == const.MonsterType.NORMAL_MELEE.value:
        return NormalMeleeMonster(recipe_id)
    raise ValueError(f"Unknown monster type '{montype}'")


#--------- monster creation from saves ---------#


def monster_from_save(save_dict):
    """ Create a monster from a saved dict. """
    raise NotImplementedError
