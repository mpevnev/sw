"""
Area header module.

Provides AreaHeader class.
"""


from sw.const.area import ArcanumLevel, HostilityLevel

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
