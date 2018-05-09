"""
Inventory stage.
"""


import sw.flow as flow

import sw.event.inventory as event
import sw.event.item_events as output_event


ENTRY_POINT = "entry point"


class Inventory(flow.SWFlow):
    """ Inventory handler. """

    def __init__(self, state, ui_spawner, ui):
        super().__init__(state, ui_spawner, ui)
        self.register_entry_point(ENTRY_POINT, self.entry_point)
        self.register_event_handler(self.quit)

    #--------- entry points ---------#

    def entry_point(self):
        """ Enter the flow from a dungeon view. """
        pass

    #--------- event handlers ---------#

    def view_item(self, ev):
        """ Handle 'view item' event. """
        if ev[0] != event.VIEW_ITEM:
            return False
        import sw.stage.item_view as iv
        item = ev[1]
        new_flow = iv.ItemView(self.state,
                               self.ui_spawner,
                               self.ui_spawner.spawn_item_viewer(),
                               item)
        raise flow.ChangeFlow(new_flow, iv.ENTRY_POINT)

    def quit(self, ev):
        """ Handle 'quit' event. """
        if ev[0] != event.QUIT:
            return False
        raise flow.EndFlow(None)
