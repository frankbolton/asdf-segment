"""Filename selector + "Save segmentation" button."""

from __future__ import annotations

from qtpy.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import napari

from ..io import Volume, save_nifti


class SavePanelWidget(QWidget):
    def __init__(self, labels_layer: "napari.layers.Labels", volume: Volume):
        super().__init__()
        self.labels_layer = labels_layer
        self.volume = volume

        self.path_edit = QLineEdit("segmentation.nii.gz", self)
        browse_button = QPushButton("Browse…", self)
        browse_button.clicked.connect(self._browse)

        save_button = QPushButton("Save segmentation", self)
        save_button.clicked.connect(self._save)

        self.status_label = QLabel("", self)

        path_row = QHBoxLayout()
        path_row.addWidget(self.path_edit)
        path_row.addWidget(browse_button)

        layout = QVBoxLayout(self)
        layout.addLayout(path_row)
        layout.addWidget(save_button)
        layout.addWidget(self.status_label)

    def _browse(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Save segmentation", self.path_edit.text(), "NIFTI (*.nii *.nii.gz)"
        )
        if path:
            self.path_edit.setText(path)

    def _save(self) -> None:
        path = self.path_edit.text().strip()
        if not path:
            self.status_label.setText("Enter a filename first.")
            return
        save_nifti(path, self.labels_layer.data, self.volume)
        self.status_label.setText(f"Saved to {path}")
