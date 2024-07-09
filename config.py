# config.py

# 游戏配置常量
SPEED_PER_MINUTE = 80  # 每分钟80米
INITIAL_HUNGER = 100
INITIAL_THIRST = 100
INITIAL_FATIGUE = 100
INITIAL_MOOD = 100

# 物品初始配置
INITIAL_INVENTORY = {
    "苹果": {"type": "Food", "hunger_restore": 20, "thirst_restore": 10},
    "剑": {"type": "Weapon", "attack": 10},
    "盾牌": {"type": "Armor", "defense": 5},
    "戒指": {"type": "Accessory", "effect": "魔法增强"},
    "背包": {"type": "Backpack", "capacity": 50},
    "马": {"type": "Mount", "speed_bonus": 20},
    "马车": {"type": "Carriage", "capacity": 200, "speed_bonus": 10}
}
