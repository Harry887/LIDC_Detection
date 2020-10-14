import numpy as np
import pandas as pd
import pydicom
import pylidc as pl
import os
import os.path as osp
import scipy.ndimage
import matplotlib.pyplot as plt
import seaborn as sns
from skimage import measure, morphology
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from collections import Counter


def load_patients(dataset_path):
    """Return patients name list like: LIDC-IDRI-XXXX
    """
    patients = os.listdir(dataset_path)
    return sorted(patients)


def load_scans(dcm_path):
    """
    Load DICOM files sorting by the actual image position in the scan

    Args:
        dcm_path: The path contains DICOM files such as Series

    Return:
        slices: The list of dicom slices
    """
    slices = [pydicom.read_file(dcm_path + '/' + s)
              for s in os.listdir(dcm_path) if s.endswith(".dcm")]
    slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
    try:
        slice_thickness = np.abs(
            slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(
            slices[0].SliceLocation - slices[1].SliceLocation)

    for s in slices:
        s.SliceThickness = slice_thickness

    return slices


def get_window_value(feature):
    if type(feature) == pydicom.multival.MultiValue:
        return np.int(feature[0])
    else:
        return np.int(feature)


def get_dicom_info(slice):
    slice_info = dict()
    slice_info["rows"] = slice.Rows
    slice_info["column"] = slice.Columns
    slice_info["window_width"] = get_window_value(slice.WindowWidth)
    slice_info["window_level"] = get_window_value(slice.WindowCenter)
    slice_info["intercept"] = slice.RescaleIntercept
    slice_info["slope"] = slice.RescaleSlope
    slice_info["pixelspacing_r"] = slice.PixelSpacing[0]
    slice_info["pixelspacing_c"] = slice.PixelSpacing[1]
    slice_info["slice_thicknesses"] = slice.SliceThickness
    slice_info["modality"] = slice.Modality
    slice_info["kvp"] = slice.KVP
    return slice_info


def series_modality(series_path):
    """Return modality type of series
    """
    if os.listdir(series_path):
        dcm_path = osp.join(series_path, os.listdir(series_path)[0])
        dcm = pydicom.dcmread(dcm_path)
        return dcm.Modality
    else:
        return None


def record_CT(dataset_path):
    """load CT image folds into json format
    """
    patients_dict = dict()
    for p in os.listdir(dataset_path):
        print(p)
        patient_path = osp.join(dataset_path, p)
        studies_list = dict()
        for study in os.listdir(patient_path):
            study_path = osp.join(patient_path, study)
            series_list = list()
            for series in os.listdir(study_path):
                series_path = osp.join(study_path, series)
                if series_modality(series_path) != 'CT':
                    continue
                series_list.append(series)
            studies_list[study] = series_list
        patients_dict[p] = studies_list

    return patients_dict


def count_files(path):
    """Count total files under the path of folder
    """
    file_num = 0
    for root, dirs, files in os.walk(path):
        file_num += len(files)
    return file_num


def check_study_index(dataset_path):
    pt_dict = dict()
    for p in os.listdir(dataset_path):
        patient_path = osp.join(dataset_path, p)
        t_list = list()
        for study in os.listdir(patient_path):
            t_list.append(study)
        pt_dict[p] = t_list

    total_study_index = list()
    redundant_dict = dict()
    for p, t_list in pt_dict.items():
        for t in t_list:
            if t not in total_study_index:
                total_study_index.append(t)
            else:
                redundant_dict[t].append(p)


def check_study(patients_path):
    studies = dict()
    types = dict()
    dup = dict()
    for p in patients_path:
        for study in os.listdir(p):
            study_path = osp.join(p, study)
            for series in os.listdir(study_path):
                series_path = osp.join(study_path, study)

                # studies[osp.basename(p)] = study[:10] + study[-6:]
                # if study[10:-6] != '':
                #     types[osp.basename(p)] = study[10:-6]
                # assert study[:10] == '01-01-2000'
                # if study[:10] + study[-6:] in ['01-01-2000-34723', '01-01-2000-58320', '01-01-2000-27983', '01-01-2000-79315', '01-01-2000-35412', '01-01-2000-82159', '01-01-2000-11943']:
                #     dup[osp.basename(p)] = study
    print(studies)


def get_CT_series(dataset_path):
    CT_series = list()
    total_series = 0

    p_list = load_patients(dataset_path)
    for p in p_list:
        p_path = osp.join(dataset_path, p)
        for study in os.listdir(p_path):
            study_path = osp.join(p_path, study)
            for serie in os.listdir(study_path):
                serie_path = osp.join(study_path, serie)
                if series_modality(serie_path) == 'CT':
                    CT_series.append(serie_path)
                total_series += 1
    return CT_series, total_series
