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

    def __init__(self, data):
        """
        Initialize a world.

        :param data: game data used to populate the world with things.
        :type data: sw.gamedata.GameData
        """
        self.name = None
        self.data = data
        self.save_dir = None
        self.area_headers = {}

    #--------- area manipulation ---------#

    def add_area(self, x, y):
        """
        Generate a new area at the given coordinates.

        :param int x: X coordinate of the new area.
        :param int y: Y coordinate of the new area.
        """
        if (x, y) in self.area_headers:
            return
        area = ah.area_header_from_scratch(self.data, None, aconst.ArcanumLevel.ZERO)
        self.area_headers[(x, y)] = area
                                                                

    def generate_area_buffer(self, around_x, around_y):
        """
        Generate buffer areas around given coordinates, that is, add new areas
        in a rectangle centered around them.

        :param int around_x: X coordinate of the center of the buffer.
        :param int around_y: Y coordinate of the center of the buffer.
        """
        for x in range(around_x - MIN_AREA_BUFFER, around_x + MIN_AREA_BUFFER):
            for y in range(around_y - MIN_AREA_BUFFER, around_y + MIN_AREA_BUFFER):
                self.add_area(x, y)


#--------- world creation from saved YAML dicts ---------#


def world_from_save(gamedata, save):
    """
    Generate a world from a save.

    :param gamedata: game data used to repopulate the world with things.
    :type gamedata: sw.gamedata.GameData
    :param dict save: saved info about the world.
    """
    raise NotImplementedError


#--------- world creation from scratch ---------#


def world_from_scratch(gamedata):
    """
    Generate a world from scratch.

    :param gamedata: game data used to populate the world.
    :type gamedata: sw.gamedata.GameData
    """
    res = World(gamedata)
    res.name = "TEMP WORLD NAME"
    res.generate_area_buffer(0, 0)
    return res
