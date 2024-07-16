import json
import os
import uuid
from datetime import datetime
from PyQt6.QtCore import QTime
from items.items import Food, Weapon, Armor
from core.character import Character

class SaveManager:
    def __init__(self, game):
        self.game = game
        self.save_file = "save/save.json"
        self.items_file_path = os.path.join(os.path.dirname(__file__), '..', 'items', 'items.json')
        with open(self.items_file_path, 'r', encoding='utf-8') as f:
            self.items_data = json.load(f)

    def save_game(self):
        save_data = {
            "character": {
                "name": self.game.character.name,
                "attributes": self.game.character.attributes,
                "skills": self.game.character.skills,
                "inventory": {item.name: {"quantity": item.quantity, "weight": item.weight, "value": item.value} for item in self.game.inventory.values()}
            },
            "companions": [{"id": str(comp.id), "name": comp.name, "attributes": comp.attributes, "skills": comp.skills} for comp in self.game.companions],
            "team": [{"id": str(comp.id), "name": comp.name, "attributes": comp.attributes, "skills": comp.skills} for comp in self.game.team],
            "state": {
                "hunger": self.game.hunger,
                "thirst": self.game.thirst,
                "fatigue": self.game.fatigue,
                "mood": self.game.mood,
                "is_traveling": self.game.is_traveling,
                "day_count": self.game.day_count,
                "distance": self.game.distance,
                "game_time": self.game.game_time.toString('HH:mm')
            },
            "log": self.game.log
        }
        with open(self.save_file, 'w') as f:
            json.dump(save_data, f, indent=4)
        print(f"Game saved at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def load_game(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
                self.game.character.name = save_data["character"]["name"]
                self.game.character.attributes = save_data["character"]["attributes"]
                self.game.character.skills = save_data["character"]["skills"]
                self.game.inventory = self._load_inventory(save_data["character"]["inventory"])
                self.game.companions = self._load_companions(save_data.get("companions", []))
                self.game.team = self._load_companions(save_data.get("team", [self.game.character]))  # Initialize team with main character if not present
                self.game.hunger = save_data["state"]["hunger"]
                self.game.thirst = save_data["state"]["thirst"]
                self.game.fatigue = save_data["state"]["fatigue"]
                self.game.mood = save_data["state"]["mood"]
                self.game.is_traveling = save_data["state"]["is_traveling"]
                self.game.day_count = save_data["state"]["day_count"]
                self.game.distance = save_data["state"]["distance"]
                self.game.game_time = QTime.fromString(save_data["state"]["game_time"], 'HH:mm')
                self.game.log = save_data["log"]
            print("Game loaded successfully")

    def _load_inventory(self, inventory_data):
        inventory = {}
        for item_name, item_data in inventory_data.items():
            if item_name in self.items_data["Food"]:
                item_info = self.items_data["Food"][item_name]
                inventory[item_name] = Food(item_name, item_data["quantity"], item_info["hunger_restore"], item_info["thirst_restore"], item_data["weight"], item_data["value"])
            elif item_name in self.items_data["Weapon"]:
                item_info = self.items_data["Weapon"][item_name]
                inventory[item_name] = Weapon(item_name, item_data["quantity"], item_info["attack"], item_data["weight"], item_data["value"])
            elif item_name in self.items_data["Armor"]:
                item_info = self.items_data["Armor"][item_name]
                inventory[item_name] = Armor(item_name, item_data["quantity"], item_info["defense"], item_data["weight"], item_data["value"])
        return inventory

    def _load_companions(self, companions_data):
        companions = []
        for comp_data in companions_data:
            companion = Character(comp_data["name"])
            companion.id = uuid.UUID(comp_data["id"])
            companion.attributes = comp_data["attributes"]
            companion.skills = comp_data["skills"]
            companions.append(companion)
        return companions
