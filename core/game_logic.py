import json
import os
from items.items import Food, Armor, Weapon
from core.character import Character
import config.config as config
from PyQt6.QtCore import QTime, QCoreApplication
from core.events import EventManager

class GameLogic:
    def __init__(self):
        self.character = Character.random_character()
        self.companions = []
        self.team = [self.character]
        self.speed_per_minute = config.SPEED_PER_MINUTE
        self.hunger = config.INITIAL_HUNGER
        self.thirst = config.INITIAL_THIRST
        self.fatigue = config.INITIAL_FATIGUE
        self.mood = config.INITIAL_MOOD
        self.is_traveling = True
        self.day_count = 1
        self.distance = 0.0
        self.inventory = self.initialize_inventory()
        self.log = []
        self.game_time = QTime(0, 0)

        self.event_manager = EventManager(self)

    def initialize_inventory(self):
        inventory = {}
        items_file_path = os.path.join(os.path.dirname(__file__), '..', 'items', 'items.json')
        with open(items_file_path, 'r', encoding='utf-8') as f:
            items_data = json.load(f)
            for item_name, quantity in config.INITIAL_INVENTORY.items():
                for item_type, items in items_data.items():
                    if item_name in items:
                        item_data = items[item_name]
                        if item_type == "Food":
                            item_name_translated = QCoreApplication.translate("Items", item_name)
                            hunger_restore = item_data["hunger_restore"]
                            thirst_restore = item_data["thirst_restore"]
                            weight = item_data["weight"]
                            value = item_data["value"]
                            inventory[item_name_translated] = Food(item_name_translated, quantity, hunger_restore, thirst_restore, weight, value)
                        elif item_type == "Weapon":
                            item_name_translated = QCoreApplication.translate("Items", item_name)
                            attack = item_data["attack"]
                            weight = item_data["weight"]
                            value = item_data["value"]
                            inventory[item_name_translated] = Weapon(item_name_translated, quantity, attack, weight, value)
                        elif item_type == "Armor":
                            item_name_translated = QCoreApplication.translate("Items", item_name)
                            defense = item_data["defense"]
                            weight = item_data["weight"]
                            value = item_data["value"]
                            inventory[item_name_translated] = Armor(item_name_translated, quantity, defense, weight, value)
        return inventory

    def update_time_and_distance(self):
        if self.is_traveling:
            self.distance += self.speed_per_minute
            self.thirst -= 0.1
            self.hunger -= 0.2
            self.fatigue -= 0.5
            self.mood -= 0.1
            self.event_manager.trigger_random_event()
        else:
            self.thirst -= 0.01
            self.hunger -= 0.02
            self.fatigue -= 0.05
            self.mood -= 0.05

        self.thirst = max(self.thirst, 0)
        self.hunger = max(self.hunger, 0)
        self.fatigue = max(self.fatigue, 0)
        self.mood = max(self.mood, 0)

    def discard_item(self, item_name):
        if item_name in self.inventory:
            del self.inventory[item_name]
            self.log.append(f"You discarded {item_name}")

    def eat_item(self, item_name):
        if item_name in self.inventory and isinstance(self.inventory[item_name], Food):
            food = self.inventory[item_name]
            self.hunger = min(self.hunger + food.hunger_restore, 100)
            self.thirst = min(self.thirst + food.thirst_restore, 100)
            food.quantity -= 1
            if food.quantity <= 0:
                del self.inventory[item_name]
            self.log.append(f"You ate an {item_name}")
