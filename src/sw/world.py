"""
World module.

Provides World class used to store information about game world and dynamically
load it from and save it to disk.
"""


from enum import Enum


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
        self.area_headers[(x, y)] = AreaHeaderFromScratch(None, ArcanumLevel.ZERO)

    def generate_area_buffer(self, around_x, around_y):
        """
        Generate buffer areas around given coordinates, that is, add new areas
        in a rectangle centered around them.
        """
        for x in range(around_x - MIN_AREA_BUFFER, around_x + MIN_AREA_BUFFER):
            for y in range(around_y - MIN_AREA_BUFFER, around_y + MIN_AREA_BUFFER):
                self.add_area(x, y)


class AreaHeader():
    """
    A minimal information about an area required to process the area as an
    overworld entity.
    """

    def __init__(self):
        self.name = None
        self.biome = None
        self.arcanum_level = ArcanumLevel.ZERO
        self.hostility = HostilityLevel.SAFE


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


class AreaHeaderFromData(AreaHeader):
    """ An area header obtained from data files. """

    def __init__(self):
        raise NotImplementedError


class AreaHeaderFromScratch(AreaHeader):
    """ A randomly-generated area header. """

    def __init__(self, biome, arcanum_level):
        super().__init__()
        self.name = "TEMP AREA NAME"
        self.biome = biome
        self.arcanum_level = arcanum_level


#--------- helpful enums ---------#


class ArcanumLevel(Enum):
    """ An enumeration of levels of area's arcanum corruption. """

    ZERO = 0
    MILD = 1
    MODERATE = 2
    SEVERE = 3
    COMPLETE = 4


class HostilityLevel(Enum):
    """ An enumeration of area's hostility level. """

    SAFE = 0
    WILD = 1
    DANGEROUS = 2
    WAR_ZONE = 3
    DEEP_ARCANUM = 4
