"""
World module.

Provides World class used to store information about game world and dynamically
load it from and save it to disk.
"""


from enum import Enum


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
        self.area_headers[(x, y)] = AreaHeaderFromScratch(None, ArcanumLevel.ZERO)


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
        for x in range(10):
            for y in range(10):
                self.area_headers[(x, y)] = AreaHeaderFromScratch(None, ArcanumLevel.ZERO)


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
