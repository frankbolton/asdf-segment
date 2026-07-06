"""Entrypoint: build viewer, wire widgets + key bindings, run."""

from __future__ import annotations

import argparse

import napari

from .io import load_nifti
from .keybindings import bind_keys
from .labels import LabelModel
from .viewer import build_viewer
from .widgets.label_table import LabelTableWidget
from .widgets.save_panel import SavePanelWidget


def main() -> None:
    parser = argparse.ArgumentParser(prog="asdf-segment")
    parser.add_argument("path", help="Path to a NIFTI volume (.nii or .nii.gz)")
    args = parser.parse_args()

    volume = load_nifti(args.path)
    label_model = LabelModel()
    viewer = build_viewer(volume, label_model)
    labels_layer = viewer.layers["segmentation"]

    bind_keys(viewer, labels_layer, label_model)

    viewer.window.add_dock_widget(
        LabelTableWidget(label_model, labels_layer), name="Labels", area="right"
    )
    viewer.window.add_dock_widget(
        SavePanelWidget(labels_layer, volume), name="Save", area="right"
    )

    napari.run()


if __name__ == "__main__":
    main()
