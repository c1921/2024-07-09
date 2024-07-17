from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QProgressBar, QPushButton, QTextEdit, QListWidget, QHBoxLayout, QComboBox, QListWidgetItem, QMenu
)
from PyQt6.QtCore import Qt, QCoreApplication, pyqtSlot, QPoint

class TravelTab(QWidget):
    def __init__(self, game, toggle_state, change_speed, toggle_pause, show_character_details, invite_to_team):
        super().__init__()

        self.game = game
        self.toggle_state = toggle_state
        self.change_speed = change_speed
        self.toggle_pause = toggle_pause
        self.show_character_details = show_character_details
        self.invite_to_team = invite_to_team

        self.name_label = QLabel(self)
        self.name_label.setText(QCoreApplication.translate("TravelTab", "Player: ") + self.game.character.name)

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

        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)

        self.companions_list = QListWidget(self)
        self.companions_list.itemClicked.connect(self.on_companion_clicked)
        self.companions_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.companions_list.customContextMenuRequested.connect(self.show_context_menu)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.toggle_button)

        travel_layout = QVBoxLayout()
        travel_layout.addWidget(self.name_label)

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
        font_metrics = self.fontMetrics()
        return max(font_metrics.horizontalAdvance(text) for text in texts)

    def update_labels(self):
        self.hunger_bar.setValue(int(self.game.hunger))
        self.thirst_bar.setValue(int(self.game.thirst))
        self.fatigue_bar.setValue(int(self.game.fatigue))
        self.mood_bar.setValue(int(self.game.mood))

    def update_log(self):
        self.log_text.append("\n".join(self.game.log))

    def update_companions(self):
        # 保存当前选中的项目
        selected_items = [self.companions_list.item(i).data(Qt.ItemDataRole.UserRole) for i in range(self.companions_list.count()) if self.companions_list.item(i).isSelected()]
        self.companions_list.clear()

        for companion in self.game.companions:
            item = QListWidgetItem(companion.name)
            item.setData(Qt.ItemDataRole.UserRole, companion.id)
            self.companions_list.addItem(item)
            if companion.id in selected_items:
                item.setSelected(True)

    def on_companion_clicked(self, item):
        companion_id = item.data(Qt.ItemDataRole.UserRole)
        companion = next((comp for comp in self.game.companions if comp.id == companion_id), None)
        if companion:
            self.show_character_details(companion)

    @pyqtSlot(QPoint)
    def show_context_menu(self, position):
        item = self.companions_list.itemAt(position)
        if item:
            companion_id = item.data(Qt.ItemDataRole.UserRole)
            companion = next((comp for comp in self.game.companions if comp.id == companion_id), None)
            if companion:
                menu = QMenu(self)
                talk_action = menu.addAction(QCoreApplication.translate("TravelTab", "Talk"))
                trade_action = menu.addAction(QCoreApplication.translate("TravelTab", "Trade"))
                invite_action = menu.addAction(QCoreApplication.translate("TravelTab", "Invite to Team"))
                attack_action = menu.addAction(QCoreApplication.translate("TravelTab", "Attack"))

                talk_action.triggered.connect(lambda: self.talk_to_companion(companion))
                trade_action.triggered.connect(lambda: self.trade_with_companion(companion))
                invite_action.triggered.connect(lambda: self.invite_to_team(companion))
                attack_action.triggered.connect(lambda: self.attack_companion(companion))

                menu.exec(self.companions_list.viewport().mapToGlobal(position))

    def talk_to_companion(self, companion):
        self.game.log.append(QCoreApplication.translate("TravelTab", "You talked to {name}.").format(name=companion.name))
        self.update_log()

    def trade_with_companion(self, companion):
        self.game.log.append(QCoreApplication.translate("TravelTab", "You traded with {name}.").format(name=companion.name))
        self.update_log()

    def invite_to_team(self, companion):
        self.invite_to_team(companion)

    def attack_companion(self, companion):
        self.game.log.append(QCoreApplication.translate("TravelTab", "You attacked {name}.").format(name=companion.name))
        self.update_log()
