"""
Area header module.

Provides AreaHeader class.
"""


from sw.const.area import ArcanumLevel, HostilityLevel


#--------- main thing ---------#


class AreaHeader():
    """
    A minimal information about an area required to process the area as an
    overworld entity.
    """

    def __init__(self, data):
        self.data = data
        self.name = None
        self.biome = None
        self.arcanum_level = ArcanumLevel.ZERO
        self.hostility = HostilityLevel.SAFE


#--------- header generation variants ---------#


class AreaHeaderFromData(AreaHeader):
    """ An area header obtained from data files. """

    def __init__(self, gamedata, datadict):
        raise NotImplementedError


class AreaHeaderFromScratch(AreaHeader):
    """ A randomly-generated area header. """

    def __init__(self, data, biome, arcanum_level):
        super().__init__(data)
        self.name = "TEMP AREA NAME"
        self.biome = biome
        self.arcanum_level = arcanum_level
