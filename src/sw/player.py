"""
Player module.

Provides Player class used to represent the player character.
"""


from sw.character import Character


class Player(Character):
    """ Player character. """

    def __init__(self):
        super().__init__()
        self.name = None
        self.species = None
        self.background = None


class PlayerFromData(Player):
    """ A player created from a data dict. """

    def __init__(self):
        super().__init__()


class PlayerFromScratch(Player):
    """ A player created from the data received from the user. """

    def __init__(self, name, species, background):
        super().__init__()
        self.name = name
        self.species = species
        self.background = background
        self._apply_species()
        self._apply_background()

    def _apply_species(self):
        """ Apply species' modifiers. """
        self.add_innate_modifiers(*self.species.modifiers)

    def _apply_background(self):
        """ Apply background's modifiers. """
        self.add_temp_modifiers(*self.background.modifiers)
