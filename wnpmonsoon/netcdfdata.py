from netcdf import NetCDFWriter
import netCDF4 as nc
import numpy as np
from netCDF4 import num2date


class NetcdfData(object):
    def __init__(self, file_, variable, create_new=False):
        if not create_new:
            dataset = nc.Dataset(file_, 'r+')
            self.var_name = variable
            self.model_id = dataset.model_id
            self.var_units = dataset.variables[variable].units
            self.variable = np.asarray(dataset.variables[variable][:])
            self.lats = np.asarray(dataset.variables['lat'])
            self.lons = np.asarray(dataset.variables['lon'])
            self.time = np.asarray(dataset.variables['time'])
            self.calendar = dataset.variables['time'].calendar
            self.t_units = dataset.variables['time'].units

    # TODO should this be a mix-in or something else?  How to sort type of NetCDFData type
    def pr_unit_conversion(self):
        """
        convert precipitation flux (units kg / m^2 / s) to precipitation rate (units mm/day)
        """
        self.variable = self.variable*86400
        self.var_units = "mm / hour"
        self.var_name = "pr"

    def jjaso_subset(self):
        """
        take input netcdf and output netcdf with only months June-October
        :return:
        """
        datelist = num2date(self.time, self.t_units, calendar='proleptic_gregorian')

        # create empty matricies to hold new data
        cnt = 0
        model_pr_new = np.full((len(yrindx), model_pr.shape[1], model_pr.shape[2]), np.NaN)
        time_new = np.full([len(yrindx), ], np.NaN)

        # fill new model matricies with data
        for k in yrindx:
            model_pr_new[cnt] = model_pr[int(k)]
            time_new[cnt] = k
            cnt += 1

        time_new = np.array(time_new)
        return [JJASO, JJASO_times]

    def yearly_subset(self, start_year, end_year):
        """
        clip netcdf to year range specified by inputs
        """
        raise NotImplementedError

    def write(self, output_filename, time_var=None, time_units=None, lats=None, lons=None, var_name=None, variable=None,
              var_units=None, calendar=None):
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
        # TODO all other positional args will be optional message
        writer = NetCDFWriter(output_filename)
        writer.create_time_variable("time", time_var, units=time_units, calendar=calendar)
        writer.create_grid_variables(lats, lons)
        writer.create_data_variable(var_name, ("time", "lat", "lon"), variable, units=var_units)
        writer.set_global_attributes(model_id=self.model_id)
