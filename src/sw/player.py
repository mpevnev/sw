"""
Player module.

Provides Player class used to represent the player character.
"""


from sw.character import Character


class Player(Character):
    """ Player character. """

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.species = None
        self.background = Noneo

    #--------- species manipulation ---------#

    def set_species(self, species):
        """ Change character's species. """
        self._undo_species()
        self.species = species
        self._apply_species()

    def _apply_species(self):
        """ Apply species' modifiers. """
        pass

    def _undo_species(self):
        """ Undo species' modifiers. """
        pass

    #--------- background manipulation ---------#

    def set_background(self, bg):
        """ Change character's background. """
        self._undo_background()
        self.background = bg
        self._apply_background()

    def _apply_background(self):
        """ Apply background's modifiers. """
        pass

    def _undo_background(self):
        """ Undo background's modifiers. """
        pass
