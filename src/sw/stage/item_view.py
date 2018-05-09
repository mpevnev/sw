"""
Item view stage.
"""


import sw.flow as flow


import sw.event.item_view as event
import sw.event.item_events as output_event


ENTRY_POINT = "entry point"


class ItemView(flow.SWFlow):
    """
    Single item interaction selector.
    
    Note that this should *not* handle the interactions, only select them and
    return them to other flows, which will handle them as required.
    """

    def __init__(self, state, ui_spawner, ui):
        super().__init__(state, ui_spawner, ui)
        self.register_entry_point(ENTRY_POINT, self.entry_point)
        self.register_event_handler(self.quit_altogether)
        self.register_event_handler(self.quit_to_inventory)

    #--------- entry points ---------#

    def entry_point(self):
        """ A stub, all processing is in the events section. """
        pass

    #--------- event handlers ---------#

    def quit_altogether(self, ev):
        """
        Quit both this viewer and possible inventory/equipment flow as well
        with no action.
        """
        if ev[0] != event.QUIT_ALTOGETHER:
            return False
        raise flow.EndFlow(None)

    def quit_to_inventory(self, ev):
        """
        Quit the item view back to inventory.
        """
        if ev[0] != event.QUIT_TO_INVENTORY:
            return False
        import sw.stage.inventory as inv
        new_flow = inv.Inventory(self.state,
                                 self.ui_spawner,
                                 self.ui_spawner.spawn_inventory(self.state))
        raise flow.ChangeFlow(new_flow, inv.ENTRY_POINT)
