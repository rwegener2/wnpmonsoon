from wnpmonsoon.monsoondata import MonsoonData, criteria_generator
from wnpmonsoon.ncdata import NCdata
import numpy as np
from numpy.testing import assert_almost_equal
import netCDF4 as nc
import pytest


@pytest.fixture
def precip_rate_ncdata_access13(path_pr_access13):
    with nc.Dataset(path_pr_access13, 'r') as pflux_src:
        return NCdata.pr_rate_from_flux(pflux_src)


@pytest.fixture
def wdir_ncdata_access13(path_uas_access13, path_vas_access13):
    with nc.Dataset(path_uas_access13, 'r') as uas_reader, \
         nc.Dataset(path_vas_access13, 'r') as vas_reader:
        return NCdata.wind_dir_from_components(uas_reader, vas_reader)


def test_aligngrids_largernc1(precip_rate_ncdata_access13, wdir_ncdata_access13, path_wdir_cnrmcm5_adj_coords):
    precip, wdir, lats, lons = MonsoonData.align_grids(precip_rate_ncdata_access13, wdir_ncdata_access13)
    wdir_truth = np.load(path_wdir_cnrmcm5_adj_coords)
    assert_almost_equal(precip, precip_rate_ncdata_access13.variable)
    assert_almost_equal(wdir, wdir_truth)
    assert_almost_equal(lats, precip_rate_ncdata_access13.lats)
    assert_almost_equal(lons, precip_rate_ncdata_access13.lons)


# def test_aligngrids_largernc2(precip_rate_ncdata_access13, wdir_ncdata_access13, path_wdir_cnrmcm5_adj_coords):
#     wdir, precip, lats, lons = MonsoonData.align_grids(wdir_ncdata_access13, precip_rate_ncdata_access13)
#     wdir_truth = np.load(path_wdir_cnrmcm5_adj_coords)
#     assert_almost_equal(precip, precip_rate_ncdata_access13.variable)
#     assert_almost_equal(wdir, wdir_truth)
#     assert_almost_equal(lats, precip_rate_ncdata_access13.lats)
#     assert_almost_equal(lons, precip_rate_ncdata_access13.lons)


def test_init():
    pass


def test_init_improper_input():
    pass
