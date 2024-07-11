class Item:
    def __init__(self, name, quantity, weight, value):
        self.name = name
        self.quantity = quantity
        self.weight = weight
        self.value = value

class Food(Item):
    def __init__(self, name, quantity, hunger_restore, thirst_restore, weight, value):
        super().__init__(name, quantity, weight, value)
        self.hunger_restore = hunger_restore
        self.thirst_restore = thirst_restore

class Armor(Item):
    def __init__(self, name, quantity, defense, weight, value):
        super().__init__(name, quantity, weight, value)
        self.defense = defense

class Weapon(Item):
    def __init__(self, name, quantity, attack, weight, value):
        super().__init__(name, quantity, weight, value)
        self.attack = attack
