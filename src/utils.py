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


def series_modality(series_path):
    """Return modality type of series
    """
    if os.listdir(series_path):
        dcm_path = osp.join(series_path, os.listdir(series_path)[0])
        dcm = pydicom.dcmread(dcm_path)
        return dcm.Modality
    else:
        return None


# def modality_filter(series_path):
#     """Filt out other modality except for CT
#     """
#     dcm_path = osp.join(series_path, os.listdir(series_path)[0])


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
    """Count files under the path of folder
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


if __name__ == "__main__":
    INPUT_FOLDER = 'data/LIDC/LIDC-IDRI'
    # patients = load_patients(INPUT_FOLDER)
    # patients_path = [osp.join(INPUT_FOLDER, patient) for patient in patients]
    # check_study(patients_path)
    patients_dict = record_CT(INPUT_FOLDER)
    print(patients_dict)
