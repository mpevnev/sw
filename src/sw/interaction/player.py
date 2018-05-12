"""
Player interactions module.
"""


import random as rand


from multipledispatch import dispatch


import sw.doodad as d
import sw.gamestate as gs
import sw.item as i
import sw.misc as misc
import sw.monster as m
import sw.player as p


import sw.const.item as ci
import sw.const.message as msg
import sw.const.player as cp
import sw.const.skill as skill
import sw.const.stat as stat


#--------- attacking ---------#


@dispatch(p.Player, i.Dagger, m.Monster, gs.GameState, bool)
def attack(player, dagger, monster, state, force):
    """
    Attack something with a given melee weapon in a given environment.

    :param player: who is attacking.
    :type player: sw.player.Player
    :param dagger: a weapon to use.
    :type dagger: sw.item.Dagger
    :param monster: a target monster.
    :type monster: sw.monster.Monster
    :param state: a global environment.
    :type state: sw.gamestate.GameState
    :param bool force: if set to True, attack even if it's dangerous.

    :return: True on success, an error code on failure.
    :rtype: bool or sw.const.player.AttackError
    """
    # TODO: a to-hit calculation, check if the target is friendly, stabbing, etc...
    weapon_skill = player.total_skill[skill.Skill.DAGGER]
    damage = rand.randint(weapon.min_damage, weapon.max_damage)
    damage_bonus = weapon_skill * 0.75 if weapon_skill < 10 else 2.5 + weapon_skill * 0.50
    damage += damage_bonus
    damage -= monster.total_secondary[stat.SecondaryStat.ARMOR]
    damage = max(damage, 0)
    monster.health -= damage
    state.ai_action_points += dagger.action_points_cost
    state.ui.message(f"TEMP DEBUG: stab {monster.recipe_id} for {damage} damage",
                     msg.Channel.PLAYER_ATTACK)

#--------- movement ---------#


def move(player, dx, dy, state, force):
    """
    Move to a specified position.

    :param player: who is moving.
    :type player: sw.player.Player
    :param int dx: change of the X coordinate of the player.
    :param int dy: change of the Y coordinate of the player.
    :param state: a global environment.
    :type state: sw.gamestate.GameState
    :param bool force: move even if it's dangerous.

    :return: True on success, an error code on failure.
    :rtype: bool or sw.const.player.MoveError
    """
    speed = player.total_secondary[stat.SecondaryStat.MOVEMENT_SPEED]
    cost = misc.segment_interpolation(
        speed,
        (0, 20),
        (10, 10),
        (20, 5),
        (25, 3),
        (30, 1))
    area = state.area
    if not area.shift_entity(player, dx, dy):
        return cp.MoveError.BLOCKED
    # TODO: danger check for player movement
    state.ai_action_points += cost
    area.update_visibility_matrix()
    return True
