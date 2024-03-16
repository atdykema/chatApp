import uuid
from server import server_settings

class Player:
    def __init__(self, alias, location=server_settings.PLAYER_SPAWN, skills=None, inventory=None, equipment=None):
        self.player_id = uuid.uuid4().hex
        self.entity_id = 'player'
        self.alias = alias
        self.location = location

        if skills is None:
            self.skills = Skills()

        if inventory is None:
            self.inventory = Inventory()

        if equipment is None:
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

class Item:
    def __init__(self, item):
        self.item_id = uuid.uuid4().hex
        self.item = item