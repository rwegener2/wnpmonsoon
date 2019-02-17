import numpy as np
from affine import Affine


def degfromnorth(uas, vas):
    """
    :param uas: np array of eastward wind speed - strength of wind coming from the east
    :param vas: np array of northward wind speed - strength of wind coming from the north
    :return: wind direction - wind coming from that direction in degrees clockwise from north
    """
    # Set values where both uas and vas are equal to zero to nan, so that no wind corresponds to nan
    both_zero = np.logical_and(uas == 0, vas == 0)
    zeros_indices = zip(*np.where(both_zero is True))
    uas_nans = uas
    vas_nans = vas
    for i, j, k in zeros_indices:
        uas_nans[i, j, k] = np.NaN
        vas_nans[i, j, k] = np.NaN
    # Calculate the degrees ccw from west using arctan2, which accounts for when arctan blows up
    deg_west = np.degrees(np.arctan2(vas_nans, uas_nans))
    # Return the result as the degrees clockwise from north
    return (-deg_west + 270) % 360


def affine_from_coords(lats, lons):
    if len(set(np.diff(lats))) > 1:
        raise TypeError('Inconsistent lats.  See input data')
    height = np.diff(lats)[0]
    if len(set(np.diff(lons))) > 1:
        raise TypeError('Inconsistent lons.  See input data')
    width = np.diff(lons)[0]
    return Affine(width, 0, lons.min(), 0, -height, lats.max())


def coords_from_affine(affine, height, width):
    # (1.88, 0.0, 120.94, 0.0, -1.25, 39.38)
    if not isinstance(affine, tuple):
        affine = Affine(*affine)
    if not isinstance(affine, Affine):
        raise TypeError('input must be an affine object or a tuple')
    lats = np.arange(affine.f, affine.f + height*affine.e, affine.e)
    lons = np.arange(affine.c, affine.c + width*affine.a, affine.a)
    return lats, lons
