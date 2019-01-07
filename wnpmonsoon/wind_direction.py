from wnpmonsoon.netcdfdata import NetcdfData
import numpy as np
import os


def degfromnorth(uas, vas):
    """
    :param uas: eastward wind speed - strength of wind coming from the east
    :param vas: northward wind speed - strength of wind coming from the north
    :return: wind direction - wind coming from that direction in degrees clockwise from north
    """
    # Calculate the degrees ccw from west using arctan2, which accounts for when arctan blows up
    deg_west = np.degrees(np.arctan2(vas, uas))
    # Return the result as the degrees clockwise from north
    return (-deg_west + 270) % 360


def wind_direction(uas_file, vas_file, save_location):
    """
    :param uas_file: filepath of 'uas'
    :param vas_file: filepath of 'vas'
    :param save_location: where to save output
    :return: a NetcdfData object wind direction
    """
    uas = NetcdfData(uas_file)
    vas = NetcdfData(vas_file)
    wind_dir_data = degfromnorth(uas.variable, vas.variable)
    uas.write(save_location, variable=wind_dir_data, var_name='wdir', var_units='degrees clockwise from north')
    return NetcdfData(save_location)
