from wnpmonsoon.ncdata import NCdata
from wnpmonsoon.monsoondata import MonsoonData, criteria_generator
import netCDF4 as nc
import os

###############################
# Calculating pr and wind_dir using NCData methods
# Calculating monsoon based off those objects
###############################

# ESTABLISHING DATA LOCATION
# folder = r"C:\repos\wnpmonsoon\tests\data"
folder = r"/home/rwegener/repos/wnpmonsoon/tests/data/"
# precip_test_file = folder + r"\ACCESS1-0\pr_day_ACCESS1-0_rcp85_r1i1p1_1year_spatial_clip.nc"
precip_test_file_lin = os.path.join(folder, r"ACCESS1-0/pr_day_ACCESS1-0_rcp85_r1i1p1_1year_spatial_clip.nc")
uas_test_file_lin = os.path.join(folder, r"ACCESS1-0/uas_day_ACCESS1-0_rcp85_r1i1p1_1year_spatial_clip.nc")
vas_test_file_lin = os.path.join(folder, r"ACCESS1-0/vas_day_ACCESS1-0_rcp85_r1i1p1_1year_spatial_clip.nc")

# Generate precipitation rate
with nc.Dataset(precip_test_file_lin, 'r') as p_flux_reader:
    print(p_flux_reader.__class__)
    p_rate = NCdata.pr_rate_from_flux(p_flux_reader)
p_rate_path = os.path.join(folder, r"created/precip_rate_ACCESS1-0.nc")
p_rate.write(p_rate_path)

# Generate wind direction
with nc.Dataset(uas_test_file_lin, 'r') as uas_reader, \
     nc.Dataset(vas_test_file_lin, 'r') as vas_reader:
    wdir = NCdata.wind_dir_from_components(uas_reader, vas_reader)
wdir_path = os.path.join(folder, r"created/wdir_ACCESS1-0.nc")
wdir.write(wdir_path)

# Compute monsoon
criteria = criteria_generator(pr_min=5, wd_min=180, wd_max=270)

with nc.Dataset(p_rate_path, 'r') as pr_reader, \
     nc.Dataset(wdir_path, 'r') as wd_reader:
     output = MonsoonData.compute(pr_reader, wd_reader, criteria)


# Testing opening an existsing file
filepath = '/home/rwegener/data/monsoon_test.nc'
with nc.Dataset(filepath, 'r') as mi_reader:
    new = MonsoonData(mi_reader)
