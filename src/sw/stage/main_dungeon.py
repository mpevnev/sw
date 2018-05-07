"""
Main dungeon stage (well, and non-dungeon area exploration too).
"""


import sw.ai as ai
import sw.flow as flow

import sw.event.main_dungeon as event

import sw.interaction.player as pi


FROM_OVERWORLD = "from overworld"


class MainDungeon(flow.SWFlow):
    """ Main dungeon handler. """

    def __init__(self, state, ui_spawner):
        super().__init__(state, ui_spawner, ui_spawner.spawn_main_dungeon(state))
        self.register_entry_point(FROM_OVERWORLD, self.from_overworld)
        self.register_event_handler(self.ascend)
        self.register_event_handler(self.descend)
        self.register_event_handler(self.move)
        self.register_event_handler(self.wait)

    #--------- entry points ---------#

    def from_overworld(self, area):
        """
        Figure out the starting position of the player and then proceed as
        usual.
        """
        self.state.ui = self.ui
        self.state.area = area
        self.state.area.tick(self.state)
        self.state.player.tick(self.state)
        # TEMP DEBUG
        import sw.item as item
        import sw.monster as monster
        self.state.area.randomly_place_player(self.state.player)
        self.state.area.update_visibility_matrix()
        recipe = self.state.data.monster_recipe_by_id("debug melee zombie")
        mon = monster.monster_from_recipe(recipe, self.state.data)
        mon.tick(self.state)
        mon.health = 1
        item_recipe = self.state.data.item_recipe_by_id("debug dagger")
        dagger = item.item_from_recipe(item_recipe, self.state.data)
        self.mon = mon
        self.state.area.add_entity(mon, 3, 3)
        self.state.area.add_entity(dagger, 3, 6)

    #--------- event handlers ---------#

    def ascend(self, ev):
        """ Handle 'ascend' event. """
        if ev[0] != event.ASCEND:
            return False
        return True

    def descend(self, ev):
        """ Handle 'descend' event. """
        if ev[0] != event.DESCEND:
            return False
        return True

    def move(self, ev):
        """ Handle 'move' event. """
        if ev[0] != event.MOVE:
            return False
        delta = ev[1]
        area = self.state.area
        player = self.state.player
        if area.shift_entity(player, *delta):
            area.update_visibility_matrix()
            self.tick()
        else:
            self.attack(player.position[0] + delta[0], player.position[1] + delta[1])
        return True

    def wait(self, ev):
        """ Handle 'wait' event. """
        if ev[0] != event.WAIT:
            return False
        self.tick()
        return True

    #--------- helper things ---------#

    def attack(self, x, y):
        """
        Make player attack things at a given position.

        :param int x: the X coordinate of a point to attack.
        :param int y: the Y coordinate of a point to attack.
        """
        player = self.state.player
        blockers = area.blockers_at(player, *target)
        for blocker in blockers:
            for weapon in player.melee_weapons():
                pi.attack(player, weapon, blocker, self.state, False)


    def tick(self):
        """ Process a single game turn. """
        self.state.turn += 1
        self.state.area.tick(self.state)
        self.state.player.tick(self.state)
        ai.ai_turn(self.state)
