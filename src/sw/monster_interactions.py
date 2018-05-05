"""
Monster interactions module.

Provides several functions for interacting with (or by) monsters.
"""


from multipledispatch import dispatch


import sw.const.ai as constai
from sw.const.message import Channel

import sw.ai as a
import sw.character as c
import sw.doodad as d
import sw.gamestate as gs
import sw.item as i
import sw.monster as m
import sw.player as p
import sw.spell as s


#--------- performing AI tasks - main function ---------#


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
    """
    if task is constai.Task.ATTACK:
        attack(monster, taskargs[0], state)
    elif task is constai.Task.CAST_SPELL:
        cast_spell(monster, taskargs[0], taskargs[1], state)
    elif task is constai.Task.EXPLORE:
        explore(monster, state)
    elif task is constai.Task.FOLLOW:
        follow(monster, taskargs[0], state)
    elif task is constai.Task.INVESTIGATE:
        investigate(monster, *taskargs[0], state)
    elif task is constai.Task.PURSUE:
        pursue(monster, taskargs[0], state)
    elif task is constai.Task.REST:
        rest(monster, state)
    elif task is constai.Task.RETREAT:
        retreat(monster, state)
    elif task is constai.Task.STEP_ASIDE:
        step_aside(monster, state)
    else:
        raise ValueError(f"Unknown task '{task}'")


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
    """
    state.ui.message("FIXME: generic attack", None)


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
    """
    state.ui.message("FIXME: generic spell cast", None)


#--------- monster exploration ---------#


@dispatch(m.Monster, gs.GameState)
def explore(monster, state):
    """
    Explore the area.

    :param monster: who is exploring.
    :type monster: sw.monster.Monster
    :param state: a global environment.
    :type state: sw.gamestate.GameState
    """
    state.ui.message("FIXME: generic monster explore", None)


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
    """
    state.ui.message("FIXME: generic monster follow", None)


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
    """
    state.ui.message("FIXME: generic monster investigate", None)


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
    """
    state.ui.message("FIXME: generic monster pursue", None)


#--------- monsters resting ---------#

@dispatch(m.Monster, gs.GameState)
def rest(monster, state):
    """
    Rest.

    :param monster: who is resting.
    :type monster: sw.monster.Monster
    :param state: a global environment.
    :type state: sw.gamestate.GameState
    """
    state.ui.message("FIXME: generic monster rest", None)


#--------- monsters retreating ---------#

@dispatch(m.Monster, gs.GameState)
def retreat(monster, state):
    """
    Retreat.

    :param monster: who is retreating.
    :type monster: sw.monster.Monster
    :param state: a global environment.
    :type state: sw.gamestate.GameState
    """
    state.ui.message("FIXME: generic monster retreat", None)


#--------- monsters stepping aside ---------#

@dispatch(m.Monster, gs.GameState)
def step_aside(monster, state):
    """
    Step aside to allow fellow monsters to pass.

    :param monster: who is stepping aside.
    :type monster: sw.monster.Monster
    :param state: a global environment.
    :type state: sw.gamestate.GameState
    """
    state.ui.message("FIXME: generic monster step aside", None)
