"""
Doodad classes bank.
"""


from sw.doodad import Doodad


#--------- wall types ---------#


class Wall(Doodad):
    """ A superclass for wall doodads. """

    def use_by_monster(self, monster, state, area, ui):
        return False

    def use_by_player(self, player, state, area, ui):
        return False

    def death_action(self, state, area, ui):
        pass
