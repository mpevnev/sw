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

    @staticmethod
    def from_data(data):
        """ Create a character from a data dict. """
        raise NotImplementedError

    def from_scratch(name, species, background):
        """ Create a wholly new character. """
        res = Player()
        res.name = name
        res.species = species
        res.background = background
        res._apply_species()
        res._apply_background()
        return res

    #--------- species manipulation ---------#

    def _apply_species(self):
        """ Apply species' modifiers. """
        self.add_innate_modifiers(*self.species.modifiers)

    #--------- background manipulation ---------#

    def _apply_background(self):
        """ Apply background's modifiers. """
        self.add_temp_modifiers(*self.background.modifiers)
