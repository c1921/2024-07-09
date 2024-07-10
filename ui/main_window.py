from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QMenu
from PyQt6.QtCore import QTimer
from ui.travel_tab import TravelTab
from ui.inventory_tab import InventoryTab
import config
from items import Food

class MainWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()

        self.game = game

        self.setWindowTitle("Adventure RPG")
        self.setGeometry(100, 100, 600, 400)

        self.tabs = QTabWidget(self)
        self.travel_tab = TravelTab(self.game, self.toggle_state)
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
        self.timer.start(config.TIMER_INTERVAL)

        self.update_labels()

    def update_time_and_distance(self):
        self.game.game_time = self.game.game_time.addSecs(60)
        if self.game.game_time.hour() == 0 and self.game.game_time.minute() == 0:
            self.game.day_count += 1

        self.game.update_time_and_distance()
        self.update_labels()
        self.update_inventory()
        self.update_log()

    def update_labels(self):
        self.travel_tab.update_labels()

    def update_inventory(self):
        self.inventory_tab.update_inventory()

    def update_log(self):
        self.travel_tab.update_log()

    def toggle_state(self):
        self.game.is_traveling = not self.game.is_traveling
        self.travel_tab.toggle_button.setText("Travel" if not self.game.is_traveling else "Rest")

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
