#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""Encompasses most of the netCDF4 Python API calls to write a netCDF file.

Author
------
Ryan D Smith
14WS/WXE, ACC, USAF
ryan.smith.106@us.af.mil

"""

# -----------------------------------------------------------------------------
#   Imports
# -----------------------------------------------------------------------------

import time

import netCDF4
import numpy as np

# -----------------------------------------------------------------------------
#   Custom Exceptions
# -----------------------------------------------------------------------------


class InvalidSizeError(Exception):
    pass


class LengthMismatchError(Exception):
    pass

# -----------------------------------------------------------------------------
#   Class: NetCDFWriter(Dataset, object)
# -----------------------------------------------------------------------------


class NetCDFWriter(netCDF4.Dataset, object):
    """Provide functionality to write netCDF files of climate data.

    Parameters
    ----------
    filename : str
        The file name of the output netCDF file.
    **kwargs
        Any keyword argument accepted by netCDF4.Datasest

    """
    def __init__(self, filename, **kwargs):
        super(NetCDFWriter, self).__init__(filename, mode='w', **kwargs)
    
    def _create_time_dimension(self, name, size=1):
        self.createDimension(name, size=size)

    def _create_xy_dimensions(self, ysize, xsize):
        self.createDimension('lat', size=ysize)
        self.createDimension('lon', size=xsize)

    def create_extra_dimensions(self, **kwargs):
        """Create reference dimensions other than time, x, and y.

        Use the inherited createDimension() method and specific kwargs
        formatting to control the name and size of each new dimension.
        
        All new dimensions created through this method will have no 
        attributes associated with them.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments. To properly create new dimensions,
            the keyword argument names should be the desired name of the
            dimension being created and the value should be the dimension's
            desired size.

        Raises
        ------    
        InvalidSizeError
            If the value of any keyword argument is not an :obj:`int`.
        
        Examples
        --------
        >>> writer = NetCDFWriter("test.nc")
        >>> writer.create_extra_dimensions(z=12)

        """
        for key in kwargs:
            if not kwargs[key] or not isinstance(kwargs[key], int):
                msg = "{} is not a valid size argument".format(
                    kwargs[key]
                    )
                raise InvalidSizeError(msg)

        for name, size in kwargs.items():
            self.createDimension(name, size=size)

    def create_time_variable(self, name, time, **kwargs):
        """Create and fill the time variable.

        First calls the internal ``_create_time_dimension method``, which
        is responsible for setting up the reference dimension for the time
        variable.

        By default, the time dimension will be set to the size of the 
        sequence of values passed to the parameter `time`. To force time
        to be an unlimited dimension, the keyword/value pair size=None must
        be provided.

        All variables support gzip compression by default.

        Parameters
        ----------
        name : str
            The desired name for the time variable. This will also become
            the name of the reference dimension.
        time : `array-like`
            The data to fill the time variable with. Should be an array-like
            object. Lists, tuples, and NumPy arrays are accepted.
        **kwargs
            Arbitrary keyword arguments. Any keyword arguments passed in
            will be used to set attributes describing the time variable.
            Argument names will become the attribute names, and argument values
            will become the attribute values.
        
        Raises
        ------
        ValueError
            If the sequence of time values provided has more than 1 dimension.
            This will cause the associated Dimension object to be created with
            a size that is equal to the length of the sequence's ``first``
            dimension only. Subsequently, the data array will be a different
            size than allocated, which will raise an error during run time.
            
        Notes
        -----
        If `time` is of type :obj:`numpy.ndarray`, the resulting size of the
        time dimension will be the length of axis 0 of that array. See the 
        `Raises` section for more details.
        
        """
        self._create_time_dimension(name, size=kwargs.pop("size", len(time)))
        
        self.createVariable(
            name,
            time.dtype,
            (name,),
            zlib=True
            )
            
        self.variables[name].setncattr(
            "units", 
            kwargs.pop("units", "seconds since 1970-1-1")
            )

        if kwargs:
            for key, value in kwargs.items():
                if key != "size":
                    self.variables[name].setncattr(key, value)
                

        self.variables[name][:] = time[:]

    def create_grid_variables(self, lats, lons):
        """Create and fill the x/y reference variables.

        First calls the private ``_create_xy_dimensions`` method with the sizes
        of the x and y arrays as parameters to create the reference dimensions
        for the x and y variables.

        These variables, and their corresponding dimensions are, by default,
        named lat (for the y dimension) and lon (for the x) in accordance with
        CF-1.6 conventions.

        Currently only 1D arrays for x/y data are supported.

        All variables support gzip compression by default.

        Parameters
        ----------
        lats : :obj:`numpy.array`
            An array of latitude (y) points.
        lons : :obj:`numpy.array`
            An array of longitude (x) points.
            
        Raises
        ------
        ValueError
            If the provided arrays of latitude and longitude points are larger
            than 1 dimension.

        """
        if lats.ndim != 1 or lons.ndim != 1:
            msg = "lat or lon array is larger than 1 dimension"
            raise ValueError(msg)
            
        conventions = {
            "lat": {"long_name": "latitude",
                    "units": "degrees_north",
                    "standard_name": "latitude"},
            "lon": {"long_name": "longitude",
                    "units": "degrees_east",
                    "standard_name": "longitude"},
                }
        
        self._create_xy_dimensions(lats.size, lons.size)

        self.createVariable(
            'lat',
            lats.dtype,
            ('lat',),
            zlib=True
            )
            
        self.createVariable(
            'lon',
            lons.dtype,
            ('lon',),
            zlib=True
            )

        for var in "lat", "lon":
            standards = conventions[var]
            for key, value in standards.items():
                self.variables[var].setncattr(key, value)
        
        self.variables['lat'][:] = lats[:]
        self.variables['lon'][:] = lons[:]

    def create_data_variable(self, name, dims, data, **kwargs):
        """Create the main data variable.

        The most basic netCDF file typically has reference dimensions, maybe
        variables which correspond to those dimensions and hold the data
        associated with them, and variables which hold the data described
        by those reference data.

        Data variables would be something like Air Temperature, while
        the reference variables (and dimensions) would be time, latitude, and
        longitude.

        Create a data variable, and fill it with the data passed in
        by the client.
        
        `fill_value` is a supported argument. If not provided, then -999
        is automatically used.

        All variables support gzip compression by default.

        Parameters
        ----------
        name : str
            The desired name for the main data variable.
        dims : tuple
            The names of the dimensions which describe this variable
            (e.g. time, latitude, longitude).
        data : :obj:`numpy.ndarray`
            The data with which the main variable will be filled. A default
            fill value of -999 will be assigned as an attribute to this
            variable unless a different value is passed in via a keyword
            argument named fill_value.
        **kwargs
            Arbitrary keyword arguments. Any keyword arguments passed in
            will be used to set attributes describing the data variable.
            Argument names will become the attribute names, and argument values
            will become the attribute values.
            
        Raises
        ------
        TypeError
            If `dims` is not a tuple.
        ValueError
            If a given dimension name does not exist in the current file.

        """
        if not isinstance(dims, tuple):
            raise TypeError("Requires tuple of reference dimension names")
            
        for dim in dims:
            if dim not in self.dimensions:
                msg = "{} is not an existing reference dimension".format(dim)
                raise ValueError(msg)
                
        if hasattr(data, "fill_value"):
            fill = data.fill_value
        else:
            fill = -999

        self.createVariable(
            name,
            data.dtype,
            dims,
            fill_value=kwargs.pop('fill_value', fill),
            zlib=True
            )

        if kwargs:
            for key, value in kwargs.items():
                self.variables[name].setncattr(key, value)

        self.variables[name][:] = data[:]

    def create_extra_variables(self, names, dims, data, **kwargs):
        """Create extra netCDF variables.
        
        This method is used mostly to add variables which may
        contain extra reference data beyond normal time and spatial
        reference data.
        
        Parameters
        ----------
        names : tuple
            A tuple of variable names to be created.
        dims : tuple
            A tuple of tuples containing reference dimension names to be
            created for this variable to reference. The index of each sub-tuple
            corresponds to the variable name which will reference the
            dimensions in the sub-tuple.
        data : tuple
            A tuple of data with which each corresponding variable name will be
            filled.
        **kwargs
            Keyword arguments whose names correspond to one of the variable
            names passed in as the 1st positional parameter.
            The values of those arguments should be tuples of 2-tuples where
            each 2-tuple indicates the name and value of an attribute, which is
            to be assigned to the variable being created.
            
        Raises
        ------
        LengthMismatchError
            If the lengths of `names`, `dims`, and `data` don't all match.
        
        Notes
        -----
        Names should be a tuple of variable names.

        Dimensions should be a tuple of tuples, where the index of each
        sub-tuple corresponds to the index of the associated variable name.

        kwargs should be composed of arguments whose names correspond to a name
        in names, and whose value is a tuple of 2-tuples where each 2-tuple
        is the (``name``, ``value``) of any attributes describing that
        variable.

        All variables support gzip compression by default.

        Examples
        --------
        >>> from datetime import datetime
        >>> filename = 'test.nc'
        >>> w = NetCDFWriter(filename, mode='w')
        >>> names = ('level', 'time')
        >>> dims = (('level',), ('time',))
        >>> data = (200, datetime(1970, 1, 1))
        >>> w.create_extra_variables(names, data, dims, level=('units', 'hPa'))

        """
        if len(names) != len(dims) != len(data):
            msg = "Not all of names, dims, or data have the same length"
            raise LengthMismatchError(msg)

        for i in xrange(len(names)):
            name = names[i]
            datum = data[i]
            dim = dims[i]

            self.createVariable(
                name,
                datum.dtype,
                dim,
                zlib=True
                )

            if name in kwargs:
                for n, v in kwargs[name]:
                    self.variables[name].setncattr(n, v)

            self.variables[name][:] = datum[:]

    def set_global_attributes(self, **kwargs):
        """Set the global attributes of the file.

        By default, the creation date/time of the file and the conventions
        string are set. 
        
        Any keyword argument will be used to set other file level attributes.
        The keys of the keyword arguments dictionary map to the attribute
        names, and the values map to the value of the corresponding attribute.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments. Any keyword arguments passed in
            will be used to set the global file attributes.
            Argument names will become the attribute names, and argument values
            will become the attribute values.

        """
        self.setncattr("conventions", "CF-1.6")
        self.setncattr("creation_date", time.asctime())

        if kwargs:
            for key, value in kwargs.items():
                self.setncattr(key, value)
