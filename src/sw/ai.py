"""
AI module.

Provides AI class and several subclasses which evaluate the game state and
choose an action for a monster.
"""


from collections import deque


from multipledispatch import dispatch


import sw.const.ai as const

import sw.interaction.monster as mi

import sw.gamestate as gs
import sw.misc as misc
import sw.monster as mon


#--------- AI driver ---------#


def ai_turn(state):
    """
    Make AI-controlled entities do something.

    :param state: game state to be modified by the active entities.
    :type state: sw.gamestate.GameState
    :param int actions: the amount of action points to be added to the
    entities' action point pools.
    """
    if state.area is None:
        return
    for monster in state.area.all_monsters(True):
        if monster.hidden():
            continue
        monster.action_points += state.ai_action_points
        task = evaluate_ai_action(monster.ai, monster, state)
        if task[0] is const.Task.CARRY_ON:
            mi.carry_on(monster, state)
        else:
            mi.start_new_task(monster, task, state)
    state.ai_action_points = 0


#--------- AI selector ---------#


def create_ai(aitype):
    """
    Create an AI of appropriate type.

    :param str aitype: a type of an AI.

    :return: an AI of a given type.
    :rtype: AI

    :raises ValueError: on unknown AI type.
    """
    if aitype == const.AIType.MELEE_ZOMBIE.value:
        return MeleeZombie()
    raise ValueError(f"Unknown AI type '{aitype}'")


#--------- AI classes ---------#


class AI():
    """ A base class in the hierarchy of AI evaluators. """

    def __init__(self):
        self.alarmed = False
        self.alarm_coordinates = None
        self.chosen_path = None
        self.last_tasks = deque(maxlen=const.REMEMBERED_TASKS_NUM)

    def last_task(self):
        """
        :return: the last task the AI performed, or None if the task deque is
        empty.
        :rtype: const.Task or None
        """
        try:
            return self.last_tasks[-1]
        except IndexError:
            return None


class MeleeZombie(AI):
    """ A very dumb AI. """
    pass


#--------- evaluators - generic ---------#


@dispatch(AI, mon.Monster, gs.GameState)
def evaluate_ai_action(ai, monster, state):
    """
    AI evaluation, generic version.

    This thing is boring, it just rests always.

    :param AI ai: an AI to use.
    :param monster: a monster to evaluate a move for.
    :type monster: sw.monster.Monster
    :param state: a global environment to take into account.
    :type state: sw.gamestate.GameState

    :return: a tuple with a task and its arguments or None if the monster
    should carry on with whatever it's doing at the moment.
    :rtype: tuple or None
    """
    return (const.Task.REST,)


#--------- evaluators - Melee Zombie ---------#


@dispatch(MeleeZombie, mon.Monster, gs.GameState)
def evaluate_ai_action(ai, monster, state):
    """
    AI evaluation, stupid melee zombie version.
    """
    player = state.player
    if state.area.can_see(monster, *player.position):
        ai.alarmed = True
        ai.alarm_coordinates = player.position
        if monster.distance(player) == 1:
            return (const.Task.ATTACK, player)
        last_task = ai.last_task()
        if last_task is None or last_task[0] is not const.Task.PURSUE:
            ai.chosen_path = None
            return (const.Task.PURSUE, player)
        return (const.Task.CARRY_ON,)
    if ai.alarmed:
        last_task = ai.last_task()
        if (last_task is None
                or last_task[0] is not const.Task.INVESTIGATE
                or misc.dist(monster.position, ai.alarm_coordinates) <= 2):
            ai.chosen_path = None
            return (const.Task.INVESTIGATE, ai.alarm_coordinates)
        return (const.Task.CARRY_ON,)
    return (const.Task.REST,)
