import numpy as np
import scipy.ndimage
from skimage import measure, morphology


def to_ndarray(slice):
    """Convert slice types to :class:`numpy.ndarray`
    """
    return np.array(slice.pixel_array).astype(np.int16)


def hu_rescale(slice, slope, intercept):
    """Convert slice raw pixel array to HU
    Args:
        slice:
        slope:
        intercept:
    """
    # convert ouside pixel-values to air:
    # I'm using <= -1000 to be sure that other defaults are captured as well
    img = set_outside_scanner_to_air(slice)

    if slope != 1:
        img = slope * img.astype(np.float64)
        img = img.astype(np.int16)

    img += np.int16(intercept)

    return np.array(img, dtype=np.int16)


def hu_rescale_scans(slices):
    images = np.stack([hu_rescale(to_ndarray(slice), slice.RescaleSlope,
                                  slice.RescaleIntercept) for slice in slices])
    return images.astype(np.int16)


def set_outside_scanner_to_air(raw_pixelarrays):
    # In LIDC we find outside-scanner-regions with raw-values of -2000.
    # Let's threshold between air (0) and this default (-2000) using -1000
    raw_pixelarrays[raw_pixelarrays <= -1000] = 0
    return raw_pixelarrays


def window(hu_img, window_width, window_level):
    lower = float(window_level) - 0.5 * float(window_width)
    upper = float(window_level) + 0.5 * float(window_width)
    return np.clip(hu_img.copy(), lower, upper)


def normalize(img):
    """Normalize the image.
    """
    min, max = np.min(img), np.max(img)
    norm_img = (img.copy() - min) / (max - min)
    return (norm_img*255.0).astype('uint8')


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
