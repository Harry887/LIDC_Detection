import numpy as np
import pandas as pd
import pydicom
import pylidc as pl
import os
import os.path as osp
import scipy.ndimage
import matplotlib.pyplot as plt
import seaborn as sns
import imageio
# from IPython import display
from skimage import measure, morphology
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from collections import Counter


# def load_scans(dcm_path):
#     files = os.listdir(dcm_path)
#     sorted_file = np.sort(files)
#     f = [pydicom.dcmread(dcm_path + "/" + str(file))
#          for file in sorted_file if file.endswith(".dcm")]
#     return f




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


def set_outside_scanner_to_air(raw_pixelarrays):
    # in OSIC we find outside-scanner-regions with raw-values of -2000.
    # Let's threshold between air (0) and this default (-2000) using -1000
    raw_pixelarrays[raw_pixelarrays <= -1000] = 0
    return raw_pixelarrays


def transform_to_hu(slices):
    images = np.stack([file.pixel_array for file in slices])
    images = images.astype(np.int16)

    # convert ouside pixel-values to air:
    # I'm using <= -1000 to be sure that other defaults are captured as well
    images = set_outside_scanner_to_air(images)

    # convert to HU
    for n in range(len(slices)):

        intercept = slices[n].RescaleIntercept
        slope = slices[n].RescaleSlope

        if slope != 1:
            images[n] = slope * images[n].astype(np.float64)
            images[n] = images[n].astype(np.int16)

        images[n] += np.int16(intercept)

    return np.array(images, dtype=np.int16)


def plot_CT_HU(scans, hu_scans, name):
    fig, ax = plt.subplots(1, 4, figsize=(20, 3))
    ax[0].set_title("Original CT-scan")
    ax[0].imshow(scans[0].pixel_array, cmap="bone")
    ax[1].set_title("Pixelarray distribution")
    sns.distplot(scans[0].pixel_array.flatten(), ax=ax[1])

    ax[2].set_title("CT-scan in HU")
    ax[2].imshow(hu_scans[0], cmap="bone")
    ax[3].set_title("HU values distribution")
    sns.distplot(hu_scans[0].flatten(), ax=ax[3])

    for m in [0, 2]:
        ax[m].grid(False)
    plt.savefig("demo/"+name+".png")


def make_gif(hu_series):
    imageio.mimsave("demo/gif.gif", hu_series, duration=0.1)
    # display.Image(filename="demo/gif.gif", format='png')


def resample(image, scans, new_spacing=[1, 1, 1]):
    spacing = np.array([float(scans[0].SliceThickness),
                        float(scans[0].PixelSpacing[0]),
                        float(scans[0].PixelSpacing[0])])

    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor

    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)

    return image, new_spacing


def make_mesh(image, threshold=-300, step_size=1):
    # Position the scan upright,
    # so the head of the patient would be at the top facing the camera
    p = image.transpose(2, 1, 0)
    verts, faces, norm, val = measure.marching_cubes_lewiner(
        p, threshold, step_size=step_size, allow_degenerate=True)
    return verts, faces


def plot_3d(verts, faces):
    x, y, z = zip(*verts)

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Fancy indexing: `verts[faces]` to generate a collection of triangles
    mesh = Poly3DCollection(verts[faces], alpha=0.70)
    face_color = [0.45, 0.45, 0.75]
    mesh.set_facecolor(face_color)
    ax.add_collection3d(mesh)

    ax.set_xlim(0, max(x))
    ax.set_ylim(0, max(y))
    ax.set_zlim(0, max(z))

    plt.savefig("demo/plot_3d.png")


def get_window_value(feature):
    if type(feature) == pydicom.multival.MultiValue:
        return np.int(feature[0])
    else:
        return np.int(feature)


def dicom_data(patient_path):
    im_path = list()
    for study in os.listdir(patient_path):
        for series in os.listdir(patient_path + study):
            x = study+'/'+series
            im_path.append(x)

    pixelspacing_r = []
    pixelspacing_c = []
    slice_thicknesses = []
    ids = []
    id_pth = []
    row_values = []
    column_values = []
    window_widths = []
    window_levels = []
    modality = []
    kvp = []

    for i in im_path:
        example_dcm = os.listdir(patient_path + i + "/")[0]
        dataset = pydicom.dcmread(patient_path + i + "/" + example_dcm)
        if dataset.Modality != 'CT':
            continue
        ids.append(i.split('/')[0]+'_'+i.split('/')[1])
        id_pth.append(patient_path + i)
        window_widths.append(get_window_value(dataset.WindowWidth))
        window_levels.append(get_window_value(dataset.WindowCenter))

        spacing = dataset.PixelSpacing
        slice_thicknesses.append(dataset.SliceThickness)

        row_values.append(dataset.Rows)
        column_values.append(dataset.Columns)
        pixelspacing_r.append(spacing[0])
        pixelspacing_c.append(spacing[1])

        modality.append(dataset.Modality)
        kvp.append(dataset.KVP)

    scan_properties = pd.DataFrame(data=ids, columns=["ID"])
    scan_properties.loc[:, "rows"] = row_values
    scan_properties.loc[:, "columns"] = column_values
    scan_properties.loc[:, "area"] = scan_properties["rows"] * \
        scan_properties["columns"]
    scan_properties.loc[:, "pixelspacing_r"] = pixelspacing_r
    scan_properties.loc[:, "pixelspacing_c"] = pixelspacing_c
    scan_properties.loc[:, "pixelspacing_area"] = scan_properties.pixelspacing_r * \
        scan_properties.pixelspacing_c
    scan_properties.loc[:, "slice_thickness"] = slice_thicknesses
    scan_properties.loc[:, "id_pth"] = id_pth
    scan_properties.loc[:, "window_width"] = window_widths
    scan_properties.loc[:, "window_level"] = window_levels
    scan_properties.loc[:, "modality"] = modality
    scan_properties.loc[:, "kvp"] = kvp

    return scan_properties


