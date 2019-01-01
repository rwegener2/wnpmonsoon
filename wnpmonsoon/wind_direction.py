from wnpmonsoon.netcdfdata import NetcdfData
import numpy as np
import math


# def olddegfromnorth(uas, vas):
#     """
#     Code for wind direction calculation exactly as I copied it from the google drive docs
#     :param uas: eastward wind speed
#     :param vas: northward wind speed
#     :return: wind direction in degrees clockwise from north
#     """
#     # Convert components to degrees ccw from east
#     rad = np.arctan(vas / uas)
#     deg_east = rad * 180 / math.pi
#
#     if uas < 0 and vas < 0:
#         deg_north = 270 - deg_east - 180
#     elif uas > 0 and vas < 0:
#         deg_north = 90 - deg_east + 180
#     elif uas > 0 and vas > 0:
#         deg_north = 90 - deg_east + 180
#     elif uas < 0 and vas > 0:
#         deg_north = 270 - deg_east - 180
#     return deg_north

def degfromnorth(uas, vas):
    # TODO function currently works for INDIVIDUAL numbers only; not numpy arrays --- 1/1/19 but wait now it does?
    # TODO use ufunc kwargs of numpy arctan2 to define a "where" array, indicating to fix 0,0 uas,vas values becoming 0
    # <<This allows the input of this to be an array>>  1/1/19 I don't know what that comment is talking about
    """
    :param uas: eastward wind speed - strength of wind coming from the east
    :param vas: northward wind speed - strength of wind coming from the north
    :return: wind direction - wind coming from that direction in degrees clockwise from north
    """
    # Calculate the degrees ccw from west using arctan2, which accounts for when arctan blows up
    deg_west = np.degrees(np.arctan2(vas, uas))
    # Return the result as the degrees clockwise from north
    return (-deg_west + 270) % 360


def wind_direction(uas, vas, save_location=None):
    """
    :param uas: a NetcdfData object of 'uas'
    :param vas: a NetcdfData object of 'vas'
    :param save_location: where to save output, if desired
    :return: a NetcdfData object wind direction
    """
    # TODO check to make sure structures have some lat/lon/time -- maybe do this in the class instead?
    wind_dir_data = degfromnorth(uas, vas)
    wind_dir_nc = NetcdfData.wd_from_existing(uas, wind_dir_data)
    if save_location:
        wind_dir_nc.write(save_location)
    return wind_dir_nc
