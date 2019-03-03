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


@pytest.fixture
def precip_rate_ncdata_cnrmcm5(path_pr_cnrmcm5):
    with nc.Dataset(path_pr_cnrmcm5, 'r') as pflux_src:
        return NCdata.pr_rate_from_flux(pflux_src)


@pytest.fixture
def wdir_ncdata_cnrmcm5(path_uas_cnrmcm5, path_vas_cnrmcm5):
    with nc.Dataset(path_uas_cnrmcm5, 'r') as uas_reader, \
         nc.Dataset(path_vas_cnrmcm5, 'r') as vas_reader:
        return NCdata.wind_dir_from_components(uas_reader, vas_reader)


@pytest.fixture
def fake_pr_matrix():
    return np.array([[0, 0, 6, 4],
                     [2, 5, 9, 0],
                     [10, 8, 7, 3],
                     [7, 6, 2, 1],
                     [6, 6, 1, 0]])


@pytest.fixture
def fake_wdir_matrix():
    return np.array([[100, 80, 110, 75],
                     [145, 162, 40, 12],
                     [173, 189, 13, 352],
                     [200, 240, 280, 342],
                     [293, 305, 210, 15]])


@pytest.fixture
def truth_monsoon_indx_access13(path_monsoon_access13):
    with nc.Dataset(path_monsoon_access13, 'r') as reader:
        return np.asarray(reader.variables['monsoon'][:])


def test_aligngrids_largernc1(precip_rate_ncdata_access13, wdir_ncdata_access13, path_wdir_cnrmcm5_adj_coords):
    precip, wdir, lats, lons = MonsoonData.align_grids(precip_rate_ncdata_access13, wdir_ncdata_access13)
    wdir_truth = np.load(path_wdir_cnrmcm5_adj_coords)
    assert_almost_equal(precip, precip_rate_ncdata_access13.variable)
    assert_almost_equal(wdir, wdir_truth)
    assert_almost_equal(lats, precip_rate_ncdata_access13.lats)
    assert_almost_equal(lons, precip_rate_ncdata_access13.lons)


def test_aligngrids_largernc2(precip_rate_ncdata_access13, wdir_ncdata_access13, path_wdir_cnrmcm5_adj_coords):
    wdir, precip, lats, lons = MonsoonData.align_grids(wdir_ncdata_access13, precip_rate_ncdata_access13)
    wdir_truth = np.load(path_wdir_cnrmcm5_adj_coords)
    assert_almost_equal(precip, precip_rate_ncdata_access13.variable)
    assert_almost_equal(wdir, wdir_truth)
    assert_almost_equal(lats, precip_rate_ncdata_access13.lats)
    assert_almost_equal(lons, precip_rate_ncdata_access13.lons)


def test_aligngrids_samesize(precip_rate_ncdata_cnrmcm5, wdir_ncdata_cnrmcm5):
    wdir, precip, lats, lons = MonsoonData.align_grids(wdir_ncdata_cnrmcm5, precip_rate_ncdata_cnrmcm5)
    assert_almost_equal(precip, precip_rate_ncdata_cnrmcm5.variable)
    assert_almost_equal(wdir, wdir_ncdata_cnrmcm5.variable)
    assert_almost_equal(lats, precip_rate_ncdata_cnrmcm5.lats)
    assert_almost_equal(lons, precip_rate_ncdata_cnrmcm5.lons)


