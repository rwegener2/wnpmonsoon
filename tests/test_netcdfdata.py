from wnpmonsoon.netcdfdata import NetcdfData
from numpy.testing import assert_almost_equal
import netCDF4 as nc
import pytest


@pytest.fixture
def direct_pr_access10(path_pr_access10):
    """Daily pr ACCESS1-0 rcp85 loaded directly with netCDF4"""
    return nc.Dataset(path_pr_access10)


@pytest.fixture
def direct_uas_cmcccm(path_uas_cmcccm):
    """Daily uas CMCC-CM rcp85 loaded directly with netCDF4"""
    return nc.Dataset(path_uas_cmcccm)


@pytest.fixture
def direct_vas_cnrmcm5(path_vas_cnrmcm5):
    """Daily vas CNRM-CM5 rcp85 loaded directly with netCDF4"""
    return nc.Dataset(path_vas_cnrmcm5)


@pytest.fixture
def pr_access10(path_pr_access10):
    """Daily pr ACCESS1-0 rcp85"""
    return NetcdfData(path_pr_access10)


@pytest.fixture
def uas_cmcccm(path_uas_cmcccm):
    """Daily uas CMCC-CM rcp85"""
    return NetcdfData(path_uas_cmcccm)


@pytest.fixture
def vas_cnrmcm5(path_vas_cnrmcm5):
    """Daily vas CNRM-CM5 rcp85"""
    return NetcdfData(path_vas_cnrmcm5)


def test_init_pr_access10(path_pr_access10):
    nc_obj = NetcdfData(path_pr_access10)
    assert nc_obj.var_name == 'pr'
    assert nc_obj.model_id == 'ACCESS1-0'
    assert nc_obj.var_units == 'kg m-2 s-1'
    assert_almost_equal(nc_obj.variable, direct_pr_access10.variables['pr'], decimal=1)
    assert_almost_equal(nc_obj.lats, direct_pr_access10.variables['lat'], decimal=1)
    assert_almost_equal(nc_obj.lons, direct_pr_access10.variables['lon'], decimal=1)
    assert_almost_equal(nc_obj.time, direct_pr_access10.variables['time'], decimal=1)
    assert nc_obj.calendar == 'proleptic_gregorian'
    assert nc_obj.t_units == 'days since 0001-01-01'


def test_init_uas_cmcccm(path_uas_cmcccm):
    nc_obj = NetcdfData(path_uas_cmcccm)
    assert nc_obj.var_name == 'uas'
    assert nc_obj.model_id == 'CMCC-CM'
    assert nc_obj.var_units == 'm s-1'
    assert_almost_equal(nc_obj.variable, path_uas_cmcccm.variables['pr'], decimal=1)
    assert_almost_equal(nc_obj.lats, path_uas_cmcccm.variables['lat'], decimal=1)
    assert_almost_equal(nc_obj.lons, path_uas_cmcccm.variables['lon'], decimal=1)
    assert_almost_equal(nc_obj.time, path_uas_cmcccm.variables['time'], decimal=1)
    assert nc_obj.calendar == 'standard'
    assert nc_obj.t_units == 'days since 2006-1-1'


def test_init_vas_cnrmcm5(path_vas_cnrmcm5):
    nc_obj = NetcdfData(path_vas_cnrmcm5)
    assert nc_obj.var_name == 'vas'
    assert nc_obj.model_id == 'CNRM-CM5'
    assert nc_obj.var_units == 'm s-1'
    assert_almost_equal(nc_obj.variable, path_vas_cnrmcm5.variables['pr'], decimal=1)
    assert_almost_equal(nc_obj.lats, path_vas_cnrmcm5.variables['lat'], decimal=1)
    assert_almost_equal(nc_obj.lons, path_vas_cnrmcm5.variables['lon'], decimal=1)
    assert_almost_equal(nc_obj.time, path_vas_cnrmcm5.variables['time'], decimal=1)
    assert nc_obj.calendar == 'gregorian'
    assert nc_obj.t_units == 'days since 2006-01-01 00:00:00'


def test_pr_unit_conversion(pr_access10, direct_pr_access10):
    unit_converted = pr_access10.pr_unit_conversion()
    assert unit_converted.var_units == 'mm hr-1'
    assert_almost_equal(unit_converted.variable, direct_pr_access10.variables['pr']*86400, decimal=1)


def test_pr_units_input_error(uas_cmcccm):
    with pytest.raises(TypeError):
        uas_cmcccm.pr_unit_conversion()


def test_write_no_overwrites():
    pass


def test_write_overwrite_time():
    pass


def test_write_overwrite_coords():
    pass


def test_write_overwrite_variable():
    pass
