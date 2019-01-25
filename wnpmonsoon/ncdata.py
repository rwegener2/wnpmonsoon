from wnpmonsoon.netcdf import NetCDFWriter
from netCDF4 import num2date, date2num
import numpy as np


class NCdata(object):
    def __init__(self, dataset_reader):
        self.var_name = list(dataset_reader.variables.keys())[-1]
        self.var_units = dataset_reader.variables[self.var_name].units
        self.variable = np.asarray(dataset_reader.variables[self.var_name][:])
        self.lats = np.asarray(dataset_reader.variables['lat'])
        self.lons = np.asarray(dataset_reader.variables['lon'])
        self.time = np.asarray(dataset_reader.variables['time'])
        self.calendar = dataset_reader.variables['time'].calendar
        self.time_units = dataset_reader.variables['time'].units
        self.model_id = dataset_reader.getncattr('model_id')
        self.globalattrs = {}
        for key in dataset_reader.ncattrs():
            self.globalattrs[key] = dataset_reader.getncattr(key)

    def pr_unit_conversion(self):
        """
        Convert precipitation flux (units kg / m^2 / s) to precipitation rate (units mm/day)
        """
        if self.var_name != 'pr' and self.var_units != 'kg m-2 s-1':
            raise TypeError("Cannot run this method on a dataset that isn't precipitation flux")
        self.variable = self.variable*86400
        self.var_units = "mm hr-1"

    def jjaso_subset(self):
        """
        Clip data down to only months of June-October
        :return:
        """
        datelist = num2date(self.time, self.time_units, calendar=self.calendar)
        # Get months and indices
        jjaso_indices = []
        jjaso_dates = []
        for index, date in enumerate(datelist):
            if date.month in list(range(6, 11)):
                jjaso_indices.append(index)
                jjaso_dates.append(date)
        # Reset new variables
        self.variable = np.delete(self.variable, jjaso_indices, axis=0)
        self.time = date2num(jjaso_dates, units=self.time_units, calendar=self.calendar)
        # TODO custom global attribute column that tracks this

    def filename_generator(self):
        """
        returns a string with an ideal filename for the file
        :return:
        """
        return "_".join([self.var_name, self.globalattrs['frequency'], self.model_id,
                         self.globalattrs['parent_experiment_id'], self.globalattrs['experiment_id'],
                         self.globalattrs['parent_experiment_rip']])
        # TODO append , custom modifiers (i.e. jjaso)

    def write(self, output_filename, time_var=None, time_units=None, lats=None, lons=None, var_name=None, variable=None,
              var_units=None, calendar=None):
        """Write the netcdf object out to the filename provided and overwrite any variables specified by the user"""
        try:
            time_var.size
        except AttributeError:
            time_var = self.time
        if not time_units:
            time_units = self.time_units
        if not calendar:
            calendar = self.calendar
        try:
            lats.size
        except AttributeError:
            lats = self.lats
        try:
            lons.size
        except AttributeError:
            lons = self.lons
        if not var_name:
            var_name = self.var_name
        if not var_units:
            var_units = self.var_units
        try:
            variable.size
        except AttributeError:
            variable = self.variable
        writer = NetCDFWriter(output_filename)
        # for key, value in self.globalattrs.items():
        writer.set_global_attributes(**self.globalattrs)
        writer.set_global_attributes(model_id=self.model_id)
        writer.create_time_variable("time", time_var, units=time_units, calendar=calendar)
        writer.create_grid_variables(lats, lons)
        writer.create_data_variable(var_name, ("time", "lat", "lon"), variable, units=var_units)
