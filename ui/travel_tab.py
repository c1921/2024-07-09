from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QProgressBar, QPushButton, QTextEdit, QListWidget, QHBoxLayout, QComboBox, QListWidgetItem
)
from PyQt6.QtCore import Qt, QCoreApplication
from PyQt6.QtGui import QFontMetrics

class TravelTab(QWidget):
    def __init__(self, game, toggle_state, change_speed, toggle_pause, show_character_details):
        super().__init__()

        self.game = game
        self.toggle_state = toggle_state
        self.change_speed = change_speed
        self.toggle_pause = toggle_pause
        self.show_character_details = show_character_details

        self.name_label = QLabel(self)
        self.name_label.setText(QCoreApplication.translate("TravelTab", "Player: ") + self.game.character.name)

        self.time_label = QLabel(self)
        self.distance_label = QLabel(self)

        self.hunger_bar = self.create_progress_bar()
        self.hunger_label = QLabel(self)

        self.thirst_bar = self.create_progress_bar()
        self.thirst_label = QLabel(self)

        self.fatigue_bar = self.create_progress_bar()
        self.fatigue_label = QLabel(self)

        self.mood_bar = self.create_progress_bar()
        self.mood_label = QLabel(self)

        self.toggle_button = QPushButton(QCoreApplication.translate("TravelTab", "Rest"), self)
        self.toggle_button.clicked.connect(self.toggle_state)

        self.pause_button = QPushButton(QCoreApplication.translate("TravelTab", "Pause"), self)
        self.pause_button.clicked.connect(self.toggle_pause)

        self.speed_combo = QComboBox(self)
        self.speed_combo.addItems([
            QCoreApplication.translate("TravelTab", "1x"),
            QCoreApplication.translate("TravelTab", "2x"),
            QCoreApplication.translate("TravelTab", "5x"),
            QCoreApplication.translate("TravelTab", "10x")
        ])
        self.speed_combo.currentIndexChanged.connect(lambda index: self.change_speed(index, update_combo=False))

        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)

        self.companions_list = QListWidget(self)
        self.companions_list.itemClicked.connect(self.on_companion_clicked)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.toggle_button)
        control_layout.addWidget(self.pause_button)
        control_layout.addWidget(self.speed_combo)

        travel_layout = QVBoxLayout()
        travel_layout.addWidget(self.name_label)
        travel_layout.addWidget(self.time_label)
        travel_layout.addWidget(self.distance_label)

        # 动态计算标签的最大宽度
        self.max_label_width = self.calculate_max_label_width([
            QCoreApplication.translate("TravelTab", "Hunger:"),
            QCoreApplication.translate("TravelTab", "Thirst:"),
            QCoreApplication.translate("TravelTab", "Fatigue:"),
            QCoreApplication.translate("TravelTab", "Mood:")
        ])

        travel_layout.addLayout(self.create_bar_layout(QCoreApplication.translate("TravelTab", "Hunger:"), self.hunger_bar, self.hunger_label))
        travel_layout.addLayout(self.create_bar_layout(QCoreApplication.translate("TravelTab", "Thirst:"), self.thirst_bar, self.thirst_label))
        travel_layout.addLayout(self.create_bar_layout(QCoreApplication.translate("TravelTab", "Fatigue:"), self.fatigue_bar, self.fatigue_label))
        travel_layout.addLayout(self.create_bar_layout(QCoreApplication.translate("TravelTab", "Mood:"), self.mood_bar, self.mood_label))
        travel_layout.addLayout(control_layout)
        travel_layout.addWidget(self.log_text)
        travel_layout.addWidget(QLabel(QCoreApplication.translate("TravelTab", "Companions:")))
        travel_layout.addWidget(self.companions_list)

        self.setLayout(travel_layout)

    def create_progress_bar(self):
        bar = QProgressBar(self)
        bar.setMaximum(100)
        bar.setValue(0)
        return bar

    def create_bar_layout(self, text, bar, value_label):
        layout = QHBoxLayout()
        label = QLabel(text, self)
        label.setFixedWidth(self.max_label_width)  # 设置最大宽度确保对齐
        layout.addWidget(label)
        layout.addWidget(bar)
        layout.addWidget(value_label)
        return layout

    def calculate_max_label_width(self, texts):
        font_metrics = QFontMetrics(self.font())
        return max(font_metrics.horizontalAdvance(text) for text in texts)

    def update_labels(self):
        time_text = QCoreApplication.translate("TravelTab", "Day {day}, {time}").format(
            day=self.game.day_count,
            time=self.game.game_time.toString('HH:mm')
        )
        distance_text = QCoreApplication.translate("TravelTab", "Distance traveled: {distance} meters").format(
            distance=int(self.game.distance)
        )
        self.time_label.setText(time_text)
        self.distance_label.setText(distance_text)

        self.hunger_bar.setValue(int(self.game.hunger))
        self.thirst_bar.setValue(int(self.game.thirst))
        self.fatigue_bar.setValue(int(self.game.fatigue))
        self.mood_bar.setValue(int(self.game.mood))

    def update_log(self):
        self.log_text.clear()
        self.log_text.append("\n".join(self.game.log))

    def update_companions(self, new_companions):
        current_ids = [self.companions_list.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.companions_list.count())]
        new_ids = [comp.id for comp in new_companions]

        if set(current_ids) != set(new_ids):
            self.companions_list.clear()
            for companion in new_companions:
                item = QListWidgetItem(companion.name)
                item.setData(Qt.ItemDataRole.UserRole, companion.id)
                self.companions_list.addItem(item)

    def on_companion_clicked(self, item):
        companion_id = item.data(Qt.ItemDataRole.UserRole)
        companion = next((comp for comp in self.game.companions if comp.id == companion_id), None)
        if companion:
            self.show_character_details(companion)
