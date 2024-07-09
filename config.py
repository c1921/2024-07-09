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
    "Sword": {"type": "Weapon", "quantity": 1, "attack": 10}
}
