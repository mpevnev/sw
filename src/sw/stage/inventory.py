"""
Inventory stage.
"""


import sw.flow as flow

import sw.event.inventory as event


ENTRY_POINT = "from dungeon"


class Inventory(flow.SWFlow):
    """ Inventory handler. """

    def __init__(self, state, ui_spawner, ui, next_flow, next_flow_entry_point):
        super().__init__(state, ui_spawner, ui)
        self.register_entry_point(ENTRY_POINT, self.entry_point)
        self.register_event_handler(self.quit)
        self.next_flow = next_flow
        self.next_flow_entry_point = next_flow_entry_point

    #--------- entry points ---------#

    def entry_point(self):
        """ Enter the flow from a dungeon view. """
        pass

    #--------- event handlers ---------#

    def quit(self, ev):
        """ Handle 'quit' event. """
        if ev[0] != event.QUIT:
            return False
        raise flow.ChangeFlow(self.next_flow, self.next_flow_entry_point)
