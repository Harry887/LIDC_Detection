import os
import os.path as osp
from src.image import *
from src.utils import *

data_dir = "data/LIDC-IDRI/"


def test_to_ndarray():
    dcm_path = osp.join(
        data_dir, "LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/")
    scans = load_scans(dcm_path)
    slice_rawpixels = to_ndarray(scans[40])
    plot_slice(slice_rawpixels, "demo/slice_rawpixels.jpg")


def test_hu_rescale():
    dcm_path = osp.join(
        data_dir, "LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/")
    scans = load_scans(dcm_path)
    slice_info = get_dicom_info(scans[40])
    slice_rawpixels = to_ndarray(scans[40])
    hu_img = hu_rescale(
        slice_rawpixels, slice_info["slope"], slice_info["intercept"])
    plot_slice(hu_img, "demo/hu_img.jpg")


def test_hu_rescale_scans():
    slice_path = osp.join(
        data_dir, "LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/")
    file_name = "CT_HU_example"
    scans = load_scans(slice_path)
    hu_scans = hu_rescale_scans(scans)
    plot_CT_HU(scans, hu_scans, file_name)


def test_window():
    dcm_path = osp.join(
        data_dir, "LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/")
    scans = load_scans(dcm_path)
    slice_info = get_dicom_info(scans[40])
    slice_rawpixels = to_ndarray(scans[40])
    hu_img = hu_rescale(
        slice_rawpixels, slice_info["slope"], slice_info["intercept"])
    windowed_img = window(
        hu_img, slice_info["window_width"], slice_info["window_level"])
    plot_slice(windowed_img, "demo/windowed_img.jpg")


def test_normalize():
    dcm_path = osp.join(
        data_dir, "LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/")
    scans = load_scans(dcm_path)
    slice_info = get_dicom_info(scans[40])
    slice_rawpixels = to_ndarray(scans[40])
    hu_img = hu_rescale(
        slice_rawpixels, slice_info["slope"], slice_info["intercept"])
    windowed_img = window(
        hu_img, slice_info["window_width"], slice_info["window_level"])
    norm_img = normalize(windowed_img)
    plot_slice(norm_img, "demo/norm_img.jpg")
