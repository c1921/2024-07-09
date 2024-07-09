import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton,
    QProgressBar, QMenu, QTabWidget
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

        # 创建标签页
        self.tabs = QTabWidget()
        self.travel_tab = QWidget()
        self.items_equipment_tab = QWidget()
        self.character_tab = QWidget()
        self.tabs.addTab(self.travel_tab, "旅行")
        self.tabs.addTab(self.items_equipment_tab, "物品与装备")
        self.tabs.addTab(self.character_tab, "人物")

        # 旅行标签页
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

        travel_layout = QVBoxLayout()
        travel_layout.addWidget(self.time_label)
        travel_layout.addWidget(self.distance_label)
        travel_layout.addWidget(self.hunger_bar)
        travel_layout.addWidget(self.thirst_bar)
        travel_layout.addWidget(self.fatigue_bar)
        travel_layout.addWidget(self.mood_bar)
        travel_layout.addWidget(self.toggle_button)
        self.travel_tab.setLayout(travel_layout)

        # 物品与装备标签页
        self.inventory_table = QTableWidget(self)
        self.inventory_table.setColumnCount(2)
        self.inventory_table.setHorizontalHeaderLabels(["Item", "Quantity"])
        self.inventory_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.inventory_table.customContextMenuRequested.connect(self.show_context_menu)
        self.inventory_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.update_inventory()

        self.equipment_table = QTableWidget(self)
        self.equipment_table.setColumnCount(2)
        self.equipment_table.setHorizontalHeaderLabels(["Slot", "Item"])
        self.equipment_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.update_equipment()

        items_equipment_layout = QHBoxLayout()
        items_equipment_layout.addWidget(self.inventory_table)
        items_equipment_layout.addWidget(self.equipment_table)
        self.items_equipment_tab.setLayout(items_equipment_layout)

        # 人物标签页
        self.strength_label = QLabel(f"Strength: {self.game.strength}")
        self.agility_label = QLabel(f"Agility: {self.game.agility}")
        self.charisma_label = QLabel(f"Charisma: {self.game.charisma}")
        self.intelligence_label = QLabel(f"Intelligence: {self.game.intelligence}")
        self.attack_label = QLabel(f"Attack: {self.game.attack}")
        self.armor_label = QLabel(f"Armor: {self.game.armor}")

        character_layout = QVBoxLayout()
        character_layout.addWidget(self.strength_label)
        character_layout.addWidget(self.agility_label)
        character_layout.addWidget(self.charisma_label)
        character_layout.addWidget(self.intelligence_label)
        character_layout.addWidget(self.attack_label)
        character_layout.addWidget(self.armor_label)
        self.character_tab.setLayout(character_layout)

        # 设置主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)

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

        self.strength_label.setText(f"Strength: {self.game.strength}")
        self.agility_label.setText(f"Agility: {self.game.agility}")
        self.charisma_label.setText(f"Charisma: {self.game.charisma}")
        self.intelligence_label.setText(f"Intelligence: {self.game.intelligence}")
        self.attack_label.setText(f"Attack: {self.game.attack}")
        self.armor_label.setText(f"Armor: {self.game.armor}")

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
        self.update_labels()

    def toggle_state(self):
        self.game.is_traveling = not self.game.is_traveling
        self.toggle_button.setText("Travel" if not self.game.is_traveling else "Rest")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    rpg = AdventureRPG()
    rpg.show()
    sys.exit(app.exec())
