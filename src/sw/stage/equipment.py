"""
Equipment stage.
"""


import sw.flow as flow

import sw.event.equipment as event


ENTRY_POINT = "entry point"


class Equipment(flow.SWFlow):
    """ Equipment handler. """

    def __init__(self, state, ui_spawner):
        super().__init__(state, ui_spawner, ui_spawner.spawn_equipment(state.player.equipment))
        self.register_event_handler(self.quit)
        self.register_event_handler(self.view_item)

    #--------- event handlers ---------#

    def view_item(self, ev):
        """ Handle 'view item' event. """
        if ev[0] != event.EXAMINE_ITEM:
            return False
        import sw.stage.item_view as iv
        item = ev[1]
        new_flow = iv.ItemView(self.state, self.ui_spawner, item)
        raise flow.ChangeFlow(new_flow, iv.FROM_EQUIPMENT)

    def quit(self, ev):
        """ Handle 'quit' event. """
        if ev[0] != event.QUIT:
            return False
        raise flow.EndFlow(None)
