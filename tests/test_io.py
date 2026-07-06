import numpy as np

from asdf_segment.io import load_nifti, save_nifti


def test_save_load_round_trip(tmp_path):
    import nibabel as nib

    data = np.zeros((8, 8, 4), dtype=np.int16)
    data[2:5, 2:5, :] = 50
    affine = np.eye(4)
    affine[:3, :3] *= [2.0, 2.0, 3.0]
    src_path = tmp_path / "source.nii.gz"
    nib.save(nib.Nifti1Image(data, affine), str(src_path))

    volume = load_nifti(src_path)
    assert volume.data.shape == data.shape
    assert np.allclose(volume.affine, affine)

    label_data = np.zeros(data.shape, dtype=np.uint8)
    label_data[3, 3, 2] = 5
    out_path = tmp_path / "segmentation.nii.gz"
    save_nifti(out_path, label_data, volume)

    saved = nib.load(str(out_path))
    assert np.allclose(saved.affine, affine)
    assert np.asarray(saved.dataobj)[3, 3, 2] == 5
