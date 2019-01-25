from wnpmonsoon.ncdata import NCdata
from numpy.testing import assert_almost_equal
from netCDF4 import num2date
import netCDF4 as nc
import numpy as np
import tempfile
import pytest
import os


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
    with nc.Dataset(path_pr_access10, 'r') as dataset_reader:
        return NCdata(dataset_reader)


@pytest.fixture
def uas_cmcccm(path_uas_cmcccm):
    """Daily uas CMCC-CM rcp85"""
    with nc.Dataset(path_uas_cmcccm, 'r') as dataset_reader:
        return NCdata(dataset_reader)


@pytest.fixture
def vas_cnrmcm5(path_vas_cnrmcm5):
    """Daily vas CNRM-CM5 rcp85"""
    with nc.Dataset(path_vas_cnrmcm5, 'r') as dataset_reader:
        return NCdata(dataset_reader)


def test_init_pr_access10(path_pr_access10, direct_pr_access10):
    with nc.Dataset(path_pr_access10, 'r') as dataset_reader:
        nc_obj = NCdata(dataset_reader)
    assert nc_obj.var_name == 'pr'
    assert nc_obj.model_id == 'ACCESS1-0'
    assert nc_obj.var_units == 'kg m-2 s-1'
    assert_almost_equal(nc_obj.variable, direct_pr_access10.variables['pr'], decimal=2)
    assert_almost_equal(nc_obj.lats, direct_pr_access10.variables['lat'], decimal=2)
    assert_almost_equal(nc_obj.lons, direct_pr_access10.variables['lon'], decimal=2)
    assert_almost_equal(nc_obj.time, direct_pr_access10.variables['time'], decimal=2)
    assert nc_obj.calendar == 'proleptic_gregorian'
    assert nc_obj.time_units == 'days since 0001-01-01'
    assert nc_obj.globalattrs['frequency'] == 'day'
    assert nc_obj.globalattrs['parent_experiment_id'] == 'historical'


def test_init_uas_cmcccm(path_uas_cmcccm, direct_uas_cmcccm):
    with nc.Dataset(path_uas_cmcccm, 'r') as dataset_reader:
        nc_obj = NCdata(dataset_reader)
    assert nc_obj.var_name == 'uas'
    assert nc_obj.model_id == 'CMCC-CM'
    assert nc_obj.var_units == 'm s-1'
    assert_almost_equal(nc_obj.variable, direct_uas_cmcccm.variables['uas'], decimal=2)
    assert_almost_equal(nc_obj.lats, direct_uas_cmcccm.variables['lat'], decimal=2)
    assert_almost_equal(nc_obj.lons, direct_uas_cmcccm.variables['lon'], decimal=2)
    assert_almost_equal(nc_obj.time, direct_uas_cmcccm.variables['time'], decimal=2)
    assert nc_obj.calendar == 'standard'
    assert nc_obj.time_units == 'days since 2006-1-1'


def test_init_vas_cnrmcm5(path_vas_cnrmcm5, direct_vas_cnrmcm5):
    with nc.Dataset(path_vas_cnrmcm5, 'r') as dataset_reader:
        nc_obj = NCdata(dataset_reader)
    assert nc_obj.var_name == 'vas'
    assert nc_obj.model_id == 'CNRM-CM5'
    assert nc_obj.var_units == 'm s-1'
    assert_almost_equal(nc_obj.variable, direct_vas_cnrmcm5.variables['vas'], decimal=2)
    assert_almost_equal(nc_obj.lats, direct_vas_cnrmcm5.variables['lat'], decimal=2)
    assert_almost_equal(nc_obj.lons, direct_vas_cnrmcm5.variables['lon'], decimal=2)
    assert_almost_equal(nc_obj.time, direct_vas_cnrmcm5.variables['time'], decimal=2)
    assert nc_obj.calendar == 'gregorian'
    assert nc_obj.time_units == 'days since 2006-01-01 00:00:00'


def test_pr_unit_conversion(pr_access10, direct_pr_access10):
    pr_access10.pr_unit_conversion()
    assert pr_access10.var_units == 'mm hr-1'
    assert_almost_equal(pr_access10.variable, np.asarray(direct_pr_access10.variables['pr'])*86400, decimal=2)


def test_pr_units_input_error(uas_cmcccm):
    with pytest.raises(TypeError):
        uas_cmcccm.pr_unit_conversion()


def test_write_no_overwrites(pr_access10):
    save_location = tempfile.NamedTemporaryFile().name + '.nc'
    pr_access10.write(save_location)
    with nc.Dataset(save_location, 'r') as dataset_reader:
        overwritten_file = NCdata(dataset_reader)
    os.remove(save_location)
    assert_almost_equal(overwritten_file.time, pr_access10.time)
    assert_almost_equal(overwritten_file.lats, pr_access10.lats)
    assert_almost_equal(overwritten_file.variable, pr_access10.variable)
    assert overwritten_file.globalattrs['frequency'] == 'day'
    assert overwritten_file.globalattrs['parent_experiment_id'] == 'historical'


def test_write_overwrite_time(pr_access10):
    save_location = tempfile.NamedTemporaryFile().name + '.nc'
    fake_time_data = np.random.rand(len(pr_access10.time),)
    fake_time_units = 'epochs'
    fake_calendar = 'corgi'
    pr_access10.write(save_location, time_var=fake_time_data, time_units=fake_time_units, calendar=fake_calendar)
    with nc.Dataset(save_location, 'r') as dataset_reader:
        overwritten_file = NCdata(dataset_reader)
    os.remove(save_location)
    assert_almost_equal(overwritten_file.time, fake_time_data)
    assert overwritten_file.model_id == pr_access10.model_id
    assert overwritten_file.time_units == fake_time_units
    assert overwritten_file.calendar == fake_calendar


def test_write_overwrite_coords(pr_access10):
    save_location = tempfile.NamedTemporaryFile().name + '.nc'
    fake_lats = pr_access10.lats + 10
    fake_lons = pr_access10.lons + 10
    pr_access10.write(save_location, lats=fake_lats, lons=fake_lons)
    with nc.Dataset(save_location, 'r') as dataset_reader:
        overwritten_file = NCdata(dataset_reader)
    os.remove(save_location)
    assert overwritten_file.model_id == pr_access10.model_id
    assert_almost_equal(overwritten_file.lats, fake_lats)
    assert_almost_equal(overwritten_file.lons, fake_lons)


def test_write_overwrite_variable(pr_access10):
    save_location = tempfile.NamedTemporaryFile().name + '.nc'
    fake_var_data = np.random.rand(*pr_access10.variable.shape)
    fake_var_unit = 'slugs'
    fake_var_name = 'force'
    pr_access10.write(save_location, variable=fake_var_data, var_units=fake_var_unit, var_name=fake_var_name)
    with nc.Dataset(save_location, 'r') as dataset_reader:
        overwritten_file = NCdata(dataset_reader)
    os.remove(save_location)
    assert_almost_equal(overwritten_file.variable, fake_var_data)
    assert overwritten_file.var_units == fake_var_unit
    assert overwritten_file.var_name == fake_var_name
    assert overwritten_file.model_id == pr_access10.model_id


def test_jjaso(pr_access10):
    pr_access10.jjaso_subset()
    first_day = num2date(pr_access10.time[0], units=pr_access10.time_units, calendar=pr_access10.calendar)
    last_day = num2date(pr_access10.time[-1], units=pr_access10.time_units, calendar=pr_access10.calendar)
    assert first_day.month == 6
    assert first_day.day == 1
    assert last_day.month == 10
    assert last_day.day == 31
