"""
Character creation module.
"""


import sw.flow as flow
import sw.event.background_selection as bs_event
import sw.event.char_name_prompt as cnp_event
import sw.event.species_selection as ss_event
from sw.player import player_from_scratch


NAME_INPUT_ENTRY_POINT = "the only"
SPECIES_SEL_ENTRY_POINT = "the only"
BG_SEL_ENTRY_POINT = "the only"
FINAL_ENTRY_POINT = "the only"


class NameInput(flow.SWFlow):
    """ Name input control flow. """

    def __init__(self, state, spawner):
        super().__init__(state, spawner, spawner.spawn_char_name_prompt())
        self.register_entry_point(NAME_INPUT_ENTRY_POINT, self.run_prompt)
        self.register_event_handler(self.enter_name)

    def run_prompt(self):
        """ A stub, main processing is done in event handlers. """
        pass

    #--------- event handlers ---------#

    def enter_name(self, ev):
        """ Process a 'name entered' event. """
        if ev[0] != cnp_event.NAME_ENTERED:
            return False
        new_flow = SpeciesSelection(self.state, self.ui_spawner, ev[1])
        raise flow.ChangeFlow(new_flow, BG_SEL_ENTRY_POINT)


class SpeciesSelection(flow.SWFlow):
    """ Species selection control flow. """

    def __init__(self, state, spawner, name):
        super().__init__(state, spawner, spawner.spawn_species_selection(state.data))
        self.name = name
        self.register_entry_point(SPECIES_SEL_ENTRY_POINT, self.run_menu)
        self.register_event_handler(self.abort)
        self.register_event_handler(self.choose_species)

    def run_menu(self):
        """ A stub. """
        pass

    #--------- event handlers ---------#

    def abort(self, ev):
        """ Process an 'abort char creation' event. """
        if ev[0] != ss_event.ABORT_SPECIES:
            return False
        import sw.stage.main_menu as mm
        new_flow = mm.MainMenu(self.state, self.ui_spawner)
        raise flow.ChangeFlow(new_flow, mm.ENTRY_POINT)

    def choose_species(self, ev):
        """ Process a 'choose species' event. """
        if ev[0] != ss_event.CHOOSE_SPECIES:
            return False
        new_flow = BackgroundSelection(self.state, self.ui_spawner, self.name, ev[1])
        raise flow.ChangeFlow(new_flow, BG_SEL_ENTRY_POINT)


class BackgroundSelection(flow.SWFlow):
    """ Background selection control flow. """

    def __init__(self, state, spawner, name, species):
        super().__init__(state, spawner, spawner.spawn_background_selection(state.data, species))
        self.name = name
        self.species = species
        self.register_entry_point(BG_SEL_ENTRY_POINT, self.run_menu)
        self.register_event_handler(self.abort)
        self.register_event_handler(self.back)
        self.register_event_handler(self.choose_background)

    def run_menu(self):
        """ A stub, main processing is done in event handlers. """
        pass

    #--------- event handlers ---------#

    def abort(self, ev):
        """ Process an 'abort char creation' event. """
        if ev[0] != bs_event.ABORT_BACKGROUND:
            return False
        import sw.stage.main_menu as mm
        new_flow = mm.MainMenu(self.state, self.ui_spawner)
        raise flow.ChangeFlow(new_flow, mm.ENTRY_POINT)

    def back(self, ev):
        """ Process 'return to species selection' event. """
        if ev[0] != bs_event.BACK_TO_SPECIES:
            return False
        new_flow = SpeciesSelection(self.state, self.ui_spawner, self.name)
        raise flow.ChangeFlow(new_flow, SPECIES_SEL_ENTRY_POINT)

    def choose_background(self, ev):
        """ Process a 'background chosen' event. """
        if ev[0] != bs_event.CHOOSE_BACKGROUND:
            return False
        new_flow = PlayerCreator(self.state, self.ui_spawner, self.name, self.species, ev[1])
        raise flow.ChangeFlow(new_flow, FINAL_ENTRY_POINT)


class PlayerCreator(flow.SWFlow):
    """ The final flow that will create the player character. """

    def __init__(self, state, spawner, name, species, background):
        super().__init__(state, spawner, None)
        self.name = name
        self.species = species
        self.background = background
        self.register_entry_point(FINAL_ENTRY_POINT, self.create_player)

    def create_player(self):
        """
        Create the player character and transfer control to the world creator.
        """
        import sw.stage.world_generation as worldgen
        player = player_from_scratch(self.name, self.species, self.background)
        self.state.player = player
        new_flow = worldgen.WorldGeneration(self.state, self.ui_spawner)
        raise flow.ChangeFlow(new_flow, worldgen.ENTRY_POINT)
