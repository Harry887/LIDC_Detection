import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import pydicom
import pylidc as pl
import os
import os.path as osp
import scipy.ndimage
import matplotlib.pyplot as plt

from skimage import measure, morphology
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from collections import Counter


def load_scan(path):
    slices = [pydicom.read_file(path + '/' + s) for s in os.listdir(path)]
    print(slices)


def load_patients(dataset_path):
    patients = os.listdir(dataset_path)
    return sorted(patients)


def count_files(path):
    file_num = 0
    for root, dirs, files in os.walk(path):
        file_num += len(files)
    return file_num


def check_study(patients_path):
    studies = dict()
    types = dict()
    dup = dict()
    for p in patients_path:
        for study in os.listdir(p):
            study_path = osp.join(patients_path, study)
            for series in os.listdir(study_path):
                pass
                # studies[osp.basename(p)] = study[:10] + study[-6:]
                # if study[10:-6] != '':
                #     types[osp.basename(p)] = study[10:-6]
                # assert study[:10] == '01-01-2000'
                # if study[:10] + study[-6:] in ['01-01-2000-34723', '01-01-2000-58320', '01-01-2000-27983', '01-01-2000-79315', '01-01-2000-35412', '01-01-2000-82159', '01-01-2000-11943']:
                #     dup[osp.basename(p)] = study
    print(studies)


if __name__ == "__main__":
    INPUT_FOLDER = 'data/LIDC/LIDC-IDRI'
    patients = load_patients(INPUT_FOLDER)
    patients_path = [osp.join(INPUT_FOLDER, patient) for patient in patients]
    check_study(patients_path)
    # load_scan()
