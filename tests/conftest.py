import pytest
import os


@pytest.fixture(scope='session')
def data_dir():
    """Absolute file path to the directory containing test datasets."""
    return os.path.abspath(os.path.join('data'))


@pytest.fixture(scope='session')
def path_pr_access10(data_dir):
    """Path to daily pr ACCESS1-0 rcp85"""
    return os.path.join(data_dir, 'ACCESS1-0', 'pr_day_ACCESS1-0_rcp85_r1i1p1_1year_spatial_clip.nc')


@pytest.fixture(scope='session')
def path_pr_access13(data_dir):
    """Path to daily pr ACCESS1-3 rcp85"""
    return os.path.join(data_dir, 'ACCESS1-3', 'pr_day_ACCESS1-3_rcp85_r1i1p1_1year_spatial_clip.nc')


@pytest.fixture(scope='session')
def path_uas_access13(data_dir):
    """Path to daily pr ACCESS1-3 rcp85"""
    return os.path.join(data_dir, 'ACCESS1-3', 'uas_day_ACCESS1-3_rcp85_r1i1p1_1year_spatial_clip.nc')


@pytest.fixture(scope='session')
def path_vas_access13(data_dir):
    """Path to daily pr ACCESS1-3 rcp85"""
    return os.path.join(data_dir, 'ACCESS1-3', 'vas_day_ACCESS1-3_rcp85_r1i1p1_1year_spatial_clip.nc')



@pytest.fixture(scope='session')
def path_uas_cmcccm(data_dir):
    """Path to daily uas CMCC-CM rcp85"""
    return os.path.join(data_dir, 'CMCC-CM', 'uas_day_CMCC-CM_rcp85_r1i1p1_1year_spatial_clip.nc')


@pytest.fixture(scope='session')
def path_vas_cmcccm(data_dir):
    """Path to daily vas CMCC-CM rcp85"""
    return os.path.join(data_dir, 'CMCC-CM', 'vas_day_CMCC-CM_rcp85_r1i1p1_1year_spatial_clip.nc')

@pytest.fixture(scope='session')
def path_pr_cnrmcm5(data_dir):
    """Path to daily pr CNRM-CM5 rcp85"""
    return os.path.join(data_dir, 'CNRM-CM5', 'pr_day_CNRM-CM5_rcp85_r1i1p1_1year_spatial_clip.nc')


@pytest.fixture(scope='session')
def path_uas_cnrmcm5(data_dir):
    """Path to daily uas CNRM-CM5 rcp85"""
    return os.path.join(data_dir, 'CNRM-CM5', 'uas_day_CNRM-CM5_rcp85_r1i1p1_1year_spatial_clip.nc')


@pytest.fixture(scope='session')
def path_vas_cnrmcm5(data_dir):
    """Path to daily vas CNRM-CM5 rcp85"""
    return os.path.join(data_dir, 'CNRM-CM5', 'vas_day_CNRM-CM5_rcp85_r1i1p1_1year_spatial_clip.nc')


@pytest.fixture(scope='session')
def path_vas_cnrmcm5_modified_lats(data_dir):
    """Path to daily vas CNRM-CM5 rcp85"""
    return os.path.join(data_dir,'created', 'vas_day_CNRM-CM5_rcp85_r1i1p1_modified_coords.nc')


@pytest.fixture(scope='session')
def path_wdir_cnrmcm5_adj_coords(data_dir):
    """Path to daily vas CNRM-CM5 rcp85"""
    return os.path.join(data_dir, 'created', 'access13_wdir_gridadj_truth.npy')

