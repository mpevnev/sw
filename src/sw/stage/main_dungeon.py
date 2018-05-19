"""
Main dungeon stage (well, and non-dungeon area exploration too).
"""


import sw.ai as ai
import sw.flow as flow

import sw.const.item as ci
import sw.const.player as cp

import sw.event.main_dungeon as event

import sw.interaction.item as ii
import sw.interaction.player as pi


FROM_INVENTORY = "from inventory"
FROM_OVERWORLD = "from overworld"


class MainDungeon(flow.SWFlow):
    """ Main dungeon handler. """

    def __init__(self, state, ui_spawner):
        super().__init__(state, ui_spawner, ui_spawner.spawn_main_dungeon(state))
        self.register_entry_point(FROM_INVENTORY, self.from_inventory)
        self.register_entry_point(FROM_OVERWORLD, self.from_overworld)
        self.register_event_handler(self.ascend)
        self.register_event_handler(self.descend)
        self.register_event_handler(self.inventory)
        self.register_event_handler(self.move)
        self.register_event_handler(self.pick_up_handler)
        self.register_event_handler(self.wait)

    #--------- entry points ---------#

    def from_inventory(self):
        """
        Do nothing special.
        """
        pass

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
        for i in range(80):
            dagger = item.item_from_recipe(item_recipe, self.state.data)
            ii.pick_up_item(dagger, self.state.player, self.state, False)
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

    def inventory(self, ev):
        """ Handle 'inventory' event. """
        if ev[0] != event.INVENTORY:
            return False
        import sw.stage.inventory as inv
        inventory = self.state.player.inventory
        inventory_flow = inv.Inventory(self.state,
                                       self.ui_spawner,
                                       self.ui_spawner.spawn_inventory(inventory))
        inventory_event = flow.execute(inventory_flow, inv.ENTRY_POINT)
        if inventory_event is None:
            return True
        self.process_event(inventory_event)
        return True

    def move(self, ev):
        """ Handle 'move' event. """
        if ev[0] != event.MOVE:
            return False
        delta = ev[1]
        player = self.state.player
        maybe_move = pi.move(player, *delta, self.state, False)
        if not maybe_move:
            if maybe_move is cp.MoveError.BLOCKED:
                self.attack(player.position[0] + delta[0], player.position[1] + delta[1])
        self.tick()
        return True

    def pick_up_handler(self, ev):
        """ Handle 'pick up' event. """
        if ev[0] != event.PICK_UP:
            return False
        area = self.state.area
        player = self.state.player
        items = list(area.items_at(*player.position, True))
        if not items:
            self.ui.message("TEMP DEBUG: nothing to pick up here", None)
        elif len(items) == 1:
            self.ui.message("TEMP DEBUG: picking up one item", None)
            self.pick_up(items)
        else:
            self.ui.message("TEMP DEBUG: picking up several items", None)
        return True

    def wait(self, ev):
        """ Handle 'wait' event. """
        if ev[0] != event.WAIT:
            return False
        self.state.ai_action_points += cp.AP_PER_WAIT
        self.tick()
        return True

    #--------- helper things ---------#

    def attack(self, x, y):
        """
        Make player attack things at a given position.

        :param int x: the X coordinate of a point to attack.
        :param int y: the Y coordinate of a point to attack.
        """
        area = self.state.area
        player = self.state.player
        blockers = area.blockers_at(player, x, y)
        weapon = player.melee_weapons()[0]
        for blocker in blockers:
            if weapon is None:
                # TODO: unarmed combat
                pass
            else:
                pi.attack(player, weapon, blocker, self.state, False)

    def pick_up(self, items):
        """
        Make player pick up some items.

        :param items: items to pick up.
        """
        player = self.state.player
        for item in items:
            res = ii.pick_up_item(item, player, self.state, False)
            if res is ci.PickUpError.NO_SLOTS:
                self.ui.message("TEMP DEBUG: no slots", None)
            else:
                self.ui.message("TEMP DEBUG: pick up an item", None)

    def tick(self):
        """ Process a single game turn. """
        self.state.turn += 1
        self.state.area.tick(self.state)
        self.state.player.tick(self.state)
        ai.ai_turn(self.state)
