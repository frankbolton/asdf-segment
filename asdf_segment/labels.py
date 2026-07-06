"""Label table model: 10 named, coloured labels driving the Labels layer."""

from __future__ import annotations

from dataclasses import dataclass

from psygnal import Signal

NUM_LABELS = 10

# Distinct, high-contrast default palette (napari-style), one per label 1-10.
DEFAULT_COLORS = [
    "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
    "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
]


@dataclass
class Label:
    index: int  # 1-10, the integer voxel value written into the Labels layer
    name: str
    color: str  # hex color for the overlay


class LabelModel:
    """Holds the 10 labels and which one is active."""

    active_changed = Signal(int)  # emits the new active row (0-based)

    def __init__(self) -> None:
        self.labels = [
            Label(index=i + 1, name=f"Label {i + 1}", color=DEFAULT_COLORS[i])
            for i in range(NUM_LABELS)
        ]
        self._active_row = 0

    @property
    def active_row(self) -> int:
        return self._active_row

    @property
    def active_label(self) -> Label:
        return self.labels[self._active_row]

    def set_active_row(self, row: int) -> None:
        row = max(0, min(NUM_LABELS - 1, row))
        if row != self._active_row:
            self._active_row = row
            self.active_changed.emit(row)

    def step_active(self, delta: int) -> None:
        self.set_active_row(self._active_row + delta)

    def color_map(self) -> dict[int | None, str]:
        """napari Labels colormap: voxel value -> hex color (0/unlabelled is transparent)."""
        color_map: dict[int | None, str] = {label.index: label.color for label in self.labels}
        color_map[None] = "#00000000"
        return color_map
