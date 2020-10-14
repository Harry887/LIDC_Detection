import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import imageio
import cv2
from skimage import measure, morphology
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def plot_slice(slices, out_path):
    if slices.ndim == 2:
        slices = slices[None, :]
    cv2.imwrite(out_path, slices[0, :])


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
