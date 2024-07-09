# config.py

# 游戏配置常量
SPEED_PER_MINUTE = 80  # 每分钟80米
INITIAL_HUNGER = 100
INITIAL_THIRST = 100
INITIAL_FATIGUE = 100
INITIAL_MOOD = 100

# 物品初始配置
INITIAL_INVENTORY = {
    "苹果": {"type": "Food", "quantity": 10, "hunger_restore": 20, "thirst_restore": 10},
    "剑": {"type": "Weapon", "quantity": 1, "attack": 10},
    "盾牌": {"type": "Armor", "quantity": 1, "defense": 5},
    "戒指": {"type": "Accessory", "quantity": 1, "effect": "魔法增强"},
    "背包": {"type": "Backpack", "quantity": 1, "capacity": 50},
    "马": {"type": "Mount", "quantity": 1, "speed_bonus": 20},
    "马车": {"type": "Carriage", "quantity": 1, "capacity": 200, "speed_bonus": 10}
}

EQUIPMENT_SLOTS = {
    "weapon": "武器",
    "armor": "护甲",
    "accessory": "饰品",
    "backpack": "背包",
    "mount": "坐骑",
    "carriage": "马车"
}