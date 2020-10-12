from src.demo import *
from src.utils import *


def test_load_scans():
    slice_path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/"
    slice_info = load_scans(slice_path)
    print(slice_info)


def test_count_files():
    path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/LIDC-IDRI-0106/"
    assert count_files(path) == 159


def test_modality_filter():
    CT_series_path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/"
    DX_series_path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/LIDC-IDRI-0001/01-01-2000-35511/3000923-62357/"
    assert modality_filter(CT_series_path) == 'CT'
    assert modality_filter(CT_series_path) == 'DX'


def test_record_CT():
    dataset_path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/"
    patients_dict = record_CT(dataset_path)
    print(patients_dict)


def test_plot_HU_range():
    slice_path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/"
    file_name = "HU_range"
    scans = load_scans(slice_path)
    plot_HU_range(scans, file_name)


def test_transform_to_hu():
    slice_path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/"
    file_name = "CT_HU"
    scans = load_scans(slice_path)
    hu_scans = transform_to_hu(scans)
    plot_CT_HU(scans, hu_scans, file_name)


def test_make_gif():
    slice_path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/"
    scans = load_scans(slice_path)
    hu_scans = transform_to_hu(scans)
    make_gif(hu_scans)


def test_plot_3d():
    slice_path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/LIDC-IDRI-0001/01-01-2000-30178/3000566-03192/"
    scans = load_scans(slice_path)
    hu_scans = transform_to_hu(scans)
    imgs_after_resamp, spacing = resample(hu_scans, scans, [1, 1, 1])
    verts, faces = make_mesh(imgs_after_resamp, threshold=350)
    plot_3d(verts, faces)


def test_dicom_data():
    patient_path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/LIDC-IDRI-0001/"
    scan_properties = dicom_data(patient_path)
    print(scan_properties.head().T)


def test_get_CT_series():
    dataset_path = "/home1/hli/xiongweiyu/data/LIDC/LIDC-IDRI/"
    CT_series, total_series = get_CT_series(dataset_path)
    assert len(CT_series) > total_series
