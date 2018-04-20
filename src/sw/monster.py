"""
Monster module.

Provides base Monster class.
"""


from sw.character import Character


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
        ui.message(self.death_message)
        ui.death_animation(self)
        if self.do_award_xp:
            state.player.xp += self.xp_award

    #--------- visibility logic ---------#

    def can_see_through(self, entity):
        return entity.transparent_for_monster(self)
