"""
AI module.

Provides AI class and several subclasses which evaluate the game state and
choose an action for a monster.
"""


from collections import deque


from multipledispatch import dispatch


import sw.const.ai as const

import sw.gamestate as gs
import sw.monster as mon
import sw.monster_interactions as mi


#--------- AI driver ---------#


def ai_turn(state, actions):
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
        monster.action_points += actions
        task = evaluate_ai_action(monster.ai, monster, state)
        mi.perform_task(monster, task[0], task[1:], state)


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
        self.last_tasks = deque(maxlen=const.REMEMBERED_TASKS_NUM)


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

    :return: a tuple with a task and its arguments
    :rtype: tuple
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
        return (const.Task.PURSUE, player)
    if ai.alarmed:
        return (const.Task.INVESTIGATE, ai.alarm_coordinates)
    return (const.Task.REST,)
