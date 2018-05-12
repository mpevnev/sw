"""
Monster interactions module.

Provides several functions for interacting with (or by) monsters.
"""


import random


from multipledispatch import dispatch


import sw.character as c
import sw.doodad as d
import sw.gamestate as gs
import sw.item as i
import sw.misc as misc
import sw.monster as m
import sw.player as p
import sw.spell as s

import sw.const.ai as constai
from sw.const.message import Channel
import sw.const.skill as skill
import sw.const.stat as stat


#--------- performing AI tasks - main functions ---------#


def carry_on(monster, state):
    """
    Make a monster continue with its current task.

    :param monster: a monster to go on.
    :type monster: sw.monster.Monster
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: amount of action points required to perform the current task or
    None if either there's no task or the monster doesn't have enough AP to
    perform it.
    :rtype: float or None
    """
    last_task = monster.ai.last_task()
    if last_task is None:
        return None
    return perform_task(monster, last_task[0], last_task[1:], state)


def perform_task(monster, task, taskargs, state):
    """
    Make a monster perform some AI-assigned task.

    :param monster: a monster to perform the task.
    :type monster: sw.monster.Monster
    :param task: a task to perform.
    :type task: sw.const.ai.Task
    :param tuple taskargs: arguments for the task, if any.
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :raises ValueError: if the task is unknown.

    :return: amount of action points required to perform the current task or
    None if either there's no task or the monster doesn't have enough AP to
    perform it.
    :rtype: float or None
    """
    if task is constai.Task.ATTACK:
        return attack(monster, taskargs[0], state)
    elif task is constai.Task.CAST_SPELL:
        return cast_spell(monster, taskargs[0], taskargs[1], state)
    elif task is constai.Task.EXPLORE:
        return explore(monster, state)
    elif task is constai.Task.FOLLOW:
        return follow(monster, taskargs[0], state)
    elif task is constai.Task.INVESTIGATE:
        return investigate(monster, *taskargs[0], state)
    elif task is constai.Task.PURSUE:
        return pursue(monster, taskargs[0], state)
    elif task is constai.Task.REST:
        return rest(monster, state)
    elif task is constai.Task.RETREAT:
        return retreat(monster, state)
    elif task is constai.Task.STEP_ASIDE:
        return step_aside(monster, state)
    elif task is constai.Task.WAIT:
        return None
    else:
        raise ValueError(f"Unknown task '{task}'")


def start_new_task(monster, task_and_args, state):
    """
    Make a monster start some new activity.

    :param monster: a monster to perform the task.
    :type monster: sw.monster.Monster
    :param tuple task_and_args: a task to perform with its arguments.
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: amount of action points required to perform the current task or
    None if either there's no task or the monster doesn't have enough AP to
    perform it.
    :rtype: float or None
    """
    monster.ai.last_tasks.append(task_and_args)
    return perform_task(monster, task_and_args[0], task_and_args[1:], state)


#--------- monster attacks ---------#


@dispatch(m.Monster, c.Character, gs.GameState)
def attack(monster, attack_who, state):
    """
    Attack someone, generic version.

    :param monster: who is doing the attacking bit.
    :type monster: sw.monster.Monster
    :param attack_who: who is getting attacked.
    :type attack_who: sw.character.Character
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: amount of spent AP, or None if there weren't enough AP to attack.
    :rtype: float or None
    """
    if monster.has_melee_weapon_equipped():
        weapon = random.choice(filter(None, monster.melee_weapons()))
        cost = attack_speed(monster, weapon, state)
        if cost > monster.action_points:
            return None
        state.ui.message("FIXME: generic attack with a weapon", None)
        return cost
    cost = attack_speed(monster, state)
    if cost > monster.action_points:
        return None
    state.ui.message("FIXME: generic attack without a weapon", None)
    return cost


#--------- monster spellcasting ---------#


@dispatch(m.Monster, s.Spell, object, gs.GameState)
def cast_spell(monster, which_spell, target, state):
    """
    Cast a spell, generic version.

    :param monster: who is casting.
    :type monster: sw.monster.Monster
    :param which_spell: which spell is being cast.
    :type which_spell: sw.spell.Spell
    :param target: the target of the spell.
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: amount of spent AP or None on failure.
    :rtype: float or None
    """
    state.ui.message("FIXME: generic spell cast", None)
    return None


#--------- monster exploration ---------#


@dispatch(m.Monster, gs.GameState)
def explore(monster, state):
    """
    Explore the area.

    :param monster: who is exploring.
    :type monster: sw.monster.Monster
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: amount of spent AP or None on failure.
    :rtype: float or None
    """
    state.ui.message("FIXME: generic monster explore", None)
    return None


#--------- monsters following others ---------#


@dispatch(m.Monster, c.Character, gs.GameState)
def follow(monster, other, state):
    """
    Follow someone.

    :param monster: who is following.
    :type monster: sw.monster.Monster
    :param other: who is being followed
    :type other: sw.character.Character
    :param state: a global environment
    :type state: sw.gamestate.GameState

    :return: amount of spent AP or None on failure.
    :rtype: float or None
    """
    state.ui.message("FIXME: generic monster follow", None)
    return None


