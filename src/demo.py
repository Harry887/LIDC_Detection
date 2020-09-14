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


def load_scans(dcm_path):
    files = os.listdir(dcm_path)
    sorted_file = np.sort(files)
    f = [pydicom.dcmread(dcm_path + "/" + str(file))
         for file in sorted_file if file.endswith(".dcm")]
    return f


def plot_HU_range(scans, name):
    fig, ax = plt.subplots(1, 2, figsize=(20, 5))
    for n in range(10):
        image = scans[n].pixel_array.flatten()
        rescaled_image = image * \
            scans[n].RescaleSlope + scans[n].RescaleIntercept
        sns.distplot(image.flatten(), ax=ax[0])
        sns.distplot(rescaled_image.flatten(), ax=ax[1])
    ax[0].set_title("Raw pixel array distributions for 10 examples")
    ax[1].set_title("HU unit distributions for 10 examples")
    plt.savefig("demo/"+name+".png")


def transform_to_hu(slices):
    images = np.stack([file.pixel_array for file in slices])
    images = images.astype(np.int16)

    # convert ouside pixel-values to air:
    # I'm using <= -1000 to be sure that other defaults are captured as well
    images[images <= -1000] = 0

    # convert to HU
    for n in range(len(slices)):

        intercept = slices[n].RescaleIntercept
        slope = slices[n].RescaleSlope

        if slope != 1:
            images[n] = slope * images[n].astype(np.float64)
            images[n] = images[n].astype(np.int16)

        images[n] += np.int16(intercept)

    return np.array(images, dtype=np.int16)


def load_patients(dataset_path):
    """Return patients name list like: LIDC-IDRI-XXXX
    """
    patients = os.listdir(dataset_path)
    return sorted(patients)


def series_modality(series_path):
    """Return modality type of series
    """
    slice_demo = osp.join(series_path, os.listdir(series_path)[0])
    slice_info = load_scan(slice_demo)
    return slice_info['Modality'].value


def modality_filter():
    """Filt out other modality except for CT
    """
    pass


def count_files(path):
    """Count files under the path of folder
    """
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
