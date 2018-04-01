"""
Character creation module.
"""


import mofloc


import sw.event.background_selection as bs_event
import sw.event.char_name_prompt as cnp_event
import sw.event.species_selection as ss_event


NAME_INPUT_ENTRY_POINT = "the only"
BG_SEL_ENTRY_POINT = "the only"
SPECIES_SEL_ENTRY_POINT = "the only"


class NameInput(mofloc.Flow):
    """ Name input control flow. """

    def __init__(self, data, spawner):
        super().__init__()
        self.data = data
        self.ui_spawner = spawner
        self.ui = spawner.spawn_char_name_prompt(data)
        self.register_entry_point(NAME_INPUT_ENTRY_POINT, self.run_prompt)
        self.register_event_source(self.ui)
        self.register_preevent_action(self.draw)
        self.register_event_handler(self.enter_name)

    def run_prompt(self):
        """ A stub, main processing is done in event handlers. """
        pass

    def draw(self):
        """ Draw the prompt. """
        self.ui.draw()

    #--------- event handlers ---------#

    def enter_name(self, ev):
        """ Process a 'name entered' event. """
        if ev[0] != cnp_event.NAME_ENTERED:
            return False
        new_flow = SpeciesSelection(self.data, self.ui_spawner, ev[1])
        raise mofloc.ChangeFlow(new_flow, BG_SEL_ENTRY_POINT)


class SpeciesSelection(mofloc.Flow):
    """ Species selection control flow. """

    def __init__(self, data, spawner, name):
        super().__init__()
        self.data = data
        self.ui_spawner = spawner
        self.ui = spawner.spawn_species_selection(data)
        self.name = name
        self.register_entry_point(SPECIES_SEL_ENTRY_POINT, self.run_menu)
        self.register_event_source(self.ui)
        self.register_preevent_action(self.draw)
        self.register_event_handler(self.abort)
        self.register_event_handler(self.choose_species)

    def run_menu(self):
        """ A stub. """
        pass

    def draw(self):
        """ Draw the menu. """
        self.ui.draw()

    #--------- event handlers ---------#

    def abort(self, ev):
        """ Process an 'abort char creation' event. """
        if ev[0] != ss_event.ABORT_SPECIES:
            return False
        import sw.stage.main_menu as mm
        new_flow = mm.MainMenu(self.data, self.ui_spawner)
        raise mofloc.ChangeFlow(new_flow, mm.ENTRY_POINT)

    def choose_species(self, ev):
        """ Process a 'choose species' event. """
        if ev[0] != ss_event.CHOOSE_SPECIES:
            return False
        new_flow = BackgroundSelection(self.data, self.ui_spawner, self.name, ev[1])
        raise mofloc.ChangeFlow(new_flow, BG_SEL_ENTRY_POINT)


class BackgroundSelection(mofloc.Flow):
    """ Background selection control flow. """

    def __init__(self, data, spawner, name, species):
        super().__init__()
        self.data = data
        self.ui_spawner = spawner
        self.ui = spawner.spawn_background_selection(data, species)
        self.name = name
        self.species = species
        self.register_entry_point(BG_SEL_ENTRY_POINT, self.run_menu)
        self.register_event_source(self.ui)
        self.register_preevent_action(self.draw)
        self.register_event_handler(self.abort)
        self.register_event_handler(self.back)
        self.register_event_handler(self.choose_background)

    def run_menu(self):
        """ A stub, main processing is done in event handlers. """
        pass

    def draw(self):
        """ Draw the menu. """
        self.ui.draw()


    #--------- event handlers ---------#

    def abort(self, ev):
        """ Process an 'abort char creation' event. """
        if ev[0] != bs_event.ABORT_BACKGROUND:
            return False
        import sw.stage.main_menu as mm
        new_flow = mm.MainMenu(self.data, self.ui_spawner)
        raise mofloc.ChangeFlow(new_flow, mm.ENTRY_POINT)

    def back(self, ev):
        """ Process 'return to species selection' event. """
        if ev[0] != bs_event.BACK_TO_SPECIES:
            return False
        new_flow = SpeciesSelection(self.data, self.ui_spawner, self.name)
        raise mofloc.ChangeFlow(new_flow, SPECIES_SEL_ENTRY_POINT)

    def choose_background(self, ev):
        """ Process a 'background chosen' event. """
        if ev[0] != bs_event.CHOOSE_BACKGROUND:
            return False
        return True
