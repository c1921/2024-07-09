from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTabWidget, QMenu, QSplitter
from PyQt6.QtCore import QTimer, Qt, QCoreApplication
from PyQt6.QtGui import QKeySequence, QShortcut
from core.save_manager import SaveManager
from ui.travel_tab import TravelTab
from ui.inventory_tab import InventoryTab
from ui.character_details import CharacterDetails
from ui.team_tab import TeamTab
from core.shortcuts import Shortcuts
import config.config as config
from items.items import Food

class MainWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()

        self.game = game
        self.timer_speed = config.TIMER_INTERVAL
        self.is_paused = False
        self.save_manager = SaveManager(self.game)

        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Drifting"))
        self.setGeometry(100, 100, 800, 600)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        self.tabs = QTabWidget(self)
        self.travel_tab = TravelTab(self.game, self.toggle_state, self.change_speed, self.toggle_pause, self.show_character_details, self.invite_to_team)
        self.inventory_tab = InventoryTab(self.game, self.show_context_menu)
        self.team_tab = TeamTab(self.game)
        self.tabs.addTab(self.travel_tab, QCoreApplication.translate("MainWindow", "Travel"))
        self.tabs.addTab(self.inventory_tab, QCoreApplication.translate("MainWindow", "Inventory"))
        self.tabs.addTab(self.team_tab, QCoreApplication.translate("MainWindow", "Team"))

        self.character_details = CharacterDetails()

        self.splitter.addWidget(self.tabs)
        self.splitter.addWidget(self.character_details)
        self.splitter.setSizes([500, 300])

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.splitter)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time_and_distance)
        self.timer.start(self.timer_speed)

        self.save_timer = QTimer(self)
        self.save_timer.timeout.connect(self.save_manager.save_game)
        self.save_timer.start(120000)

        self.update_labels()
        self.setup_shortcuts()
        self.save_manager.load_game()

        self.team_tab.character_selected.connect(self.show_character_details)

    def closeEvent(self, event):
        self.save_manager.save_game()
        event.accept()

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
            self.travel_tab.update_companions()

    def update_labels(self):
        self.travel_tab.update_labels()
        self.team_tab.update_team_table()

    def update_inventory(self):
        self.inventory_tab.update_inventory()

    def update_log(self):
        self.travel_tab.update_log()

    def toggle_state(self):
        self.game.is_traveling = not self.game.is_traveling
        self.travel_tab.toggle_button.setText(QCoreApplication.translate("MainWindow", "Travel") if not self.game.is_traveling else QCoreApplication.translate("MainWindow", "Rest"))

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.travel_tab.pause_button.setText(QCoreApplication.translate("MainWindow", "Resume") if self.is_paused else QCoreApplication.translate("MainWindow", "Pause"))

    def change_speed(self, index, update_combo=False):
        speeds = [config.TIMER_INTERVAL, config.TIMER_INTERVAL // 2, config.TIMER_INTERVAL // 5, config.TIMER_INTERVAL // 10]
        self.timer_speed = speeds[index]
        self.timer.start(self.timer_speed)
        if update_combo:
            self.travel_tab.speed_combo.setCurrentIndex(index)

    def show_context_menu(self, position):
        menu = QMenu()
        row = self.inventory_tab.inventory_table.currentRow()
        if row >= 0:
            item_name = self.inventory_tab.inventory_table.item(row, 0).text()
            item = self.game.inventory[item_name]

            if isinstance(item, Food):
                eat_action = menu.addAction(QCoreApplication.translate("MainWindow", "Eat"))
                eat_action.triggered.connect(lambda: self.eat_item(item_name))

            discard_action = menu.addAction(QCoreApplication.translate("MainWindow", "Discard"))
            discard_action.triggered.connect(lambda: self.discard_item(item_name))

        menu.exec(self.inventory_tab.inventory_table.viewport().mapToGlobal(position))

    def discard_item(self, item_name):
        self.game.discard_item(item_name)
        self.update_inventory()
        self.update_log()

    def eat_item(self, item_name):
        self.game.eat_item(item_name)
        self.update_inventory()
        self.update_labels()
        self.update_log()

    def show_character_details(self, character):
        self.character_details.update_details(character)

    def invite_to_team(self, companion):
        if companion.affinity >= 60:
            self.game.companions.remove(companion)
            self.game.team.append(companion)
            self.travel_tab.update_companions()
            self.team_tab.update_team_table()
            self.travel_tab.log_text.append(QCoreApplication.translate("MainWindow", "You invited {name} to your team.").format(name=companion.name))
        else:
            self.travel_tab.log_text.append(QCoreApplication.translate("MainWindow", "{name} refused to join your team.").format(name=companion.name))
