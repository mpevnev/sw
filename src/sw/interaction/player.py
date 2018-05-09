"""
Player interactions module.
"""


import random as rand


from multipledispatch import dispatch


import sw.doodad as d
import sw.gamestate as gs
import sw.item as i
import sw.monster as m
import sw.player as p


import sw.const.item as ci
import sw.const.message as msg
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