#--------- monsters investigating ---------#


@dispatch(m.Monster, int, int, gs.GameState)
def investigate(monster, x, y, state):
    """
    Investigate a spot.

    :param monster: who is investigating.
    :type monster: sw.monster.Monster
    :param int x: X coordinate of a spot to investigate.
    :param int y: Y coordinate of a spot to investigate.
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: movement cost on success, None on failure.
    :rtype: float or None
    """
    path = monster.ai.chosen_path or state.area.path(monster, x, y)
    if path is None:
        return None
    monster.ai.chosen_path = path
    try:
        move_here = monster.ai.chosen_path.popleft()
    except IndexError:
        return 0
    cost = movement_speed(monster, state)
    if cost > monster.action_points:
        return None
    state.area.place_entity(monster, *move_here)
    return cost


#--------- monsters pursuing ---------#


@dispatch(m.Monster, c.Character, gs.GameState)
def pursue(monster, who, state):
    """
    Pursue someone.

    :param monster: who is pursuing.
    :type monster: sw.monster.Monster
    :param who: who is being pursued.
    :type who: sw.character.Character
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: movement cost on success, None on failure.
    :rtype: float or None
    """
    path = monster.ai.chosen_path or state.area.path(monster, *who.position)
    if path is None:
        return None
    monster.ai.chosen_path = path
    try:
        move_here = monster.ai.chosen_path[0]
    except IndexError:
        return 0
    cost = movement_speed(monster, state)
    if cost > monster.action_points:
        return None
    monster.ai.chosen_path.popleft()
    state.area.place_entity(monster, *move_here)
    return cost


#--------- monsters resting ---------#

@dispatch(m.Monster, gs.GameState)
def rest(monster, state):
    """
    Rest.

    :param monster: who is resting.
    :type monster: sw.monster.Monster
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: amount of spent AP.
    :rtype: float
    """
    state.ui.message("FIXME: generic monster rest", None)
    monster.action_points = 0
    return None


#--------- monsters retreating ---------#

@dispatch(m.Monster, gs.GameState)
def retreat(monster, state):
    """
    Retreat.

    :param monster: who is retreating.
    :type monster: sw.monster.Monster
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: amount of spent AP or None on failure.
    :rtype: float or None
    """
    state.ui.message("FIXME: generic monster retreat", None)
    return None


#--------- monsters stepping aside ---------#

@dispatch(m.Monster, gs.GameState)
def step_aside(monster, state):
    """
    Step aside to allow fellow monsters to pass.

    :param monster: who is stepping aside.
    :type monster: sw.monster.Monster
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: amount of spent AP or None on failure.
    :rtype: float or None
    """
    state.ui.message("FIXME: generic monster step aside", None)
    return None


#--------- movement speeds ---------#


@dispatch(m.Monster, gs.GameState)
def movement_speed(monster, state):
    """
    :param monster: a monster to calculate movement cost for.
    :type monster: sw.monster.Monster
    :param state: a global environment.
    :type state: sw.gamestate.GameState

    :return: AP cost of a single movement.
    :rtype: float
    """
    speed = monster.total_secondary[stat.SecondaryStat.MOVEMENT_SPEED]
    return misc.segment_interpolation(
        speed,
        (0, 30),
        (10, 10),
        (20, 7),
        (25, 5),
        (30, 1))


#--------- attack speeds - with weapons ---------#


@dispatch(m.Monster, i.Dagger, gs.GameState)
def attack_speed(monster, dagger, state):
    """
    Return AP cost of a dagger strike.

    :param monster: a monster to calculate AP cost for.
    :type monster: sw.monster.Monster
    :param weapon: a dagger the monster uses.
    :type weapon: sw.item.Dagger
    :param state: a global state.
    :type state: sw.gamestate.GameState

    :return: AP cost of a dagger attack.
    :rtype: float
    """
    speed = monster.total_secondary[stat.SecondaryStat.SPEED]
    skill = monster.total_skills[skill.Skill.DAGGER]
    speed = speed + skill * 1.25
    return misc.segment_interpolation(
        speed,
        (0, 20),
        (10, 10),
        (20, 5),
        (25, 3),
        (30, 1))


#--------- attack speeds - unarmed ---------#


@dispatch(m.Monster, gs.GameState)
def attack_speed(monster, state):
    """
    Return AP cost of an unarmed melee attack.

    :param monster: a monster to calculate AP cost for.
    :type monster: sw.monster.Monster
    :param state: a global environment.
    :type state: sw.gamestate.GameState
    
    :return: AP cost of an unarmed melee attack.
    :rtype: float
    """
    speed = monster.total_secondary[stat.SecondaryStat.SPEED]
    return misc.segment_interpolation(
        speed,
        (0, 20),
        (10, 10),
        (20, 5),
        (25, 3),
        (30, 1))
