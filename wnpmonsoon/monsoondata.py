from wnpmonsoon.ncdata import NCdata
from wnpmonsoon import tools
from rasterio.warp import reproject
from rasterio.enums import Resampling
from itertools import groupby
import numpy as np
from netCDF4 import num2date
import netCDF4


def criteria_generator(pr_min=-np.inf, pr_max=np.inf, wd_min=-np.inf, wd_max=np.inf, consecutive_days=0):
    def pr_criteria(pr):
        return ((pr_min < pr) & (pr < pr_max)).astype(int)

    def wd_criteria(wd):
        return ((wd_min < wd) & (wd < wd_max)).astype(int)

    criteria_dict = {'pr_min': pr_min, 'pr_max': pr_max, 'wd_min': wd_min, 'wd_max': wd_max,
                     'consecutive_days': consecutive_days}
    return {'precip': pr_criteria, 'wind_dir': wd_criteria, 'summary_dict': criteria_dict}


class MonsoonData(NCdata):
    def __init__(self, dataset_reader):
        NCdata.__init__(self, dataset_reader)

    @classmethod
    def compute(cls, precip_rate, wind_direction, criteria):
        # Checking input types
        if isinstance(precip_rate, netCDF4._netCDF4.Dataset):
            pr = NCdata(precip_rate)
        elif isinstance(precip_rate, NCdata):
            pr = precip_rate
        else:
            raise TypeError('precip_rate of class ', precip_rate.__class__, ' must be either a netCDF4 reader or a '
                                                                            'NCData object')
        if isinstance(wind_direction, netCDF4._netCDF4.Dataset):
            wind_dir = NCdata(wind_direction)
        elif isinstance(wind_direction, NCdata):
            wind_dir = wind_direction
        else:
            raise TypeError('wind_direction of class ', wind_direction.__class__, ' must be either a netCDF4 reader or '
                                                                                  'a NCData object')
        # Create new monsoon object
        NCmonsoon = MonsoonData.__new__(cls)

        # Check that pr and wind_dir have properly aligning grids
        if pr.lats != wind_dir.lats or pr.lons != wind_dir.lons:
            pr.variable, wind_dir.variable, new_lats, new_lons = cls.align_grids(pr, wind_dir)
            pr.lats = wind_dir.lats = new_lats
            pr.lons = wind_dir.lons = new_lons

        # Check that pr and wind_dir are compatible; if so assign shared variables to monsoon object
        for attr in ['lats', 'lons', 'time', 'calendar', 'time_units', 'model_id']:
            if (np.asarray(getattr(pr, attr) != getattr(wind_dir, attr))).all():
                raise TypeError(attr, ' not aligned in pr and wind_dir')
            setattr(NCmonsoon, attr, getattr(pr, attr))

        # Create boolean monsoon from pr and wind_dir
        passing_pr = criteria['precip'](pr.variable)
        passing_wd = criteria['wind_dir'](wind_dir.variable)
        blank_monsoon = passing_pr & passing_wd

        # Add newly calculated data to the monsoon object
        NCmonsoon.var_name = 'monsoon'
        NCmonsoon.var_units = 'boolean'
        NCmonsoon.variable = blank_monsoon

        # Created combined global attributes
        monsoon_globalattrs = {}
        all_keys = list(set(list(pr.globalattrs.keys()) + list(wind_dir.globalattrs.keys())))
        for key in all_keys:
            if key not in pr.globalattrs.keys():
                monsoon_globalattrs[key + '_wd'] = wind_dir.globalattrs[key]
            elif key not in wind_dir.globalattrs.keys():
                monsoon_globalattrs[key + '_pr'] = pr.globalattrs[key]
            elif pr.globalattrs[key] == wind_dir.globalattrs[key]:
                monsoon_globalattrs[key] = pr.globalattrs[key]
            else:
                monsoon_globalattrs[key + '_pr'] = pr.globalattrs[key]
                monsoon_globalattrs[key + '_wd'] = wind_dir.globalattrs[key]

        monsoon_globalattrs['monsoon_criteria'] = criteria['summary_dict']
        NCmonsoon.globalattrs = monsoon_globalattrs
        return NCmonsoon

    @staticmethod
    def align_grids(ncdata1, ncdata2):
        data_track = {}
        # TODO checking size here isn't ideal -- how to check that ???
        if ncdata1.variable.size > ncdata2.variable.size:
            modifying_nc = ncdata2.__copy__()
            template = ncdata1.__copy__()
            data_track.update({'ncdata1': template, 'ncdata2': modifying_nc})
        elif ncdata1.variable.size < ncdata2.variable.size:
            modifying_nc = ncdata1.__copy__()
            template = ncdata2.__copy__()
            data_track.update({'ncdata1': modifying_nc, 'ncdata2': template})
        else:
            return ncdata1.variable, ncdata2.variable, ncdata1.lats, ncdata1.lons

        # Resample the data
        transformed = np.zeros(template.variable.shape)
        src_transform = tools.affine_from_coords(modifying_nc.lats, modifying_nc.lons)
        dst_transform = tools.affine_from_coords(template.lats, template.lons)
        reproject(
            modifying_nc.variable, transformed,
            src_transform=src_transform,
            dst_transform=dst_transform,
            src_crs={'init': 'EPSG:4326'},
            dst_crs={'init': 'EPSG:4326'},
            resampling=Resampling.mode)

        # Update modified variable
        modifying_nc.variable = transformed
        return data_track['ncdata1'].variable, data_track['ncdata2'].variable, template.lats, template.lons

    def decadal_rollup(self, average=False, write=None):
        """
        :param average: if True return average # of days per decade
        :param write: if input with a filepath save the rolled up data to that location
        :return: numpy array for rolled up data
        """
        datelist = num2date(self.time, self.time_units, calendar=self.calendar)
        decades = np.array([list(g) for k, g in groupby(datelist, lambda i: i.year // 10)])
        if write:
            self.write(write)
        raise NotImplementedError
