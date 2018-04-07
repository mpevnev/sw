"""
World module.

Provides World class used to store information about game world and dynamically
load it from and save it to disk.
"""


from enum import Enum


#--------- main classes ---------#

class World():
    """
    Representation of a game world. It is responsible for unifying AreaHeader's
    and for saving and loading them as needed, also for creating new ones.
    """

    def __init__(self):
        self.name = None
        self.save_dir = None
        self.area_headers = None


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
        # TODO: name generation
        super().__init__()


class AreaHeaderFromData(AreaHeader):
    """ An area header obtained from data files. """

    def __init__(self):
        raise NotImplementedError


class AreaHeaderFromScratch(AreaHeader):
    """ A randomly-generated area header. """

    def __init__(self, biome, arcanum_level):
        super().__init__()
        # TODO: name generation
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
    """ An enumeration of hostility levels of areas. """

    SAFE = 0
    WILD = 1
    DANGEROUS = 2
    WAR_ZONE = 3
