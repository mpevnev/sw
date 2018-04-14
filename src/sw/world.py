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
        self.name = None
        self.data = data
        self.save_dir = None
        self.area_headers = {}

    #--------- area manipulation ---------#

    def add_area(self, x, y):
        """ Generate a new area at the given coordinates. """
        if (x, y) in self.area_headers:
            return
        area = ah.area_header_from_scratch(self.data, None, aconst.ArcanumLevel.ZERO)
        self.area_headers[(x, y)] = area
                                                                

    def generate_area_buffer(self, around_x, around_y):
        """
        Generate buffer areas around given coordinates, that is, add new areas
        in a rectangle centered around them.
        """
        for x in range(around_x - MIN_AREA_BUFFER, around_x + MIN_AREA_BUFFER):
            for y in range(around_y - MIN_AREA_BUFFER, around_y + MIN_AREA_BUFFER):
                self.add_area(x, y)


#--------- world creation from YAML dicts ---------#


def world_from_data(gamedata, yaml_dict):
    """ Generate a world from a YAML dict. """
    raise NotImplementedError


#--------- world creation from scratch ---------#


def world_from_scratch(gamedata):
    """ Generate a world from scratch. """
    res = World(gamedata)
    res.name = "TEMP WORLD NAME"
    res.generate_area_buffer(0, 0)
    return res
