import netCDF4 as nc
import os
from wnpmonsoon.netcdf import NetCDFWriter
from wnpmonsoon.netcdfdata import NetcdfData

model_precip = NetcdfData(file_, 'pr')
model_precip.pr_unit_conversion()
model_precip.write(output_filename)


print("processing data for file:", file_)
# set up output directory and filename
output_file = directory_saved_files+'/../../../pr_rate/'+os.path.basename(file_).replace("pr", "pr_rate")

# open up the file and extract data
dataset = nc.Dataset(file_, 'r+')
model_pr = dataset.variables['pr'][:]
lats = dataset.variables['lat']
lons = dataset.variables['lon']
time = dataset.variables['time']
# establish "before" test points
# I: make sure appropriate translation is applied to test points
z_len = model_pr.shape[0]-1
x_len = model_pr.shape[1]-1
y_len = model_pr.shape[2]-1
test_point_1_before = model_pr[z_len, x_len, y_len]
test_point_2_before = model_pr[z_len//2, x_len//3, 0]
print('test point 1 value (before):', test_point_1_before, '\n', 'test point 2 value(before)', test_point_2_before)
# multiply by the number of seconds in a month to get the rain rate in average mm/day;
# *** if you would like to change from the default cmip5 produced pr unit of mm/s to some other unit [ex. mm/h] \
# multiply here [ex. mm/h => model_pr*3600]
hrly_multiplier = 3600
model_pr = model_pr*hrly_multiplier

# testing points
test_point_1_after = model_pr[z_len, x_len, y_len]
test_point_2_after = model_pr[z_len//2, x_len//3, 0]
print('test point 1 value (after):', test_point_1_after, '\n', 'test point 2 value(after)', test_point_2_after, '\n'
    ' <<<"after" values should be ', hrly_multiplier, ' times larger than "before" values>>>')

# automated testing of points (within 5% uncertainty?)
pcnt_uncertainty_1 = 0.05 * test_point_1_after
pcnt_uncertainty_2 = 0.05 * test_point_2_after
if (test_point_1_after - pcnt_uncertainty_1) > (test_point_1_before*hrly_multiplier) > (test_point_1_after + pcnt_uncertainty_1):
    print('TEST POINT 1 RAISED INCORRECT VALUE: check code')
elif (test_point_2_after - pcnt_uncertainty_1) > (test_point_2_before*hrly_multiplier) > (test_point_2_after + pcnt_uncertainty_2):
    print('TEST POINT 2 RAISED INCORRECT VALUE: check code')
else:
    print('AUTOMATED TEST RETURNED POSITIVE: test points conform to expectation', '\n', 'for file ', output_file, '\n')

# write to new netcdf
print('beginning to write output for file: ', os.path.normpath(output_file))
writer = NetCDFWriter(output_file)
writer.create_time_variable("time", time, units=dataset.variables['time'].units)
writer.create_grid_variables(lats, lons)
# write precipitation variable, add comments or notes as needed
writer.create_data_variable("pr", ("time", "lat", "lon"), model_pr, units="mm h-1")
