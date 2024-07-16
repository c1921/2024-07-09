import random
import uuid
from core.traits import ALL_TRAITS, Trait

class Character:
    def __init__(self, name):
        self.id = uuid.uuid4()
        self.name = name
        self.inventory = {}
        self.affinity = 0  # 好感度默认为 0
        self.attributes = {
            'Strength': random.randint(1, 10),
            'Agility': random.randint(1, 10),
            'Charisma': random.randint(1, 10),
            'Intelligence': random.randint(1, 10)
        }
        self.skills = {
            'Running': random.randint(1, 10),
            'Riding': random.randint(1, 10),
            'Management': random.randint(1, 10),
            'Eloquence': random.randint(1, 10),
            'Gathering': random.randint(1, 10)
        }
        self.traits = self.assign_traits()

    def assign_traits(self):
        traits = random.sample(ALL_TRAITS, 3)  # 随机分配三个特质
        # 确保没有相互排斥的特质
        final_traits = []
        for trait in traits:
            if not any(t for t in final_traits if trait.name in t.exclusive_traits):
                final_traits.append(trait)
        return final_traits

    def calculate_affinity(self, other_character):
        affinity = 0
        for trait in self.traits:
            if trait in other_character.traits:
                affinity += 20
            if any(exclusive_trait in other_character.traits for exclusive_trait in trait.exclusive_traits):
                affinity -= 20
        return affinity

    @staticmethod
    def random_character():
        names = ["Alice", "Bob", "Charlie", "Diana", "Edward"]
        name = random.choice(names)
        return Character(name)
