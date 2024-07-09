# character.py

import random

class Character:
    def __init__(self, name, strength, agility, charisma, intelligence, attack, armor):
        self.name = name
        self.strength = strength
        self.agility = agility
        self.charisma = charisma
        self.intelligence = intelligence
        self.attack = attack
        self.armor = armor

    def interact(self):
        event = random.choices(["nothing", "talk", "fight"], [0.5, 0.3, 0.2])[0]
        return event

    def fight(self, opponent):
        self_power = self.attack + random.randint(-10, 10)
        opponent_power = opponent.attack + random.randint(-10, 10)
        return "win" if self_power >= opponent_power else "lose"
