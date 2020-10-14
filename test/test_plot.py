import os
import os.path as osp
from src.image import *
from src.utils import *

data_dir = "data/LIDC-IDRI/"


def test_plot_HU_range():
    dcm_path = osp.join(
        data_dir, "LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/")
    file_name = "HU_range"
    scans = load_scans(dcm_path)
    plot_HU_range(scans, file_name)


def test_make_gif():
    dcm_path = osp.join(
        data_dir, "LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/")
    scans = load_scans(dcm_path)
    hu_scans = hu_rescale_scans(scans)
    make_gif(hu_scans)


def test_plot_3d():
    dcm_path = osp.join(
        data_dir, "LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/")
    scans = load_scans(slice_path)
    hu_scans = hu_rescale_scans(scans)
    imgs_after_resamp, spacing = resample(hu_scans, scans, [1, 1, 1])
    verts, faces = make_mesh(imgs_after_resamp, threshold=350)
    plot_3d(verts, faces)
