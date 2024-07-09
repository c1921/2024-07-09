# game_logic.py

from items import Item, Food, Armor, Weapon, Accessory, Backpack, Mount, Carriage
from character import Character
import config
import random

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
        self.equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None,
            "backpack": None,
            "mount": None,
            "carriage": None
        }
        self.strength = 10
        self.agility = 10
        self.charisma = 10
        self.intelligence = 10
        self.attack = 0
        self.armor = 0
        self.update_combat_attributes()
        self.log = []
        self.character = Character("Player", self.strength, self.agility, self.charisma, self.intelligence, self.attack, self.armor)

    def initialize_inventory(self):
        inventory = {}
        for item_name, item_data in config.INITIAL_INVENTORY.items():
            if item_data["type"] == "Food":
                inventory[item_name] = Food(item_name, item_data["quantity"], item_data["hunger_restore"], item_data["thirst_restore"])
            elif item_data["type"] == "Weapon":
                inventory[item_name] = Weapon(item_name, item_data["quantity"], item_data["attack"])
            elif item_data["type"] == "Armor":
                inventory[item_name] = Armor(item_name, item_data["quantity"], item_data["defense"])
            elif item_data["type"] == "Accessory":
                inventory[item_name] = Accessory(item_name, item_data["quantity"], item_data["effect"])
            elif item_data["type"] == "Backpack":
                inventory[item_name] = Backpack(item_name, item_data["quantity"], item_data["capacity"])
            elif item_data["type"] == "Mount":
                inventory[item_name] = Mount(item_name, item_data["quantity"], item_data["speed_bonus"])
            elif item_data["type"] == "Carriage":
                inventory[item_name] = Carriage(item_name, item_data["quantity"], item_data["capacity"], item_data["speed_bonus"])
        return inventory

    def update_time_and_distance(self):
        if self.is_traveling:
            self.distance += self.speed_per_minute
            self.thirst -= 0.1
            self.hunger -= 0.2
            self.fatigue -= 0.5
            self.mood -= 0.1
            if random.random() < 0.1:  # 10% 的概率遇到其他角色
                self.encounter()
        else:
            self.thirst -= 0.01
            self.hunger -= 0.02
            self.fatigue -= 0.05
            self.mood -= 0.05

        self.thirst = max(self.thirst, 0)
        self.hunger = max(self.hunger, 0)
        self.fatigue = max(self.fatigue, 0)
        self.mood = max(self.mood, 0)

    def encounter(self):
        opponent = Character("Opponent", random.randint(5, 15), random.randint(5, 15), random.randint(5, 15), random.randint(5, 15), random.randint(5, 15), random.randint(5, 15))
        event = opponent.interact()
        if event == "nothing":
            self.log.append("You encountered someone, but nothing happened.")
        elif event == "talk":
            self.log.append("You encountered someone and had a conversation.")
        elif event == "fight":
            result = self.character.fight(opponent)
            if result == "win":
                self.log.append("You encountered someone and won the fight.")
            else:
                self.log.append("You encountered someone and lost the fight.")
                # You might want to add some logic here for what happens if you lose
                # such as losing health or items

    def discard_item(self, item_name):
        if item_name in self.inventory:
            del self.inventory[item_name]

    def eat_item(self, item_name):
        if item_name in self.inventory and isinstance(self.inventory[item_name], Food):
            food = self.inventory[item_name]
            self.hunger = min(self.hunger + food.hunger_restore, 100)
            self.thirst = min(self.thirst + food.thirst_restore, 100)
            food.quantity -= 1
            if food.quantity <= 0:
                del self.inventory[item_name]

    def equip_item(self, item_name):
        if item_name in self.inventory:
            item = self.inventory[item_name]
            if isinstance(item, Weapon):
                self.equipment["weapon"] = item
            elif isinstance(item, Armor):
                self.equipment["armor"] = item
            elif isinstance(item, Accessory):
                self.equipment["accessory"] = item
            elif isinstance(item, Backpack):
                self.equipment["backpack"] = item
            elif isinstance(item, Mount):
                self.equipment["mount"] = item
            elif isinstance(item, Carriage):
                self.equipment["carriage"] = item
            item.quantity -= 1
            if item.quantity <= 0:
                del self.inventory[item_name]
            self.update_combat_attributes()

    def unequip_item(self, slot):
        if slot in self.equipment and self.equipment[slot] is not None:
            item = self.equipment[slot]
            item_name = item.name
            if item_name in self.inventory:
                self.inventory[item_name].quantity += 1
            else:
                self.inventory[item_name] = item
                item.quantity = 1
            self.equipment[slot] = None
            self.update_combat_attributes()

    def update_combat_attributes(self):
        self.attack = 0
        self.armor = 0
        if self.equipment["weapon"]:
            self.attack += self.equipment["weapon"].attack
        if self.equipment["armor"]:
            self.armor += self.equipment["armor"].defense
