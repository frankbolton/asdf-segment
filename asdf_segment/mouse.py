"""Right-click deletes a segment: the contiguous region under the cursor is
filled with background, but only if its value matches the currently selected
label.

Two napari details drive the implementation:

- napari runs the active tool's mouse callback (``draw``) for *every* mouse
  button, so a right-click would also paint-stamp. ``draw`` refuses to run
  while ``layer.cursor == 'circle_frozen'`` (napari uses this during
  brush-resize), so we freeze the cursor for the duration of the right-click.
  Our callback sits at index 0 of ``mouse_drag_callbacks``; mode switches
  always re-append the tool callback to the end, so we always run first.
- ``layer.fill`` honours the layer's ``contiguous`` setting (on by default,
  giving connected-blob deletion), edits only the displayed slice, and records
  a single undo step, so Ctrl+Z restores the deleted segment.
"""

from __future__ import annotations

import napari

RIGHT_BUTTON = 2  # vispy button code (1 = left, 2 = right)


def _delete_segment_on_right_click(layer: napari.layers.Labels, event):
    if event.button != RIGHT_BUTTON:
        return

    background = layer.colormap.background_value
    value = layer.get_value(
        event.position,
        view_direction=event.view_direction,
        dims_displayed=event.dims_displayed,
        world=True,
    )

    previous_cursor = layer.cursor
    layer.cursor = "circle_frozen"  # blocks draw() for this click
    try:
        if value is not None and value == layer.selected_label and value != background:
            layer.fill(layer.world_to_data(event.position), background)
        yield
        while event.type == "mouse_move":
            yield
    finally:
        layer.cursor = previous_cursor


def bind_mouse(labels_layer: napari.layers.Labels) -> None:
    labels_layer.mouse_drag_callbacks.insert(0, _delete_segment_on_right_click)
