# items.py

class Item:
    def __init__(self, name):
        self.name = name

class Food(Item):
    def __init__(self, name, hunger_restore, thirst_restore):
        super().__init__(name)
        self.hunger_restore = hunger_restore
        self.thirst_restore = thirst_restore

class Armor(Item):
    def __init__(self, name, defense):
        super().__init__(name)
        self.defense = defense

class Weapon(Item):
    def __init__(self, name, attack):
        super().__init__(name)
        self.attack = attack

class Accessory(Item):
    def __init__(self, name, effect):
        super().__init__(name)
        self.effect = effect

class Backpack(Item):
    def __init__(self, name, capacity):
        super().__init__(name)
        self.capacity = capacity

class Mount(Item):
    def __init__(self, name, speed_bonus):
        super().__init__(name)
        self.speed_bonus = speed_bonus

class Carriage(Item):
    def __init__(self, name, capacity, speed_bonus):
        super().__init__(name)
        self.capacity = capacity
        self.speed_bonus = speed_bonus
