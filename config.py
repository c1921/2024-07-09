# config.py

# 游戏配置常量
SPEED_PER_MINUTE = 80  # 每分钟80米
INITIAL_HUNGER = 100
INITIAL_THIRST = 100
INITIAL_FATIGUE = 100
INITIAL_MOOD = 100

# 计时器触发间隔（毫秒）
TIMER_INTERVAL = 1000  # 1秒

# 初始背包物品配置
INITIAL_INVENTORY = {
    "Apple": 10,
    "Blueberry": 15,
    "Mulberry": 20,
    "Sword": 1
}

# 游戏中所有物品定义
ITEM_DEFINITIONS = {
    "Food": {
        "Apple": [20, 10],
        "Blueberry": [10, 5],
        "Mulberry": [15, 7]
    },
    "Weapon": {
        "Sword": {"attack": 10}
    }
}
