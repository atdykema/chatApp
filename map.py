from game import *
from server import server_settings
import uuid

class Tile:
    def __init__(self, tile_type, properties=None, players=None, items=None):
        self.tile_id = uuid.uuid4().hex
        self.tile_type = tile_type

        if properties is not None:
            self.properties = properties
        else:
            self.properties = tile_properties[tile_type]
                
        if players is not None:
            self.players = players
        else:
            self.players = dict()

        if items is not None:
            self.items = items
        else:
            self.items = dict()


class Properties:
    def __init__(self, is_occupied, tile_texture, script):
        self.tile_texture = tile_texture
        self.is_occupied = is_occupied
        self.script = script

tile_scripts = {
    'GRASS': None,
    'WATER': None,
    'TREE_1': None,
    'WALL_1': None,
}

tile_texture = {
    'GRASS': '_',
    'WATER': '🌊',
    'TREE_1': '🌳',
    'WALL_1': '🧱'
}

tile_properties = {
    'GRASS': Properties(False, tile_texture['GRASS'], tile_scripts['GRASS']),
    'WATER': Properties(True, tile_texture['WATER'], tile_scripts['WATER']),
    'TREE_1': Properties(True, tile_texture['TREE_1'], tile_scripts['TREE_1']),
    'WALL_1': Properties(True, tile_texture['WALL_1'], tile_scripts['WALL_1'])
}

world_map = [
    [Tile('WATER'), Tile('WATER'), Tile('WATER'), Tile('WATER'), Tile('WATER'), Tile('WATER'), Tile('WATER'), Tile('WATER'), Tile('WATER')],
    [Tile('WATER'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('WATER')],
    [Tile('WATER'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('WATER')],
    [Tile('WATER'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('WATER')],
    [Tile('WATER'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('WATER')],
    [Tile('WATER'), Tile('GRASS'), Tile('GRASS'), Tile('WALL_1'), Tile('TREE_1'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('WATER')],
    [Tile('WATER'), Tile('GRASS'), Tile('GRASS'), Tile('TREE_1'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('WATER')],
    [Tile('WATER'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('WATER')],
    [Tile('WATER'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('GRASS'), Tile('WATER')],
    [Tile('WATER'), Tile('WATER'), Tile('WATER'), Tile('WATER'), Tile('WATER'), Tile('WATER'), Tile('WATER'), Tile('WATER'), Tile('WATER')]
]

server_settings.MAP_DIMENSIONS = [len(world_map), len(world_map[0])]