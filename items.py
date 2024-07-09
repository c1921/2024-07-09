# items.py

class Item:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

class Food(Item):
    def __init__(self, name, quantity, hunger_restore, thirst_restore):
        super().__init__(name, quantity)
        self.hunger_restore = hunger_restore
        self.thirst_restore = thirst_restore

class Armor(Item):
    def __init__(self, name, quantity, defense):
        super().__init__(name, quantity)
        self.defense = defense

class Weapon(Item):
    def __init__(self, name, quantity, attack):
        super().__init__(name, quantity)
        self.attack = attack

class Accessory(Item):
    def __init__(self, name, quantity, effect):
        super().__init__(name, quantity)
        self.effect = effect

class Backpack(Item):
    def __init__(self, name, quantity, capacity):
        super().__init__(name, quantity)
        self.capacity = capacity

class Mount(Item):
    def __init__(self, name, quantity, speed_bonus):
        super().__init__(name, quantity)
        self.speed_bonus = speed_bonus

class Carriage(Item):
    def __init__(self, name, quantity, capacity, speed_bonus):
        super().__init__(name, quantity)
        self.capacity = capacity
        self.speed_bonus = speed_bonus
