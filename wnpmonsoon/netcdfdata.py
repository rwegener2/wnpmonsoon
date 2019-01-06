from wnpmonsoon.netcdf import NetCDFWriter
import netCDF4 as nc
import numpy as np


class NetcdfData(object):
    def __init__(self, file_):
        dataset = nc.Dataset(file_, 'r+')
        self.var_name = list(dataset.variables.keys())[-1]
        self.model_id = dataset.model_id
        self.var_units = dataset.variables[self.var_name].units
        self.variable = np.asarray(dataset.variables[self.var_name][:])
        self.lats = np.asarray(dataset.variables['lat'])
        self.lons = np.asarray(dataset.variables['lon'])
        self.time = np.asarray(dataset.variables['time'])
        self.calendar = dataset.variables['time'].calendar
        self.t_units = dataset.variables['time'].units

    def pr_unit_conversion(self):
        """
        Convert precipitation flux (units kg / m^2 / s) to precipitation rate (units mm/day)
        """
        if self.var_name != 'pr' and self.var_units != 'kg m-2 s-1':
            raise TypeError("Cannot run this method on a dataset that isn't precipitation flux")
        self.variable = self.variable*86400
        self.var_units = "mm hr-1"

    def write(self, output_filename, time_var=None, time_units=None, lats=None, lons=None, var_name=None, variable=None,
              var_units=None, calendar=None):
        """Write the netcdf object out to the filename provided and overwrite any variables specified by the user"""
        if not time_var:
            time_var = self.time
        if not time_units:
            time_units = self.t_units
        if not lats:
            lats = self.lats
        if not lons:
            lons = self.lons
        if not var_name:
            var_name = self.var_name
        if not variable:
            variable = self.variable
        if not var_units:
            var_units = self.var_units
        if not calendar:
            calendar = self.calendar
        writer = NetCDFWriter(output_filename)
        writer.create_time_variable("time", time_var, units=time_units, calendar=calendar)
        writer.create_grid_variables(lats, lons)
        writer.create_data_variable(var_name, ("time", "lat", "lon"), variable, units=var_units)
        writer.set_global_attributes(model_id=self.model_id)

    def jjaso_subset(self):
        # """
        # take input netcdf and output netcdf with only months June-October
        # :return:
        # """
        # from netCDF4 import num2date
        # datelist = num2date(self.time, self.t_units, calendar='proleptic_gregorian')
        #
        # # create empty matricies to hold new data
        # cnt = 0
        # model_pr_new = np.full((len(yrindx), model_pr.shape[1], model_pr.shape[2]), np.NaN)
        # time_new = np.full([len(yrindx), ], np.NaN)
        #
        # # fill new model matricies with data
        # for k in yrindx:
        #     model_pr_new[cnt] = model_pr[int(k)]
        #     time_new[cnt] = k
        #     cnt += 1
        #
        # time_new = np.array(time_new)
        # return [JJASO, JJASO_times]
        raise NotImplementedError

    def yearly_subset(self, start_year, end_year):
        """
        clip netcdf to year range specified by inputs
        """
        raise NotImplementedError

    def filename_generator(self):
        # """
        # returns a string with an ideal filename for the file
        # :return:
        # """
        # # TODO maybe not possible to make general enough for all models and temporal situations
        # return self.var_name + '_' + self.model_id
        raise NotImplementedError

    @classmethod
    def wd_from_existing(cls, existing, wd_data):
        # obj = cls.__new__(cls)
        # # existing_nc = cls(file_=existing, )
        # obj.var_name = 'wd'
        # obj.model_id = existing.model_id
        # obj.var_units = 'degrees clockwise from north'
        # obj.variable = wd_data
        # obj.lats = existing.lats
        # obj.lons = existing.lons
        # obj.time = existing.time
        # obj.calendar = existing.calendar
        # obj.t_units = existing.t_units
        # return obj
        raise NotImplementedError
