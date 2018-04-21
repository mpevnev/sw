"""
AI module.

Provides AI class and several subclasses which evaluate the game state and
choose an action for a monster.
"""


from collections import deque


import sw.const.ai as const


#--------- base class ---------#


class AI():
    """ A base class in the hierarchy of AI evaluators. """

    def __init__(self):
        self.alarmed = False
        self.alarm_coordinates = None
        self.last_tasks = deque(maxlen=const.REMEMBERED_TASKS_NUM)

    def evaluate(self, monster, state, area):
        """
        Choose and return a task (with whatever arguments it requires in a
        tuple) for the monster, given a specific environment.
        """
        raise NotImplementedError


#--------- concrete classes ---------#


class MeleeZombie(AI):
    """ A very dumb AI. """

    def evaluate(self, monster, state, area):
        player = state.player
        if area.can_see(monster, *player.position):
            self.alarmed = True
            if monster.distance(player) == 1:
                return (const.Task.ATTACK, player)
            return (const.Task.PURSUE, player)
        if self.alarmed:
            return (const.Task.INVESTIGATE, self.alarm_coordinates)
        return (const.Task.REST,)


#--------- AI selector ---------#


def select_ai(of_type):
    """ Return an instance of a specific AI subclass. """
    if of_type == const.AIType.MELEE_ZOMBIE.value:
        return MeleeZombie()
    raise ValueError(f"Unknown AI type '{of_type}'")
