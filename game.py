import pickle
import uuid
from variables import *

class Player:
    def __init__(self, alias):
        self.player_id = uuid.uuid4().hex
        self.alias = alias
        self.location = PLAYER_SPAWN
        self.skills = Skills()
        self.inventory = Inventory()
        self.equipment = Equipment()
        self.indicator = '*'

class Skills:
    def __init__(self):
        self.woodcutting = 1
        self.magic = 1

class Inventory:
    def __init__(self):
        self.backpack = [None, None, None, None, None, None, None, None, None, None]

class Equipment:
    def __init__(self):
        self.equipment = [None, None, None, None, None, None, None, None, None, None]

class MapTile:
    def __init__(self, tile_purpose, is_occupied, properties):
        self.tile_id = uuid.uuid4().hex
        self.tile_purpose = tile_purpose
        self.is_occupied = is_occupied
        self.properties = MapTileProperties(properties)
        self.players = []
        self.items = []

class MapTileProperties:
    def __init__(self, properties):
        self.script = properties.script

class Item:
    def __init__(self, item):
        self.item_id = uuid.uuid4().hex
        self.item = item

class DroppedItem:
    def __init__(self, item, location):
        self.dropped_item_id = uuid.uuid4().hex
        self.item = item
        self.location = location

def move_down(entity):
        if entity.location[0] < MAP_DIMENSIONS[0]:
            current_board_state[player_1_loc[0]][player_1_loc[1]] = '-'
            player_1_loc[0] += 1
            current_board_state[player_1_loc[0]][player_1_loc[1]] = '*'

def move_up(player_number, entity):
    if player_number == 1:
        if player_1_loc[0] > 0:
            current_board_state[player_1_loc[0]][player_1_loc[1]] = '-'
            player_1_loc[0] -= 1
            current_board_state[player_1_loc[0]][player_1_loc[1]] = '*'
    elif player_number == 2:
        if player_2_loc[0] > 0:
            current_board_state[player_2_loc[0]][player_2_loc[1]] = '-'
            player_2_loc[0] -= 1
            current_board_state[player_2_loc[0]][player_2_loc[1]] = '*'

def move_left(player_number, entity):
    if player_number == 1:
        if player_1_loc[1] > 0:
            current_board_state[player_1_loc[0]][player_1_loc[1]] = '-'
            player_1_loc[1] -= 1
            current_board_state[player_1_loc[0]][player_1_loc[1]] = '*'
    elif player_number == 2:
        if player_2_loc[1] > 0:
            current_board_state[player_2_loc[0]][player_2_loc[1]] = '-'
            player_2_loc[1] -= 1
            current_board_state[player_2_loc[0]][player_2_loc[1]] = '*'

def move_right(player_number, entity):
    if player_number == 1:
        if player_1_loc[1] < 9:
            current_board_state[player_1_loc[0]][player_1_loc[1]] = '-'
            player_1_loc[1] += 1
            current_board_state[player_1_loc[0]][player_1_loc[1]] = '*'
    elif player_number == 2:
        if player_2_loc[1] < 9:
            current_board_state[player_2_loc[0]][player_2_loc[1]] = '-'
            player_2_loc[1] += 1
            current_board_state[player_2_loc[0]][player_2_loc[1]] = '*'

def fireball(player_number, client):
    if player_number == 1:
        fireball_loc = [player_1_loc[0], player_1_loc[1]]
        msg = client.recv(1024)
        key = pickle.loads(msg)