import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QListWidget, QPushButton,
    QProgressBar
)
from PyQt6.QtCore import QTimer, QTime

class AdventureRPG(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化时间和距离
        self.game_time = QTime(0, 0)
        self.day_count = 1
        self.distance = 0.0
        self.speed_per_minute = 80  # 每分钟80米

        # 初始化物品栏
        self.inventory = {"Apple": 10}

        # 初始化角色状态
        self.hunger = 100
        self.thirst = 100
        self.fatigue = 100
        self.mood = 100
        self.is_traveling = True

        # 设置窗口
        self.setWindowTitle("Adventure RPG")
        self.setGeometry(100, 100, 600, 400)

        # 创建标签
        self.time_label = QLabel(self)
        self.distance_label = QLabel(self)

        # 创建物品栏列表
        self.inventory_list = QListWidget(self)

        # 创建角色状态进度条
        self.hunger_bar = QProgressBar(self)
        self.hunger_bar.setMaximum(100)
        self.hunger_bar.setValue(int(self.hunger))
        self.hunger_bar.setFormat("Hunger: %p%")

        self.thirst_bar = QProgressBar(self)
        self.thirst_bar.setMaximum(100)
        self.thirst_bar.setValue(int(self.thirst))
        self.thirst_bar.setFormat("Thirst: %p%")

        self.fatigue_bar = QProgressBar(self)
        self.fatigue_bar.setMaximum(100)
        self.fatigue_bar.setValue(int(self.fatigue))
        self.fatigue_bar.setFormat("Fatigue: %p%")

        self.mood_bar = QProgressBar(self)
        self.mood_bar.setMaximum(100)
        self.mood_bar.setValue(int(self.mood))
        self.mood_bar.setFormat("Mood: %p%")

        # 创建按钮
        self.toggle_button = QPushButton("Rest", self)
        self.toggle_button.clicked.connect(self.toggle_state)

        # 布局
        state_layout = QVBoxLayout()
        state_layout.addWidget(self.hunger_bar)
        state_layout.addWidget(self.thirst_bar)
        state_layout.addWidget(self.fatigue_bar)
        state_layout.addWidget(self.mood_bar)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.time_label)
        main_layout.addWidget(self.distance_label)
        main_layout.addWidget(self.inventory_list)
        main_layout.addLayout(state_layout)
        main_layout.addWidget(self.toggle_button)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # 设置计时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_and_distance)
        self.timer.start(1000)  # 每秒触发一次

        # 更新标签显示
        self.update_labels()
        self.update_inventory()

    def update_time_and_distance(self):
        # 更新游戏时间
        self.game_time = self.game_time.addSecs(60)
        if self.game_time.hour() == 0 and self.game_time.minute() == 0:
            self.day_count += 1

        if self.is_traveling:
            # 更新距离
            self.distance += self.speed_per_minute

            # 更新状态
            self.thirst -= 0.1
            self.hunger -= 0.2
            self.fatigue -= 0.5
            self.mood -= 0.1
        else:
            # 更新状态
            self.thirst -= 0.01
            self.hunger -= 0.02
            self.fatigue -= 0.05
            self.mood -= 0.05

        # 确保状态值不低于0
        self.thirst = max(self.thirst, 0)
        self.hunger = max(self.hunger, 0)
        self.fatigue = max(self.fatigue, 0)
        self.mood = max(self.mood, 0)

        # 更新标签显示
        self.update_labels()

    def update_labels(self):
        time_text = f"Day {self.day_count}, {self.game_time.toString('HH:mm')}"
        distance_text = f"Distance traveled: {self.distance:.2f} meters"
        self.time_label.setText(time_text)
        self.distance_label.setText(distance_text)

        self.hunger_bar.setValue(int(self.hunger))
        self.thirst_bar.setValue(int(self.thirst))
        self.fatigue_bar.setValue(int(self.fatigue))
        self.mood_bar.setValue(int(self.mood))

    def update_inventory(self):
        self.inventory_list.clear()
        for item, quantity in self.inventory.items():
            self.inventory_list.addItem(f"{item}: {quantity}")

    def toggle_state(self):
        self.is_traveling = not self.is_traveling
        self.toggle_button.setText("Travel" if not self.is_traveling else "Rest")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    rpg = AdventureRPG()
    rpg.show()
    sys.exit(app.exec())