def test_criteria_blank_pr_full_wind(fake_pr_matrix, fake_wdir_matrix):
    criteria = criteria_generator(wd_min=165, wd_max=200)
    passing_pr = criteria['precip'](fake_pr_matrix)
    passing_wd = criteria['wind_dir'](fake_wdir_matrix)
    truth_pr = np.ones(fake_pr_matrix.shape)
    truth_wdir = np.array([[0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [1, 1, 0, 0],
                           [1, 0, 0, 0],
                           [0, 0, 0, 0]])
    truth_combined = np.array([[0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [1, 1, 0, 0],
                               [1, 0, 0, 0],
                               [0, 0, 0, 0]])
    assert_almost_equal(truth_pr, passing_pr)
    assert_almost_equal(truth_wdir, passing_wd)
    assert_almost_equal(truth_combined, (passing_pr & passing_wd))


# def test_criteria_blank_pr_overlap_wind(fake_pr_matrix, fake_wdir_matrix):
#     criteria = criteria_generator(wd_min=330, wd_max=60)
#     passing_pr = criteria['precip'](fake_pr_matrix)
#     passing_wd = criteria['wind_dir'](fake_wdir_matrix)
#     truth_pr = np.ones(fake_pr_matrix.shape)
#     truth_wdir = np.array([[0, 0, 0, 0],
#                            [0, 0, 1, 1],
#                            [0, 0, 1, 1],
#                            [0, 0, 0, 1],
#                            [0, 0, 0, 1]])
#     assert_almost_equal(truth_pr, passing_pr)
#     assert_almost_equal(truth_wdir, passing_wd)
# TODO adjust criteria function so it accepts this type of request ^^^


def test_criteria_min_pr_full_wind(fake_pr_matrix, fake_wdir_matrix):
    criteria = criteria_generator(pr_min=4, wd_min=165, wd_max=200)
    passing_pr = criteria['precip'](fake_pr_matrix)
    passing_wd = criteria['wind_dir'](fake_wdir_matrix)
    truth_pr = np.array([[0, 0, 1, 1],
                         [0, 1, 1, 0],
                         [1, 1, 1, 0],
                         [1, 1, 0, 0],
                         [1, 1, 0, 0]])
    truth_wdir = np.array([[0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [1, 1, 0, 0],
                           [1, 0, 0, 0],
                           [0, 0, 0, 0]])
    truth_combined = np.array([[0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [1, 1, 0, 0],
                               [1, 0, 0, 0],
                               [0, 0, 0, 0]])
    assert_almost_equal(truth_pr, passing_pr)
    assert_almost_equal(truth_wdir, passing_wd)
    assert_almost_equal(truth_combined, (passing_pr & passing_wd))


def test_criteria_full_pr_blank_wind(fake_pr_matrix, fake_wdir_matrix):
    criteria = criteria_generator(pr_min=2, pr_max=7)
    passing_pr = criteria['precip'](fake_pr_matrix)
    passing_wd = criteria['wind_dir'](fake_wdir_matrix)
    truth_pr = np.array([[0, 0, 1, 1],
                         [1, 1, 0, 0],
                         [0, 0, 1, 1],
                         [1, 1, 1, 0],
                         [1, 1, 0, 0]])
    truth_combined = np.array([[0, 0, 1, 1],
                         [1, 1, 0, 0],
                         [0, 0, 1, 1],
                         [1, 1, 1, 0],
                         [1, 1, 0, 0]])
    truth_wdir = np.ones(fake_wdir_matrix.shape)
    assert_almost_equal(truth_pr, passing_pr)
    assert_almost_equal(truth_wdir, passing_wd)
    assert_almost_equal(truth_combined, (passing_pr & passing_wd))


def test_criteria_full_pr_max_wind(fake_pr_matrix, fake_wdir_matrix):
    criteria = criteria_generator(pr_min=2, pr_max=7, wd_max=90)
    passing_pr = criteria['precip'](fake_pr_matrix)
    passing_wd = criteria['wind_dir'](fake_wdir_matrix)
    truth_pr = np.array([[0, 0, 1, 1],
                         [1, 1, 0, 0],
                         [0, 0, 1, 1],
                         [1, 1, 1, 0],
                         [1, 1, 0, 0]])
    truth_wdir = np.array([[0, 1, 0, 1],
                           [0, 0, 1, 1],
                           [0, 0, 1, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 1]])
    truth_combined = np.array([[0, 0, 0, 1],
                               [0, 0, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 0]])
    assert_almost_equal(truth_pr, passing_pr)
    assert_almost_equal(truth_wdir, passing_wd)
    assert_almost_equal(truth_combined, (passing_pr & passing_wd))


def test_criteria_max_pr_min_wind(fake_pr_matrix, fake_wdir_matrix):
    # TODO add testing for the criteria dic
    criteria = criteria_generator(pr_max=5, wd_min=270)
    passing_pr = criteria['precip'](fake_pr_matrix)
    passing_wd = criteria['wind_dir'](fake_wdir_matrix)
    truth_pr = np.array([[1, 1, 0, 1],
                         [1, 1, 0, 1],
                         [0, 0, 0, 1],
                         [0, 0, 1, 1],
                         [0, 0, 1, 1]])
    truth_wdir = np.array([[0, 0, 0, 0],
                           [0, 0, 0, 0],
                           [0, 0, 0, 1],
                           [0, 0, 1, 1],
                           [1, 1, 0, 0]])
    truth_combined = np.array([[0, 0, 0, 0],
                               [0, 0, 0, 0],
                               [0, 0, 0, 1],
                               [0, 0, 1, 1],
                               [0, 0, 0, 0]])
    assert_almost_equal(truth_pr, passing_pr)
    assert_almost_equal(truth_wdir, passing_wd)
    assert_almost_equal(truth_combined, (passing_pr & passing_wd))


def test_init(path_monsoon_access13, precip_rate_ncdata_access13, wdir_ncdata_access13, truth_monsoon_indx_access13):
    with nc.Dataset(path_monsoon_access13, 'r') as monsoon_reader:
        monsoon = MonsoonData(monsoon_reader)
    assert_almost_equal(truth_monsoon_indx_access13, monsoon.variable)
    assert monsoon.var_name == 'monsoon'
    assert_almost_equal(monsoon.lats, precip_rate_ncdata_access13.lats)
    assert monsoon.time_units == wdir_ncdata_access13.time_units
    assert monsoon.globalattrs['frequency'] == precip_rate_ncdata_access13.globalattrs['frequency']
    assert monsoon.globalattrs['institute_id'] == wdir_ncdata_access13.globalattrs['institute_id']
    # TODO what is happening here?
    # assert 'monsoon_criteria' in monsoon.globalattrs.keys()


def test_init_improper_input(path_monsoon_access13):
    with pytest.raises(TypeError):
        MonsoonData(path_monsoon_access13)


def test_monsoon_compute_nc_input(precip_rate_ncdata_access13, wdir_ncdata_access13, truth_monsoon_indx_access13):
    criteria = criteria_generator(pr_min=5, wd_min=180, wd_max=270)
    monsoon = MonsoonData.compute(precip_rate_ncdata_access13, wdir_ncdata_access13, criteria)
    assert_almost_equal(truth_monsoon_indx_access13, monsoon.variable)
    assert monsoon.var_name == 'monsoon'
    assert_almost_equal(monsoon.lats, precip_rate_ncdata_access13.lats)
    assert monsoon.time_units == wdir_ncdata_access13.time_units
    assert monsoon.globalattrs['frequency'] == precip_rate_ncdata_access13.globalattrs['frequency']
    assert monsoon.globalattrs['institute_id'] == wdir_ncdata_access13.globalattrs['institute_id']
    assert monsoon.globalattrs['monsoon_criteria'] == criteria['summary_dict']


def test_monsoon_compute_reader_input(path_pr_access13, path_wdir_access13, precip_rate_ncdata_access13,
                                      wdir_ncdata_access13, truth_monsoon_indx_access13):
    criteria = criteria_generator(pr_min=5, wd_min=180, wd_max=270)
    with nc.Dataset(path_pr_access13, 'r') as pr_reader, \
         nc.Dataset(path_wdir_access13, 'r') as wdir_reader:
        monsoon = MonsoonData.compute(pr_reader, wdir_reader, criteria)
        assert_almost_equal(truth_monsoon_indx_access13, monsoon.variable)
    assert monsoon.var_name == 'monsoon'
    assert_almost_equal(monsoon.lats, precip_rate_ncdata_access13.lats)
    assert monsoon.time_units == wdir_ncdata_access13.time_units
    assert monsoon.globalattrs['frequency'] == precip_rate_ncdata_access13.globalattrs['frequency']
    assert monsoon.globalattrs['institute_id'] == wdir_ncdata_access13.globalattrs['institute_id']
    assert monsoon.globalattrs['monsoon_criteria'] == criteria['summary_dict']


def test_monsoon_compute_pr_typeerror(path_pr_access13, wdir_ncdata_access13):
    with pytest.raises(TypeError):
        MonsoonData.compute(path_pr_access13, wdir_ncdata_access13,
                            criteria_generator(pr_min=5, wd_min=180, wd_max=270))


def test_monsoon_compute_wdir_typeerror(precip_rate_ncdata_access13, path_uas_access13):
    with pytest.raises(TypeError):
        MonsoonData.compute(precip_rate_ncdata_access13, path_uas_access13,
                            criteria_generator(pr_min=5, wd_min=180, wd_max=270))


def test_monsoon_compute_misaligned_models(precip_rate_ncdata_access13, wdir_ncdata_cnrmcm5):
    with pytest.raises(TypeError):
        MonsoonData.compute(precip_rate_ncdata_access13, wdir_ncdata_cnrmcm5,
                            criteria_generator(pr_min=5, wd_min=180, wd_max=270))
