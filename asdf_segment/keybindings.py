"""Custom A/S/D/F key bindings: A/S step the slice axis, D/F change the active label.

napari resolves keys against the active layer before the viewer, and the Labels
layer class claims several letters for itself (notably F = fill mode), so binding
on the viewer alone is not enough — the layer would shadow us whenever it is
active, which is always while painting. We therefore bind on the Labels layer
instance too: its keymap takes precedence over the layer-class defaults. Fill
mode stays reachable via the "4" key and the toolbar button.
"""

from __future__ import annotations

import napari

from .labels import LabelModel


def _step_slice(viewer: napari.Viewer, delta: int) -> None:
    axis = viewer.dims.order[0]
    nsteps = viewer.dims.nsteps[axis]
    current = viewer.dims.current_step[axis]
    new = max(0, min(nsteps - 1, current + delta))
    viewer.dims.set_current_step(axis, new)


def bind_keys(
    viewer: napari.Viewer,
    labels_layer: napari.layers.Labels,
    label_model: LabelModel,
) -> None:
    def _prev_slice(_provider) -> None:
        _step_slice(viewer, -1)

    def _next_slice(_provider) -> None:
        _step_slice(viewer, 1)

    def _prev_label(_provider) -> None:
        label_model.step_active(-1)

    def _next_label(_provider) -> None:
        label_model.step_active(1)

    actions = {"a": _prev_slice, "s": _next_slice, "d": _prev_label, "f": _next_label}
    for provider in (viewer, labels_layer):
        for key, action in actions.items():
            provider.bind_key(key, action, overwrite=True)
