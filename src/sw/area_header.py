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
        """
        Create an area header.

        :param data: a game data object needed for a later area generation.
        :type data: sw.gamedata.GameData
        """
        self.data = data
        self.name = None
        self.biome = None
        self.arcanum_level = ArcanumLevel.ZERO
        self.hostility = HostilityLevel.SAFE

    def load_or_generate_area(self):
        """
        Either load an area from a file, or generate it from scratch.
        
        :return: the loaded or generated area.
        :rtype: sw.area.Area
        """
        # TODO: reading areas from a file
        import sw.area as area
        return area.area_from_scratch(self.data, self.biome, 20, 20)


#--------- header generation from saved YAML dicts ---------#


def area_header_from_save(gamedata, yaml_dict):
    """
    Generate an area header from a YAML dict.

    :param gamedata: a game data object.
    :type gamedata: sw.gamedata.GameData
    :param dict yaml_dict: a YAML dict with the saved header info.

    :return: the generated header.
    :rtype: AreaHeader
    """
    raise NotImplementedError


#--------- header generation from scratch ---------#


def area_header_from_scratch(gamedata, biome, arcanum_level):
    """
    Generate an area header with given parameters.

    :param gamedata: a game data object.
    :type gamedata: sw.gamedata.GameData
    :param biome: the biome that should be used for the generated header.
    :param ArcanumLevel arcanum_level: the level of arcanum corruption for the
    generated header.

    :return: the generated header.
    :rtype: AreaHeader
    """
    res = AreaHeader(gamedata)
    res.name = "TEMP AREA NAME"
    res.biome = biome
    res.arcanum_level = arcanum_level
    return res
