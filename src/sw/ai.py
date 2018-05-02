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

    def evaluate(self, monster, state):
        """
        Choose and return a task (with whatever arguments it requires in a
        tuple) for the monster, given a specific environment.

        :param monster: the monster for which the AI should calculate the task.
        :type monster: sw.monster.Monster
        :param state: the global environment of the monster that the AI should
        take into account.
        :type state: sw.gamestate.GameState
        """
        raise NotImplementedError


#--------- concrete classes ---------#


class MeleeZombie(AI):
    """ A very dumb AI. """

    def evaluate(self, monster, state):
        player = state.player
        if state.area.can_see(monster, *player.position):
            self.alarmed = True
            if monster.distance(player) == 1:
                return (const.Task.ATTACK, player)
            return (const.Task.PURSUE, player)
        if self.alarmed:
            return (const.Task.INVESTIGATE, self.alarm_coordinates)
        return (const.Task.REST,)


#--------- AI selector ---------#


def select_ai(of_type):
    """
    Return an instance of a specific AI subclass.
    
    :param str of_type: a string with the type of the resulting AI.
    """
    if of_type == const.AIType.MELEE_ZOMBIE.value:
        return MeleeZombie()
    raise ValueError(f"Unknown AI type '{of_type}'")
