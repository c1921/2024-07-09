from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QMenu
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from ui.travel_tab import TravelTab
from ui.inventory_tab import InventoryTab
from shortcuts import Shortcuts
import config
from items import Food

class MainWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()

        self.game = game
        self.timer_speed = config.TIMER_INTERVAL  # 初始时间间隔
        self.is_paused = False

        self.setWindowTitle("Adventure RPG")
        self.setGeometry(100, 100, 600, 400)

        self.tabs = QTabWidget(self)
        self.travel_tab = TravelTab(self.game, self.toggle_state, self.change_speed, self.toggle_pause)
        self.inventory_tab = InventoryTab(self.game, self.show_context_menu)
        self.tabs.addTab(self.travel_tab, "Travel")
        self.tabs.addTab(self.inventory_tab, "Inventory")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_and_distance)
        self.timer.start(self.timer_speed)

        self.update_labels()

        self.setup_shortcuts()

    def setup_shortcuts(self):
        QShortcut(Shortcuts.PAUSE_CONTINUE, self).activated.connect(self.toggle_pause)
        QShortcut(Shortcuts.SPEED_1X, self).activated.connect(lambda: self.change_speed(0, update_combo=True))
        QShortcut(Shortcuts.SPEED_2X, self).activated.connect(lambda: self.change_speed(1, update_combo=True))
        QShortcut(Shortcuts.SPEED_5X, self).activated.connect(lambda: self.change_speed(2, update_combo=True))
        QShortcut(Shortcuts.SPEED_10X, self).activated.connect(lambda: self.change_speed(3, update_combo=True))
        QShortcut(Shortcuts.SWITCH_TAB, self).activated.connect(self.switch_tab)

    def switch_tab(self):
        current_index = self.tabs.currentIndex()
        new_index = (current_index + 1) % self.tabs.count()
        self.tabs.setCurrentIndex(new_index)

    def update_time_and_distance(self):
        if not self.is_paused:
            self.game.game_time = self.game.game_time.addSecs(60)
            if self.game.game_time.hour() == 0 and self.game.game_time.minute() == 0:
                self.game.day_count += 1

            self.game.update_time_and_distance()
            self.update_labels()
            self.update_inventory()
            self.update_log()

            # 更新同路人
            for companion in self.game.companions:
                self.travel_tab.update_companions(companion)
            self.game.companions = []  # 清空已处理的同路人列表

    def update_labels(self):
        self.travel_tab.update_labels()

    def update_inventory(self):
        self.inventory_tab.update_inventory()

    def update_log(self):
        self.travel_tab.update_log()

    def toggle_state(self):
        self.game.is_traveling = not self.game.is_traveling
        self.travel_tab.toggle_button.setText("Travel" if not self.game.is_traveling else "Rest")

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.travel_tab.pause_button.setText("Resume" if self.is_paused else "Pause")

    def change_speed(self, index, update_combo=False):
        speeds = [config.TIMER_INTERVAL, config.TIMER_INTERVAL // 2, config.TIMER_INTERVAL // 5, config.TIMER_INTERVAL // 10]
        self.timer_speed = speeds[index]
        self.timer.start(self.timer_speed)
        if update_combo:
            self.travel_tab.speed_combo.setCurrentIndex(index)

    def show_context_menu(self, position):
        menu = QMenu()
        row = self.inventory_tab.inventory_table.currentRow()  # 引用inventory_tab中的inventory_table
        if row >= 0:
            item_name = self.inventory_tab.inventory_table.item(row, 0).text()  # 引用inventory_tab中的inventory_table
            item = self.game.inventory[item_name]

            if isinstance(item, Food):
                eat_action = menu.addAction("Eat")
                eat_action.triggered.connect(lambda: self.eat_item(item_name))

            discard_action = menu.addAction("Discard")
            discard_action.triggered.connect(lambda: self.discard_item(item_name))

        menu.exec(self.inventory_tab.inventory_table.viewport().mapToGlobal(position))  # 引用inventory_tab中的inventory_table

    def discard_item(self, item_name):
        self.game.discard_item(item_name)
        self.update_inventory()
        self.update_log()

    def eat_item(self, item_name):
        self.game.eat_item(item_name)
        self.update_inventory()
        self.update_labels()
        self.update_log()
