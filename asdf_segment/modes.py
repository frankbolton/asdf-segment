"""Vim-style input modes: COMMAND (our hotkeys) vs NAPARI (native shortcuts)."""

from __future__ import annotations

from enum import Enum

from psygnal import Signal


class Mode(Enum):
    COMMAND = "command"  # A/S slice, D/F label, 1-0 pick label — shadows napari keys
    NAPARI = "napari"  # native napari shortcuts (E/P/F tools, 1-7 modes, [/] brush)


class ModeModel:
    changed = Signal(Mode)

    def __init__(self, mode: Mode = Mode.COMMAND) -> None:
        self._mode = mode

    @property
    def mode(self) -> Mode:
        return self._mode

    def set_mode(self, mode: Mode) -> None:
        if mode != self._mode:
            self._mode = mode
            self.changed.emit(mode)

    def toggle(self) -> None:
        self.set_mode(Mode.NAPARI if self._mode is Mode.COMMAND else Mode.COMMAND)
