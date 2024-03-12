import pickle
import uuid
from variables import *
from map import *
from game import *

class DroppedItem:
    def __init__(self, item, location):
        self.dropped_item_id = uuid.uuid4().hex
        self.item = item
        self.location = location

def move_down(entity):
        if entity.location[1] < MAP_DIMENSIONS[1]:
            if entity.entity_id == 'player':
                world_map[entity.location[0]][entity.location[1]].players.remove(entity.player_id)
                entity.location[1] += 1
                world_map[entity.location[0]][entity.location[1]].players.add(entity.player_id)

def move_up(entity):
    if entity.location[1] > 0:
            if entity.entity_id == 'player':
                world_map[entity.location[0]][entity.location[1]].players.remove(entity.player_id)
                entity.location[1] -= 1
                world_map[entity.location[0]][entity.location[1]].players.add(entity.player_id)

def move_left(entity):
    if entity.location[0] > 0:
            if entity.entity_id == 'player':
                world_map[entity.location[0]][entity.location[1]].players.remove(entity.player_id)
                entity.location[0] -= 1
                world_map[entity.location[0]][entity.location[1]].players.add(entity.player_id)

def move_right(entity):
    if entity.location[0] < MAP_DIMENSIONS[1]:
            if entity.entity_id == 'player':
                world_map[entity.location[0]][entity.location[1]].players.remove(entity.player_id)
                entity.location[0] += 1
                world_map[entity.location[0]][entity.location[1]].players.add(entity.player_id)

def fireball(client):
    fireball_loc = [player_1_loc[0], player_1_loc[1]]
    msg = client.recv(1024)
    key = pickle.loads(msg)