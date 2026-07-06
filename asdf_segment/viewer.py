"""napari viewer setup: Image + Labels layers, fixed-axis slicing."""

from __future__ import annotations

import napari
import numpy as np
from napari.utils.colormaps.colormap_utils import direct_colormap

from .io import Volume
from .labels import LabelModel


def build_viewer(volume: Volume, label_model: LabelModel) -> napari.Viewer:
    viewer = napari.Viewer(title="asdf-segment")

    viewer.add_image(volume.data, name="image")

    label_data = np.zeros(volume.data.shape, dtype=np.uint8)
    labels_layer = viewer.add_labels(
        label_data,
        name="segmentation",
        colormap=direct_colormap(label_model.color_map()),
    )
    labels_layer.selected_label = label_model.active_label.index
    labels_layer.brush_size = 10

    # Fix slicing to the last axis: put it first in dims.order so the other
    # two axes are the displayed 2D plane and this one drives the slider.
    last_axis = volume.data.ndim - 1
    order = (last_axis, *(a for a in range(volume.data.ndim) if a != last_axis))
    viewer.dims.order = order

    return viewer
