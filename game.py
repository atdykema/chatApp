import pickle
import uuid
from server import server_settings
from map import world_map
from map import *

class DroppedItem:
    def __init__(self, item, location):
        self.dropped_item_id = uuid.uuid4().hex
        self.item = item
        self.location = location

def move_down(entity):
        if entity.location[1] < server_settings.MAP_DIMENSIONS[1]:
            if entity.entity_id == 'player':
                if world_map[entity.location[0]][entity.location[1] + 1].properties.is_occupied == False:
                    world_map[entity.location[0]][entity.location[1]].players.remove(entity.player_id)
                    entity.location[1] += 1
                    world_map[entity.location[0]][entity.location[1]].players.add(entity.player_id)

def move_up(entity):
    if entity.location[1] > 0:
            if entity.entity_id == 'player':
                if world_map[entity.location[0]][entity.location[1] - 1].properties.is_occupied == False:
                    world_map[entity.location[0]][entity.location[1]].players.remove(entity.player_id)
                    entity.location[1] -= 1
                    world_map[entity.location[0]][entity.location[1]].players.add(entity.player_id)

def move_left(entity):
    if entity.location[0] > 0:
            if entity.entity_id == 'player':
                if world_map[entity.location[0] - 1][entity.location[1]].properties.is_occupied == False:
                    world_map[entity.location[0]][entity.location[1]].players.remove(entity.player_id)
                    entity.location[0] -= 1
                    world_map[entity.location[0]][entity.location[1]].players.add(entity.player_id)

def move_right(entity):
    if entity.location[0] < server_settings.MAP_DIMENSIONS[1]:
            if entity.entity_id == 'player':
                if world_map[entity.location[0] + 1][entity.location[1]].properties.is_occupied == False:
                    world_map[entity.location[0]][entity.location[1]].players.remove(entity.player_id)
                    entity.location[0] += 1
                    world_map[entity.location[0]][entity.location[1]].players.add(entity.player_id)