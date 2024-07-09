import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton,
    QProgressBar, QMenu, QHBoxLayout
)
from PyQt6.QtCore import QTimer, QTime, Qt
from game_logic import GameLogic
from items import Food, Weapon, Armor, Accessory, Backpack, Mount, Carriage

class AdventureRPG(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化游戏逻辑
        self.game = GameLogic()

        # 初始化时间
        self.game_time = QTime(0, 0)

        # 设置窗口
        self.setWindowTitle("Adventure RPG")
        self.setGeometry(100, 100, 800, 600)

        # 创建标签
        self.time_label = QLabel(self)
        self.distance_label = QLabel(self)

        # 创建物品栏表格
        self.inventory_table = QTableWidget(self)
        self.inventory_table.setColumnCount(2)
        self.inventory_table.setHorizontalHeaderLabels(["Item", "Quantity"])
        self.inventory_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.inventory_table.customContextMenuRequested.connect(self.show_context_menu)
        self.inventory_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # 禁止编辑
        self.update_inventory()

        # 创建装备栏表格
        self.equipment_table = QTableWidget(self)
        self.equipment_table.setColumnCount(2)
        self.equipment_table.setHorizontalHeaderLabels(["Slot", "Item"])
        self.equipment_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # 禁止编辑
        self.update_equipment()

        # 创建角色状态进度条
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

        # 创建按钮
        self.toggle_button = QPushButton("Rest", self)
        self.toggle_button.clicked.connect(self.toggle_state)

        # 布局
        state_layout = QVBoxLayout()
        state_layout.addWidget(self.hunger_bar)
        state_layout.addWidget(self.thirst_bar)
        state_layout.addWidget(self.fatigue_bar)
        state_layout.addWidget(self.mood_bar)

        inventory_layout = QVBoxLayout()
        inventory_layout.addWidget(self.inventory_table)
        inventory_layout.addWidget(self.equipment_table)

        main_layout = QHBoxLayout()
        main_layout.addLayout(inventory_layout)
        main_layout.addLayout(state_layout)
        main_layout.addWidget(self.time_label)
        main_layout.addWidget(self.distance_label)
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

    def update_time_and_distance(self):
        self.game_time = self.game_time.addSecs(60)
        if self.game_time.hour() == 0 and self.game_time.minute() == 0:
            self.game.day_count += 1

        self.game.update_time_and_distance()
        self.update_labels()

    def update_labels(self):
        time_text = f"Day {self.game.day_count}, {self.game_time.toString('HH:mm')}"
        distance_text = f"Distance traveled: {int(self.game.distance)} meters"  # 将距离转换为整数
        self.time_label.setText(time_text)
        self.distance_label.setText(distance_text)

        self.hunger_bar.setValue(int(self.game.hunger))
        self.thirst_bar.setValue(int(self.game.thirst))
        self.fatigue_bar.setValue(int(self.game.fatigue))
        self.mood_bar.setValue(int(self.game.mood))

    def update_inventory(self):
        self.inventory_table.setRowCount(0)
        for item in self.game.inventory.values():
            row_position = self.inventory_table.rowCount()
            self.inventory_table.insertRow(row_position)
            item_name = QTableWidgetItem(item.name)
            item_name.setFlags(item_name.flags() & ~Qt.ItemFlag.ItemIsEditable)  # 禁止编辑
            item_name.setFlags(item_name.flags() & ~Qt.ItemFlag.ItemIsSelectable)  # 禁止选中文字
            item_quantity = QTableWidgetItem(str(item.quantity))
            item_quantity.setFlags(item_quantity.flags() & ~Qt.ItemFlag.ItemIsEditable)  # 禁止编辑
            item_quantity.setFlags(item_quantity.flags() & ~Qt.ItemFlag.ItemIsSelectable)  # 禁止选中文字
            self.inventory_table.setItem(row_position, 0, item_name)
            self.inventory_table.setItem(row_position, 1, item_quantity)

    def update_equipment(self):
        self.equipment_table.setRowCount(0)
        for slot, item in self.game.equipment.items():
            row_position = self.equipment_table.rowCount()
            self.equipment_table.insertRow(row_position)
            slot_name = QTableWidgetItem(slot)
            slot_name.setFlags(slot_name.flags() & ~Qt.ItemFlag.ItemIsEditable)  # 禁止编辑
            slot_name.setFlags(slot_name.flags() & ~Qt.ItemFlag.ItemIsSelectable)  # 禁止选中文字
            item_name = QTableWidgetItem(item.name if item else "None")
            item_name.setFlags(item_name.flags() & ~Qt.ItemFlag.ItemIsEditable)  # 禁止编辑
            item_name.setFlags(item_name.flags() & ~Qt.ItemFlag.ItemIsSelectable)  # 禁止选中文字
            self.equipment_table.setItem(row_position, 0, slot_name)
            self.equipment_table.setItem(row_position, 1, item_name)

    def show_context_menu(self, position):
        menu = QMenu()
        row = self.inventory_table.currentRow()
        if row >= 0:
            item_name = self.inventory_table.item(row, 0).text()
            item = self.game.inventory[item_name]
            discard_action = menu.addAction("Discard")
            discard_action.triggered.connect(lambda: self.discard_item(item_name))

            if isinstance(item, Food):
                eat_action = menu.addAction("Eat")
                eat_action.triggered.connect(lambda: self.eat_item(item_name))
            if isinstance(item, (Weapon, Armor, Accessory, Backpack, Mount, Carriage)):
                equip_action = menu.addAction("Equip")
                equip_action.triggered.connect(lambda: self.equip_item(item_name))

        menu.exec(self.inventory_table.viewport().mapToGlobal(position))

    def discard_item(self, item_name):
        self.game.discard_item(item_name)
        self.update_inventory()

    def eat_item(self, item_name):
        self.game.eat_item(item_name)
        self.update_inventory()
        self.update_labels()

    def equip_item(self, item_name):
        self.game.equip_item(item_name)
        self.update_inventory()
        self.update_equipment()

    def toggle_state(self):
        self.game.is_traveling = not self.game.is_traveling
        self.toggle_button.setText("Travel" if not self.game.is_traveling else "Rest")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    rpg = AdventureRPG()
    rpg.show()
    sys.exit(app.exec())
