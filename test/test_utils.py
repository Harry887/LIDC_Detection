import os
import os.path as osp
from src import *
from src.utils import *

data_dir = "data/LIDC-IDRI/"


def test_load_patients():
    patients = load_patients(data_dir)
    assert len(patients) == 1012


def test_load_scans():
    slice_path = osp.join(
        data_dir, "LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/")
    slices = load_scans(slice_path)
    assert len(slices) == 133


def test_count_files():
    path = osp.join(data_dir, "LIDC-IDRI-0019/")
    assert count_files(path) == 306


def test_series_modality():
    CT_series_path = osp.join(
        data_dir, "LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/")
    DX_series_path = osp.join(
        data_dir, "LIDC-IDRI-0001/01-01-2000-35511/3000923-62357/")
    assert series_modality(CT_series_path) == 'CT'
    assert series_modality(DX_series_path) == 'DX'


def test_get_CT_series():
    CT_series, total_series = get_CT_series(data_dir)
    assert len(CT_series) < total_series


def test_get_dicom_info():
    dcm_path = osp.join(
        data_dir, "LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/000001.dcm")
    slice_info = get_dicom_info(dcm_path)
    assert slice_info["modality"] == 'CT'
