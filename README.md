# asdf-segment

A lightweight tool for manually segmenting NIFTI images by painting labelled regions
with a circular brush. Built on **[napari](https://napari.org)** for the GUI and
**nibabel** for I/O.

> Status: **planning**. This README is the design/spec.

## Why napari

napari is a scientific n-dimensional image viewer (Qt + GPU-accelerated vispy). Its
built-in `Labels` layer already provides most of this tool's spec, so we mainly
*configure* napari and add a couple of small widgets rather than building a canvas from
scratch:

| Requirement | napari provides |
| --- | --- |
| Circular brush + adjustable radius | `Labels` paint mode with a **brush size** slider |
| Erase | Eraser mode / right-click-drag erases |
| Undo | **Ctrl+Z** undo (and Ctrl+Shift+Z redo) built in |
| Slice scrolling | Native dims slider + scroll wheel over the canvas |
| Label as integer voxel value | `selected_label` is the integer written into the layer |
| Overlay colours | Per-label colour map on the `Labels` layer |

What we add on top: nibabel load/save with affine preservation, a **10-row editable
label table** (name + colour + active selection), and custom **A/S/D/F** key bindings.

## Decisions

- **Slicing:** single fixed axis (default: the last/z axis). Scroll through this one axis.
- **Brush:** *click to stamp* — a single click paints one filled circle of the current
  brush radius. (napari also supports drag; we tune brush behaviour to match.)
- **Editing:** eraser mode (paints 0 / unlabelled, also via right-click) and Ctrl+Z undo.
- **Labels:** a 10-row table, **editable in-app** — names editable, colours from a palette
  (overridable), active row highlighted.

## Goals

- Load a 3D NIFTI volume (`.nii` / `.nii.gz`) with nibabel.
- Scroll through slices along one axis.
- Paint segmentation labels with a circular brush of adjustable radius.
- Assign each stamp one of 10 named labels.
- Save the segmentation back out as a NIFTI label map (integer voxels), preserving the
  source affine/header, with a chosen output filename.

## Core interactions

| Action | Control |
| --- | --- |
| Change slice | Dims slider · scroll wheel over image · hotkeys **A** / **S** |
| Brush radius | Brush-size slider (napari Labels controls) |
| Active label | Click a row in the 10-label table · hotkeys **D** / **F** (down / up the list) |
| Paint | Left-click on the image to stamp a filled circle |
| Erase | Eraser mode, or **right-click** |
| Undo | **Ctrl+Z** |
| Save | "Save segmentation" button + filename selector |

### Label table

A 10-row table (a napari dock widget). Each row has:
- an index (1–10, the integer written into the label volume),
- a user-editable name,
- a colour (for the overlay).

The active label is highlighted and drives `Labels.selected_label`. Clicking a row
selects it; **D**/**F** move the selection down/up the list.

## Architecture

```
asdf_segment/
  __main__.py       # Entrypoint: build viewer, wire widgets + key bindings, run
  viewer.py         # napari viewer setup: image + Labels layers, dims/axis config
  io.py             # nibabel load/save, affine + header preservation
  labels.py         # Label table model (index, name, colour) + colour map
  keybindings.py    # A/S/D/F custom bindings on the viewer
  widgets/
    label_table.py  # 10-row editable label table dock widget (magicgui/Qt)
    save_panel.py   # filename selector + "Save segmentation" button
pyproject.toml      # uv-managed, deps + `asdf-segment` entrypoint
tests/
```

### Technical notes

- Volume loaded via nibabel → numpy; added as an `Image` layer. A parallel `uint8`
  `Labels` layer (same shape) holds the segmentation, initialised to zeros.
- The `Labels` layer's `color` / `selected_label` are driven from the label table; the
  brush size slider maps to "radius".
- Custom **A/S/D/F** via `viewer.bind_key` (A/S step the current dims axis; D/F change the
  active label row). Scroll, radius, erase, and undo come from napari itself.
- On Save, the `Labels` data + the source affine/header go back through nibabel to the
  chosen filename. Kept in memory until then.

## Tooling

- Managed with **uv** and `pyproject.toml`.
- `uv sync` to install, `uv run asdf-segment <path-to.nii.gz>` to launch (napari opens a
  desktop window; needs a display / Qt backend).

## Roadmap

1. Project scaffold: `pyproject.toml`, package layout, `uv sync` (napari + nibabel).
2. NIFTI load/save + show Image + empty Labels layer on the fixed axis.
3. 10-row editable label table widget driving `selected_label` + colours.
4. A/S/D/F key bindings; confirm brush radius / erase / undo / scroll behave.
5. Save panel: filename selector + write-out with affine preserved.
6. Polish: default label palette, brush tuning, tests.
```
