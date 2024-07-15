from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView
from PyQt6.QtCore import Qt, QCoreApplication

class TeamTab(QWidget):
    def __init__(self, game):
        super().__init__()

        self.game = game

        self.layout = QVBoxLayout(self)
        self.team_table = QTableWidget(self)
        self.team_table.setColumnCount(2)
        self.team_table.setHorizontalHeaderLabels([
            QCoreApplication.translate("TeamTab", "Name"),
            QCoreApplication.translate("TeamTab", "Affinity")
        ])
        self.team_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.layout.addWidget(self.team_table)
        self.setLayout(self.layout)

        self.update_team_table()

    def update_team_table(self):
        self.team_table.setRowCount(0)

        # 插入玩家角色
        self.insert_character_to_table(self.game.character, 0)

        # 插入同伴角色
        for i, companion in enumerate(self.game.companions, start=1):
            self.insert_character_to_table(companion, i)

    def insert_character_to_table(self, character, row):
        self.team_table.insertRow(row)
        name_item = QTableWidgetItem(character.name)
        name_item.setFlags(name_item.flags() ^ Qt.ItemFlag.ItemIsEditable)  # 不可编辑
        affinity_item = QTableWidgetItem(str(character.affinity))  # 假设每个角色有affinity属性
        affinity_item.setFlags(affinity_item.flags() ^ Qt.ItemFlag.ItemIsEditable)  # 不可编辑
        self.team_table.setItem(row, 0, name_item)
        self.team_table.setItem(row, 1, affinity_item)
