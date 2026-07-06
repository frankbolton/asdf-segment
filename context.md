# Context / handoff — asdf-segment

Pick this up in an environment **with a working GUI display** (napari is a desktop Qt app).
This file captures everything decided so far so you can restart cleanly.

## What this is

A tool for manually segmenting 3D NIFTI images by painting labelled regions with a
circular brush. Full design/spec lives in `README.md`. This file is the working-state
summary + next actions.

## Stack (decided)

- **GUI: napari** (Qt + vispy). Chosen over Streamlit — Streamlit can't do mouse-paint /
  right-click / scroll / hotkeys well. napari gives brush+radius, erase, Ctrl+Z undo,
  and slice-scrolling for free.
- **I/O: nibabel** (load/save `.nii`/`.nii.gz`, preserve affine/header).
- **Env: uv + pyproject.toml.** Python 3.14 available locally; `uv` 0.11.21.

## Design decisions (already confirmed with user)

- **Slicing:** single fixed axis (default last/z). No plane switching.
- **Brush:** click-to-stamp — single click paints one filled circle of the current radius.
- **Editing:** eraser mode (also **right-click**) + **Ctrl+Z** undo.
- **Labels:** 10-row table, **editable in-app** — editable names, palette colours
  (overridable), active row highlighted.
- **Save:** button + **filename selector** for the output path.

## Interaction map

| Action | Control |
| --- | --- |
| Change slice | dims slider · scroll wheel · **A** / **S** |
| Brush radius | napari brush-size slider |
| Active label | click table row · **D** / **F** (down/up list) |
| Paint | left-click (stamp filled circle) |
| Erase | eraser mode / right-click |
| Undo | Ctrl+Z |
| Save | button + filename selector |

## What napari gives vs. what we build

- **Free from napari:** `Labels` layer brush + brush-size (radius), eraser, Ctrl+Z undo,
  scroll-through-slices, per-label colours, `selected_label` = integer voxel value.
- **We build:** nibabel load/save w/ affine preservation; 10-row editable label-table
  dock widget; A/S/D/F key bindings (`viewer.bind_key`); save panel w/ filename selector.

## Planned layout (see README for detail)

```
asdf_segment/
  __main__.py    viewer.py    io.py    labels.py    keybindings.py
  widgets/ label_table.py  save_panel.py
pyproject.toml   tests/
```

## Status: scaffold built and verified (2026-07-03)

Steps 1-6 below are done, running natively on Windows (not WSL2 — see environment note).
`asdf_segment/` package is implemented per the README architecture: `io.py`, `labels.py`,
`viewer.py`, `keybindings.py`, `widgets/label_table.py`, `widgets/save_panel.py`,
`__main__.py`. Entrypoint `asdf-segment <path>` works (`uv run asdf-segment --help`).

Verified end-to-end (not just imports): loaded a synthetic NIFTI, built the viewer,
exercised A/S slice-stepping and D/F label-switching logic, edited a label name through
the table widget, painted a label stamp on the `Labels` layer, and saved it back out —
confirmed the round-tripped file preserves the affine and the painted voxel count.
Screenshots confirm the napari window, layer list, 10-row label table (with per-row
colour swatches and highlight-follows-selection), and save panel all render correctly.

Note: napari resolves keys against the **active layer before the viewer**, and the
Labels layer class binds F to fill mode (plus E/P/L/Z/M/X/B/1-7) — so `viewer.bind_key`
alone gets shadowed while painting. `bind_keys()` now binds A/S/D/F on both the viewer
and the Labels layer instance (instance keymap beats class defaults); fill mode is
still on `4`/toolbar. Verified via simulated presses through the `KeymapHandler`
(2026-07-06).

Note: napari 0.7.1's `add_labels()` has no `color=` kwarg anymore — use
`napari.utils.colormaps.colormap_utils.direct_colormap(color_map_dict)` and pass it as
`colormap=`. `viewer.py` already does this.

`tests/test_io.py` and `tests/test_labels.py` cover the headless-safe modules (no Qt
needed) — `uv run pytest` passes. Widget/viewer code isn't unit-tested (would need
pytest-qt); it was instead verified manually via the screenshot-based e2e check above.

## Next actions

1. ~~Scaffold~~ — done.
2. ~~Display smoke-test~~ — done, confirmed on native Windows.
3. ~~Load NIFTI → show Image + empty Labels layer on fixed axis~~ — done.
4. ~~10-row editable label table driving `selected_label` + colours~~ — done.
5. ~~A/S/D/F key bindings~~ — logic verified; **not yet verified via real simulated
   keypresses through Qt** (tested by calling the bound functions directly instead —
   see e2e note above). Worth a manual click-through pass.
6. ~~Save panel~~ — done, round-trip verified.
7. **Remaining polish:** brush-tuning pass (currently just `brush_size = 10`, not
   user-configurable beyond napari's own slider), a real manual click-through session
   with an actual NIFTI file, and deciding whether pytest-qt is worth adding for
   widget-level tests.

## Environment caveat

- This session ran **natively on Windows**, not WSL2 — napari's window opened and
  rendered correctly with no WSLg/X-server setup needed. If a future session is back in
  WSL2, re-check the display situation described in the original version of this file
  (napari needs WSLg or an X server there).
```
