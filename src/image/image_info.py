import os
import os.path as osp
import pydicom
import numpy as np


def load_scans(dcm_path):
    """
    Load DICOM files sorting by the actual image position in the scan
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