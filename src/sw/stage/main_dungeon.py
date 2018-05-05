"""
Main dungeon stage (well, and non-dungeon area exploration too).
"""


import sw.ai as ai
import sw.flow as flow
import sw.event.main_dungeon as event


FROM_OVERWORLD = "from overworld"


class MainDungeon(flow.SWFlow):
    """ Main dungeon handler. """

    def __init__(self, state, ui_spawner):
        super().__init__(state, ui_spawner, ui_spawner.spawn_main_dungeon(state))
        self.register_entry_point(FROM_OVERWORLD, self.from_overworld)
        self.register_event_handler(self.ascend)
        self.register_event_handler(self.descend)
        self.register_event_handler(self.move)

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
        import sw.monster as monster
        self.state.area.randomly_place_player(self.state.player)
        self.state.area.update_visibility_matrix()
        recipe = self.state.data.monster_recipe_by_id("debug melee zombie")
        mon = monster.monster_from_recipe(recipe, self.state.data)
        mon.tick(self.state)
        mon.health = 1
        self.mon = mon
        self.state.area.add_entity(mon, 3, 3)

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
        if self.state.area.shift_entity(self.state.player, *delta):
            self.state.area.update_visibility_matrix()
            self.tick()
        return True

    #--------- helper things ---------#

    def tick(self):
        """ Process a single game turn. """
        self.state.turn += 1
        self.state.area.tick(self.state)
        self.state.player.tick(self.state)
        ai.ai_turn(self.state, 0)
