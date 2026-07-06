"""nibabel load/save, preserving affine + header."""

from __future__ import annotations

from pathlib import Path

import nibabel as nib
import numpy as np


class Volume:
    """A loaded NIFTI volume plus the metadata needed to save it back out."""

    def __init__(self, data: np.ndarray, affine: np.ndarray, header: nib.Nifti1Header):
        self.data = data
        self.affine = affine
        self.header = header


def load_nifti(path: str | Path) -> Volume:
    img = nib.load(str(path))
    data = np.asarray(img.dataobj)
    return Volume(data=data, affine=img.affine, header=img.header)


def save_nifti(path: str | Path, label_data: np.ndarray, volume: Volume) -> None:
    """Write `label_data` out as a NIFTI label map, reusing the source affine/header."""
    img = nib.Nifti1Image(
        label_data.astype(np.uint8), affine=volume.affine, header=volume.header
    )
    nib.save(img, str(path))
