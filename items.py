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
