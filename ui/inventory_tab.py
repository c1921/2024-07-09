from PyQt6.QtWidgets import (
    QLabel, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QAbstractItemView
)
from PyQt6.QtCore import Qt

class InventoryTab(QWidget):
    def __init__(self, game, show_context_menu):
        super().__init__()

        self.game = game
        self.show_context_menu = show_context_menu

        self.inventory_table = QTableWidget(self)
        self.inventory_table.setColumnCount(6)  # 增加两列
        self.inventory_table.setHorizontalHeaderLabels(["Item", "Quantity", "Weight", "Total Weight", "Value", "Total Value"])
        self.inventory_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.inventory_table.customContextMenuRequested.connect(self.show_context_menu)
        self.inventory_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.inventory_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.weight_label = QLabel(self)
        self.max_weight = 100  # 设置负重上限
        self.update_weight_label()

        inventory_layout = QVBoxLayout()
        inventory_layout.addWidget(self.inventory_table)
        inventory_layout.addWidget(self.weight_label)

        self.setLayout(inventory_layout)

    def update_inventory(self):
        self.inventory_table.setRowCount(0)
        total_weight = 0
        total_value = 0
        for item in self.game.inventory.values():
            row_position = self.inventory_table.rowCount()
            self.inventory_table.insertRow(row_position)
            self.inventory_table.setItem(row_position, 0, QTableWidgetItem(item.name))
            self.inventory_table.setItem(row_position, 1, QTableWidgetItem(str(item.quantity)))
            self.inventory_table.setItem(row_position, 2, QTableWidgetItem(str(item.weight)))
            total_item_weight = item.weight * item.quantity
            total_item_value = item.value * item.quantity
            self.inventory_table.setItem(row_position, 3, QTableWidgetItem(str(total_item_weight)))
            self.inventory_table.setItem(row_position, 4, QTableWidgetItem(str(item.value)))
            self.inventory_table.setItem(row_position, 5, QTableWidgetItem(str(total_item_value)))
            total_weight += total_item_weight
            total_value += total_item_value
        self.update_weight_label(total_weight)
        self.update_value_label(total_value)

    def update_weight_label(self, current_weight=0):
        self.weight_label.setText(f"Weight: {current_weight} / {self.max_weight}")

    def update_value_label(self, total_value=0):
        self.weight_label.setText(self.weight_label.text() + f", Total Value: {total_value}")
