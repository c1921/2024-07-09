from enum import Enum, auto

class TraitType(Enum):
    PERSONALITY = auto()
    PHYSIOLOGY = auto()
    EXPERIENCE = auto()

class Trait:
    def __init__(self, name, trait_type, exclusive_traits=None):
        self.name = name
        self.trait_type = trait_type
        self.exclusive_traits = exclusive_traits or []

# 定义性格特质
BRAVE = Trait("Brave", TraitType.PERSONALITY, ["Cowardly"])
COWARDLY = Trait("Cowardly", TraitType.PERSONALITY, ["Brave"])
CALM = Trait("Calm", TraitType.PERSONALITY, ["Hot-tempered"])
HOT_TEMPERED = Trait("Hot-tempered", TraitType.PERSONALITY, ["Calm"])
LOYAL = Trait("Loyal", TraitType.PERSONALITY, ["Lustful"])
LUSTFUL = Trait("Lustful", TraitType.PERSONALITY, ["Loyal"])
DILIGENT = Trait("Diligent", TraitType.PERSONALITY, ["Lazy"])
LAZY = Trait("Lazy", TraitType.PERSONALITY, ["Diligent"])

# 将所有特质放在一个列表中，方便以后使用
ALL_TRAITS = [BRAVE, COWARDLY, CALM, HOT_TEMPERED, LOYAL, LUSTFUL, DILIGENT, LAZY]
