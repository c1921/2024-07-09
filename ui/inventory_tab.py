from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QMenu, QAbstractItemView, QToolTip
)
from PyQt6.QtCore import Qt, QEvent, QCoreApplication
from items.items import Food

class InventoryTab(QWidget):
    def __init__(self, game, show_context_menu):
        super().__init__()

        self.game = game
        self.show_context_menu = show_context_menu

        self.inventory_table = QTableWidget(self)
        self.inventory_table.setColumnCount(4)
        self.inventory_table.setHorizontalHeaderLabels([
            QCoreApplication.translate("InventoryTab", "Item"),
            QCoreApplication.translate("InventoryTab", "Quantity"),
            QCoreApplication.translate("InventoryTab", "Weight"),
            QCoreApplication.translate("InventoryTab", "Value")
        ])
        self.inventory_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.inventory_table.customContextMenuRequested.connect(self.show_context_menu)
        self.inventory_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.inventory_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.inventory_table.setMouseTracking(True)
        self.inventory_table.viewport().installEventFilter(self)

        self.weight_label = QLabel(self)
        self.max_weight = 100
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
            self.inventory_table.setItem(row_position, 2, QTableWidgetItem(f"{total_item_weight:.2f}"))
            self.inventory_table.setItem(row_position, 3, QTableWidgetItem(f"{total_item_value:.2f}"))
            total_weight += total_item_weight
            total_value += total_item_value
        self.update_weight_label(total_weight)
        self.update_value_label(total_value)

    def update_weight_label(self, current_weight=0):
        self.weight_label.setText(
            QCoreApplication.translate("InventoryTab", "Weight: ") + 
            f"{current_weight:.2f} / {self.max_weight}"
        )

    def update_value_label(self, total_value=0):
        self.weight_label.setText(
            self.weight_label.text() +
            QCoreApplication.translate("InventoryTab", ", Total Value: ") +
            f"{total_value:.2f}"
        )

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.ToolTip and source is self.inventory_table.viewport():
            index = self.inventory_table.indexAt(event.pos())
            if index.isValid():
                item_name = self.inventory_table.item(index.row(), 0).text()
                item = self.game.inventory[item_name]
                if isinstance(item, Food):
                    tooltip_name = QCoreApplication.translate("InventoryTab", "Name: ") + "{name}"
                    tooltip_weight = QCoreApplication.translate("InventoryTab", "Weight: ") + "{weight}"
                    tooltip_value = QCoreApplication.translate("InventoryTab", "Value: ") + "{value}"
                    tooltip_hunger_restore = QCoreApplication.translate("InventoryTab", "Hunger Restore: ") + "{hunger_restore}"
                    tooltip_thirst_restore = QCoreApplication.translate("InventoryTab", "Thirst Restore: ") + "{thirst_restore}"

                    tooltip_text = (
                        f"{tooltip_name}\n{tooltip_weight}\n{tooltip_value}\n{tooltip_hunger_restore}\n{tooltip_thirst_restore}"
                    ).format(
                        name=item.name,
                        weight=item.weight,
                        value=item.value,
                        hunger_restore=item.hunger_restore,
                        thirst_restore=item.thirst_restore
                    )
                    QToolTip.showText(event.globalPos(), tooltip_text)
                else:
                    QToolTip.hideText()
                return True
        return super().eventFilter(source, event)
