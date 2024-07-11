from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QProgressBar, QPushButton, QTextEdit, QListWidget, QHBoxLayout, QComboBox
)
from PyQt6.QtCore import Qt

class TravelTab(QWidget):
    def __init__(self, game, toggle_state, change_speed, toggle_pause, show_character_details):
        super().__init__()

        self.game = game
        self.toggle_state = toggle_state
        self.change_speed = change_speed
        self.toggle_pause = toggle_pause
        self.show_character_details = show_character_details

        self.character_name_label = QLabel(f"Player: {self.game.character.name}", self)  # 显示玩家角色名字

        self.time_label = QLabel(self)
        self.distance_label = QLabel(self)

        self.hunger_bar = QProgressBar(self)
        self.hunger_bar.setMaximum(100)
        self.hunger_bar.setValue(int(self.game.hunger))
        self.hunger_bar.setFormat("Hunger: %p%")

        self.thirst_bar = QProgressBar(self)
        self.thirst_bar.setMaximum(100)
        self.thirst_bar.setValue(int(self.game.thirst))
        self.thirst_bar.setFormat("Thirst: %p%")

        self.fatigue_bar = QProgressBar(self)
        self.fatigue_bar.setMaximum(100)
        self.fatigue_bar.setValue(int(self.game.fatigue))
        self.fatigue_bar.setFormat("Fatigue: %p%")

        self.mood_bar = QProgressBar(self)
        self.mood_bar.setMaximum(100)
        self.mood_bar.setValue(int(self.game.mood))
        self.mood_bar.setFormat("Mood: %p%")

        self.toggle_button = QPushButton("Rest", self)
        self.toggle_button.clicked.connect(self.toggle_state)

        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.toggle_pause)

        self.speed_combo = QComboBox(self)
        self.speed_combo.addItems(["1x", "2x", "5x", "10x"])
        self.speed_combo.currentIndexChanged.connect(lambda index: self.change_speed(index, update_combo=False))

        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)

        self.companions_list = QListWidget(self)
        self.companions_list.itemClicked.connect(self.show_character_details)  # 点击同路人显示详情

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.toggle_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.speed_combo)

        travel_layout = QVBoxLayout()
        travel_layout.addWidget(self.character_name_label)  # 添加玩家角色名字标签
        travel_layout.addWidget(self.time_label)
        travel_layout.addWidget(self.distance_label)
        travel_layout.addWidget(self.hunger_bar)
        travel_layout.addWidget(self.thirst_bar)
        travel_layout.addWidget(self.fatigue_bar)
        travel_layout.addWidget(self.mood_bar)
        travel_layout.addLayout(control_layout)
        travel_layout.addWidget(self.log_text)
        travel_layout.addWidget(QLabel("Companions:"))  # 标签
        travel_layout.addWidget(self.companions_list)

        self.setLayout(travel_layout)

    def update_labels(self):
        time_text = f"Day {self.game.day_count}, {self.game.game_time.toString('HH:mm')}"
        distance_text = f"Distance traveled: {int(self.game.distance)} meters"
        self.time_label.setText(time_text)
        self.distance_label.setText(distance_text)

        self.hunger_bar.setValue(int(self.game.hunger))
        self.thirst_bar.setValue(int(self.game.thirst))
        self.fatigue_bar.setValue(int(self.game.fatigue))
        self.mood_bar.setValue(int(self.game.mood))

    def update_log(self):
        self.log_text.clear()
        self.log_text.append("\n".join(self.game.log))

    def update_companions(self):
        self.companions_list.clear()
        for companion in self.game.companions:
            self.companions_list.addItem(companion.name)
