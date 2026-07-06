"""10-row editable label table dock widget: name + colour, active row highlighted."""

from __future__ import annotations

from qtpy.QtCore import Qt
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

import napari

from ..labels import LabelModel

NAME_COL = 0
COLOR_COL = 1


class LabelTableWidget(QWidget):
    def __init__(self, label_model: LabelModel, labels_layer: "napari.layers.Labels"):
        super().__init__()
        self.label_model = label_model
        self.labels_layer = labels_layer

        self.table = QTableWidget(len(label_model.labels), 2, self)
        self.table.setHorizontalHeaderLabels(["Name", "Color"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        for row, label in enumerate(label_model.labels):
            name_item = QTableWidgetItem(label.name)
            self.table.setItem(row, NAME_COL, name_item)

            color_item = QTableWidgetItem()
            color_item.setFlags(color_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            color_item.setBackground(QColor(label.color))
            self.table.setItem(row, COLOR_COL, color_item)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

        self.table.currentCellChanged.connect(self._on_row_selected)
        self.table.itemChanged.connect(self._on_item_changed)
        label_model.active_changed.connect(self._highlight_row)

        self._highlight_row(label_model.active_row)

    def _on_row_selected(self, row: int, *_args) -> None:
        if row < 0:
            return
        self.label_model.set_active_row(row)
        self._apply_selected_label()

    def _on_item_changed(self, item: QTableWidgetItem) -> None:
        if item.column() != NAME_COL:
            return
        row = item.row()
        self.label_model.labels[row].name = item.text()

    def _highlight_row(self, row: int) -> None:
        self.table.blockSignals(True)
        self.table.selectRow(row)
        self.table.blockSignals(False)
        self._apply_selected_label()

    def _apply_selected_label(self) -> None:
        self.labels_layer.selected_label = self.label_model.active_label.index
