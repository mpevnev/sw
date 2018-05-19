"""
Item view stage.
"""


import sw.flow as flow


import sw.event.item_view as event
import sw.event.item_events as output_event


FROM_INVENTORY = "from inventory"
FROM_EQUIPMENT = "from equipment"


class ItemView(flow.SWFlow):
    """
    Single item interaction selector.
    
    Note that this should *not* handle the interactions, only select them and
    return them to other flows, which will handle them as required.
    """

    def __init__(self, state, ui_spawner, item):
        super().__init__(state, ui_spawner, ui_spawner.spawn_item_view(state, item))
        self.register_entry_point(FROM_EQUIPMENT, self.from_equipment)
        self.register_entry_point(FROM_INVENTORY, self.from_inventory)
        self.register_event_handler(self.drink)
        self.register_event_handler(self.drop)
        self.register_event_handler(self.equip)
        self.register_event_handler(self.read)
        self.register_event_handler(self.take_off)
        self.register_event_handler(self.use)
        self.register_event_handler(self.quit_altogether)
        self.item = item

    #--------- entry points ---------#

    def from_inventory(self):
        """ Entered from inventory, will return to it on exit. """
        self.register_event_handler(self.quit_to_inventory)

    def from_equipment(self):
        """ Entered from the equipment menu, will return there on exit. """
        self.register_event_handler(self.quit_to_equipment)

    #--------- event handlers ---------#

    def drink(self, ev):
        """ Handle 'drink' event. """
        if ev[0] != event.DRINK:
            return False
        raise flow.EndFlow((output_event.DRINK, self.item))

    def drop(self, ev):
        """ Handle 'drop' event. """
        if ev[0] != event.DROP:
            return False
        raise flow.EndFlow((output_event.DROP, self.item))

    def equip(self, ev):
        """ Handle 'equip' event. """
        if ev[0] != event.EQUIP:
            return False
        raise flow.EndFlow((output_event.EQUIP, self.item))

    def read(self, ev):
        """ Handle 'read' event. """
        if ev[0] != event.READ:
            return False
        raise flow.EndFlow((output_event.READ, self.item))

    def take_off(self, ev):
        """ Handle 'take_off' event. """
        if ev[0] != event.TAKE_OFF:
            return False
        raise flow.EndFlow((output_event.TAKE_OFF, self.item))

    def use(self, ev):
        """ Handle 'use' event. """
        if ev[0] != event.USE:
            return False
        raise flow.EndFlow((output_event.USE, self.item))

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
        inventory = self.state.player.inventory
        new_flow = inv.Inventory(self.state, self.ui_spawner, inventory)
        raise flow.ChangeFlow(new_flow, inv.ENTRY_POINT)
