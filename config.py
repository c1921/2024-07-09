# config.py

# 游戏配置常量
SPEED_PER_MINUTE = 80  # 每分钟80米
INITIAL_HUNGER = 100
INITIAL_THIRST = 100
INITIAL_FATIGUE = 100
INITIAL_MOOD = 100

# 物品初始配置
INITIAL_INVENTORY = {
    "Apple": {"type": "Food", "quantity": 10, "hunger_restore": 20, "thirst_restore": 10},
    "Sword": {"type": "Weapon", "quantity": 1, "attack": 10},
    "Shield": {"type": "Armor", "quantity": 1, "defense": 5},
    "Ring": {"type": "Accessory", "quantity": 1, "effect": "Magic Boost"},
    "Backpack": {"type": "Backpack", "quantity": 1, "capacity": 50},
    "Horse": {"type": "Mount", "quantity": 1, "speed_bonus": 20},
    "Carriage": {"type": "Carriage", "quantity": 1, "capacity": 200, "speed_bonus": 10}
}
