import random
from core.character import Character
from items.items import Food
import config.config as config

class EventManager:
    def __init__(self, game):
        self.game = game

    def trigger_random_event(self):
        event_probabilities = {
            "find_apple": 0.5,
            "meet_character": 0.1,
            # 可以在这里添加更多事件及其概率
        }
        for event, probability in event_probabilities.items():
            if random.random() < probability:
                getattr(self, event)()

    def find_apple(self):
        if "Apple" in self.game.inventory:
            self.game.inventory["Apple"].quantity += 1
        else:
            hunger_restore, thirst_restore, weight, value = config.ITEM_DEFINITIONS["Food"]["Apple"]
            self.game.inventory["Apple"] = Food("Apple", 1, hunger_restore, thirst_restore, weight, value)
        self.game.log.append("You found an apple!")

    def meet_character(self):
        new_companion = Character.random_character()
        self.game.companions.append(new_companion)
        self.game.log.append(f"You met {new_companion.name}!")

    # 可以在这里添加更多事件的处理方法
