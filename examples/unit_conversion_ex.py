from wnpmonsoon.netcdfdata import NetcdfData
from wnpmonsoon.wind_direction import wind_direction

###############################
# Calculating precipitation rate from precipitation flux
# Calculating wind direction from uas and vas
# Inspecting the netcdf object
###############################

# ESTABLISHING DATA LOCATION
# folder = r"C:\repos\wnpmonsoon-testdata"
folder = '/home/rwegener/repos/wnpmonsoon/tests/data/'
precip_test_file = folder + r"\ACCESS1-0\pr_day_ACCESS1-0_rcp85_r1i1p1_1year_spatial_clip.nc"
uas_test_file = folder + r"\CMCC-CM\uas_day_CMCC-CM_rcp85_r1i1p1_1year_spatial_clip.nc"
vas_test_file = folder + r"\CMCC-CM\vas_day_CMCC-CM_rcp85_r1i1p1_1year_spatial_clip.nc"
precip_test_file_lin = folder + r"/ACCESS1-0/pr_day_ACCESS1-0_rcp85_r1i1p1_1year_spatial_clip.nc"
uas_test_file_lin = folder + r"/CMCC-CM/uas_day_CMCC-CM_rcp85_r1i1p1_1year_spatial_clip.nc"
vas_test_file_lin = folder + r"/CMCC-CM/vas_day_CMCC-CM_rcp85_r1i1p1_1year_spatial_clip.nc"

# EXAMPLE WIND DIRECTION
save_at = '/home/rwegener/repos/wnpmonsoon/winddir-tst.nc'
wdir_obj = wind_direction(uas_test_file_lin, vas_test_file_lin, save_location=save_at)

print('model:', wdir_obj.model_id)
print('variable:', wdir_obj.var_name)
print('max and min of variable data:', wdir_obj.variable.max(), wdir_obj.variable.min())

# EXAMPLE PRECIPITATION RATE
precip_obj = NetcdfData(precip_test_file_lin)
precip_obj.pr_unit_conversion()

print('model:', precip_obj.model_id)
print('variable:',precip_obj.var_name)
print('variable units:', precip_obj.var_units)
