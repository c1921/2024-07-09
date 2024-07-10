from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QMenu, QAbstractItemView, QToolTip
)
from PyQt6.QtCore import Qt, QEvent
from items import Food

class InventoryTab(QWidget):
    def __init__(self, game, show_context_menu):
        super().__init__()

        self.game = game
        self.show_context_menu = show_context_menu

        self.inventory_table = QTableWidget(self)
        self.inventory_table.setColumnCount(4)  # 减少两列
        self.inventory_table.setHorizontalHeaderLabels(["Item", "Quantity", "Weight", "Value"])
        self.inventory_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.inventory_table.customContextMenuRequested.connect(self.show_context_menu)
        self.inventory_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.inventory_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.inventory_table.setMouseTracking(True)  # 启用鼠标跟踪
        self.inventory_table.viewport().installEventFilter(self)  # 安装事件过滤器

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
            total_item_weight = item.weight * item.quantity
            total_item_value = item.value * item.quantity
            self.inventory_table.setItem(row_position, 2, QTableWidgetItem(f"{total_item_weight:.2f}"))  # 更新为Weight
            self.inventory_table.setItem(row_position, 3, QTableWidgetItem(f"{total_item_value:.2f}"))  # 更新为Value
            total_weight += total_item_weight
            total_value += total_item_value
        self.update_weight_label(total_weight)
        self.update_value_label(total_value)

    def update_weight_label(self, current_weight=0):
        self.weight_label.setText(f"Weight: {current_weight:.2f} / {self.max_weight}")  # 格式化当前负重

    def update_value_label(self, total_value=0):
        self.weight_label.setText(self.weight_label.text() + f", Total Value: {total_value:.2f}")  # 格式化总价值

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.ToolTip and source is self.inventory_table.viewport():
            index = self.inventory_table.indexAt(event.pos())
            if index.isValid():
                item_name = self.inventory_table.item(index.row(), 0).text()
                item = self.game.inventory[item_name]
                if isinstance(item, Food):
                    tooltip_text = (
                        f"Name: {item.name}\n"
                        f"Weight: {item.weight}\n"
                        f"Value: {item.value}\n"
                        f"Hunger Restore: {item.hunger_restore}\n"
                        f"Thirst Restore: {item.thirst_restore}"
                    )
                    QToolTip.showText(event.globalPos(), tooltip_text)
                else:
                    QToolTip.hideText()
                return True
        return super().eventFilter(source, event)
