"""
World module.

Provides World class used to store information about game world and dynamically
load it from and save it to disk.
"""


import sw.area_header as ah
import sw.const.area as aconst


MIN_AREA_BUFFER = 7


#--------- main classes ---------#

class World():
    """
    Representation of a game world. It is responsible for unifying and creating
    AreaHeader's.
    """

    def __init__(self):
        self.name = None
        self.save_dir = None
        self.area_headers = {}

    #--------- area manipulation ---------#

    def add_area(self, x, y):
        """ Generate a new area at the given coordinates. """
        if (x, y) in self.area_headers:
            return
        self.area_headers[(x, y)] = ah.AreaHeaderFromScratch(None, aconst.ArcanumLevel.ZERO)

    def generate_area_buffer(self, around_x, around_y):
        """
        Generate buffer areas around given coordinates, that is, add new areas
        in a rectangle centered around them.
        """
        for x in range(around_x - MIN_AREA_BUFFER, around_x + MIN_AREA_BUFFER):
            for y in range(around_y - MIN_AREA_BUFFER, around_y + MIN_AREA_BUFFER):
                self.add_area(x, y)


#--------- subclasses for reading and creating the above ---------#


class WorldFromData(World):
    """ Representation of a game world obtained from a save file. """

    def __init__(self, data):
        raise NotImplementedError


class WorldFromScratch(World):
    """ A randomly generated representation of a game world. """

    def __init__(self):
        super().__init__()
        self.name = "TEMP WORLD NAME"
        self.generate_area_buffer(0, 0)
