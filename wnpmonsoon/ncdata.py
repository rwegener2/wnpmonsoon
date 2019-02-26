from wnpmonsoon.netcdf import NetCDFWriter
from wnpmonsoon import tools
from netCDF4 import num2date, date2num
import netCDF4
import numpy as np


class NCdata(object):
    def __init__(self, dataset_reader):
        if not isinstance(dataset_reader, netCDF4._netCDF4.Dataset):
            raise TypeError('Input to NCData should be a netCDF4._netCDF4.Dataset object')
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

    def __copy__(self):
        return type(self).fromexisting(self.var_name, self.var_units, self.variable, self.lats, self.lons, self.time,
                                       self.calendar, self.time_units, self.model_id, self.globalattrs)

    @classmethod
    def fromexisting(cls, var_name, var_units, variable, lats, lons, time, calendar, time_units, model_id, globalattrs):
        ncdata = cls.__new__(cls)
        ncdata.var_name = var_name
        ncdata.var_units = var_units
        ncdata.variable = variable
        ncdata.lats = lats
        ncdata.lons = lons
        ncdata.time = time
        ncdata.calendar = calendar
        ncdata.time_units = time_units
        ncdata.model_id = model_id
        ncdata.globalattrs = globalattrs
        return ncdata

    @classmethod
    def pr_rate_from_flux(cls, pr_rate_reader):
        """
        Create a NCdata object for precipitation rate using an input dataset_reader from precipitation rate
        :param pr_rate_reader: netCDF4 Dataset object for precipitation flux
        :return: NCdata object for precipitation rate
        """
        if not isinstance(pr_rate_reader, netCDF4._netCDF4.Dataset):
            raise TypeError('Input to NCData should be a netCDF4._netCDF4.Dataset object')
        pr_flux = NCdata(pr_rate_reader)
        if pr_flux.var_name != 'pr' or pr_flux.var_units != 'kg m-2 s-1':
            raise TypeError("Filepath used to create precipitation rate must be a flux nc file, with a variable name "
                            "of 'pr' and units of 'kg m-2 s-1")
        pr_flux.variable = pr_flux.variable * 86400
        pr_flux.var_units = "mm hr-1"
        return pr_flux

    @classmethod
    def wind_dir_from_components(cls, uas_reader, vas_reader):
        """
        Create a NCdata object for wind direction based on uas and vas.  For global attributes, the attributes that the
        two datasets share will be input into the wind direction object exactly as they were.  Those attributes that
        differ (usually history, creation_date, etc.) will be post-pended with `_uas` or `_vas` and added to the global
        attributes as such
        :param uas_reader: netCDF4 Dataset object for uas
        :param vas_reader: netCDF Dataset object for vas
        :return: NCdata object for wind direction with appropriately updated data and units
        """
        if not all(isinstance(reader, netCDF4._netCDF4.Dataset) for reader in [uas_reader, vas_reader]):
            raise TypeError('Input to NCData should be a netCDF4._netCDF4.Dataset object')

        # Ensure inputs are of proper type
        if 'uas' not in uas_reader.variables.keys():
            raise TypeError("uas_reader must have a variable 'uas'")
        if 'vas' not in vas_reader.variables.keys():
            raise TypeError("vas_reader must have a variable 'vas'")

        # Ensure uas and vas align and can be converted to wind direction
        uas = NCdata(uas_reader)
        vas = NCdata(vas_reader)
        shared_vars = [item for item in list(uas.__dict__.keys()) if item not in ['var_name', 'variable', 'globalattrs']]
        wind_dir = cls.__new__(cls)
        for var in shared_vars:
            if (np.asarray(getattr(uas, var) != getattr(vas, var))).all():
                raise TypeError('uas and vas are not aligned (do not have the same value) for global attribute: ', var)
            setattr(wind_dir, var, getattr(uas, var))

        # Created combined global attributes
        wdir_globalattrs = {}
        for key, value in uas.globalattrs.items():
            if value == vas.globalattrs[key] == value:
                wdir_globalattrs[key] = value
            else:
                wdir_globalattrs[key + '_uas'] = value
                wdir_globalattrs[key + '_vas'] = vas.globalattrs[key]

        # Set new attributes
        wind_dir.var_name = 'wdir'
        wind_dir.var_units = 'degrees clockwise from north'
        wind_dir.globalattrs = wdir_globalattrs
        wind_dir.variable = tools.degfromnorth(uas=uas.variable, vas=vas.variable)
        return wind_dir

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

    def filename_generator(self):
        """
        returns a string with an ideal filename for the file
        :return:
        """
        return "_".join([self.var_name, self.globalattrs['frequency'], self.model_id,
                         self.globalattrs['parent_experiment_id'], self.globalattrs['experiment_id'],
                         self.globalattrs['parent_experiment_rip']])

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
        writer.set_global_attributes(**self.globalattrs)
        writer.set_global_attributes(model_id=self.model_id)
        writer.create_time_variable("time", time_var, units=time_units, calendar=calendar)
        writer.create_grid_variables(lats, lons)
        writer.create_data_variable(var_name, ("time", "lat", "lon"), variable, units=var_units)
