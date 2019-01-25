from wnpmonsoon.ncdata import NCdata
import numpy as np


def degfromnorth(uas, vas):
    """
    :param uas: eastward wind speed - strength of wind coming from the east
    :param vas: northward wind speed - strength of wind coming from the north
    :return: wind direction - wind coming from that direction in degrees clockwise from north
    """
    # Set values where both uas and vas are equal to zero to nan, so that no wind corresponds to nan
    both_zero = np.logical_and(uas == 0, vas == 0)
    zeros_indices = zip(*np.where(both_zero is True))
    uas_nans = uas
    vas_nans = vas
    for i, j, k in zeros_indices:
        print('modified indices ', i, j, k)
        uas_nans[i, j, k] = np.NaN
        vas_nans[i, j, k] = np.NaN
    # Calculate the degrees ccw from west using arctan2, which accounts for when arctan blows up
    deg_west = np.degrees(np.arctan2(vas_nans, uas_nans))
    # Return the result as the degrees clockwise from north
    return (-deg_west + 270) % 360


def wind_direction(uas_file, vas_file, save_location):
    """
    :param uas_file: filepath of 'uas'
    :param vas_file: filepath of 'vas'
    :param save_location: where to save output
    :return: a NCdata object wind direction
    """
    uas = NCdata(uas_file)
    vas = NCdata(vas_file)
    wind_dir_data = degfromnorth(uas.variable, vas.variable)
    uas.write(save_location, variable=wind_dir_data, var_name='wdir', var_units='degrees clockwise from north')
    return NCdata(save_location)
