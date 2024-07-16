from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QMenu
from PyQt6.QtCore import Qt, QCoreApplication, pyqtSignal

class TeamTab(QWidget):
    character_selected = pyqtSignal(object)

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
        self.team_table.cellClicked.connect(self.on_cell_clicked)

        self.layout.addWidget(self.team_table)
        self.setLayout(self.layout)

        self.update_team_table()

    def update_team_table(self):
        # 保存当前选中单元格
        selected_items = self.team_table.selectedItems()
        selected_cell = None
        if selected_items:
            selected_cell = (self.team_table.row(selected_items[0]), self.team_table.column(selected_items[0]))

        self.team_table.setRowCount(0)

        # 插入玩家角色
        self.insert_character_to_table(self.game.character, 0)

        # 插入团队角色
        for i, companion in enumerate(self.game.team[1:], start=1):  # 排除玩家角色
            self.insert_character_to_table(companion, i)

        # 恢复之前的选中单元格
        if selected_cell:
            self.team_table.setCurrentCell(selected_cell[0], selected_cell[1])

    def insert_character_to_table(self, character, row):
        self.team_table.insertRow(row)
        name_item = QTableWidgetItem(character.name)
        name_item.setData(Qt.ItemDataRole.UserRole, character.id)
        name_item.setFlags(name_item.flags() ^ Qt.ItemFlag.ItemIsEditable)  # 不可编辑
        affinity_item = QTableWidgetItem(str(character.affinity))  # 假设每个角色有affinity属性
        affinity_item.setFlags(affinity_item.flags() ^ Qt.ItemFlag.ItemIsEditable)  # 不可编辑
        self.team_table.setItem(row, 0, name_item)
        self.team_table.setItem(row, 1, affinity_item)

    def on_cell_clicked(self, row, column):
        character_id = self.team_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        character = next((comp for comp in self.game.team if comp.id == character_id), None)
        if character:
            self.character_selected.emit(character)
