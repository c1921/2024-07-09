# game_logic.py

import random
from items import Item, Food, Armor, Weapon
import config

class GameLogic:
    def __init__(self):
        # 初始化游戏状态
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

    def initialize_inventory(self):
        inventory = {}
        for item_name, item_data in config.INITIAL_INVENTORY.items():
            if item_data["type"] == "Food":
                inventory[item_name] = Food(item_name, item_data["quantity"], item_data["hunger_restore"], item_data["thirst_restore"])
            elif item_data["type"] == "Weapon":
                inventory[item_name] = Weapon(item_name, item_data["quantity"], item_data["attack"])
            elif item_data["type"] == "Armor":
                inventory[item_name] = Armor(item_name, item_data["quantity"], item_data["defense"])
        return inventory

    def update_time_and_distance(self):
        if self.is_traveling:
            self.distance += self.speed_per_minute
            self.thirst -= 0.1
            self.hunger -= 0.2
            self.fatigue -= 0.5
            self.mood -= 0.1
            self.random_event()
        else:
            self.thirst -= 0.01
            self.hunger -= 0.02
            self.fatigue -= 0.05
            self.mood -= 0.05

        self.thirst = max(self.thirst, 0)
        self.hunger = max(self.hunger, 0)
        self.fatigue = max(self.fatigue, 0)
        self.mood = max(self.mood, 0)

    def random_event(self):
        # 50%概率获得一个苹果
        if random.random() < 0.5:
            if "Apple" in self.inventory:
                self.inventory["Apple"].quantity += 1
            else:
                self.inventory["Apple"] = Food("Apple", 1, hunger_restore=20, thirst_restore=10)
            self.log.append("You found an apple!")
    
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
