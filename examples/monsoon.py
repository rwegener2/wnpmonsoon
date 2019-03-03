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
precip_test_file_lin = os.path.join(folder, r"ACCESS1-3/pr_day_ACCESS1-3_rcp85_r1i1p1_1year_spatial_clip.nc")
uas_test_file_lin = os.path.join(folder, r"ACCESS1-3/uas_day_ACCESS1-3_rcp85_r1i1p1_1year_spatial_clip.nc")
vas_test_file_lin = os.path.join(folder, r"ACCESS1-3/vas_day_ACCESS1-3_rcp85_r1i1p1_1year_spatial_clip.nc")

# Generate precipitation rate
with nc.Dataset(precip_test_file_lin, 'r') as p_flux_reader:
    print(p_flux_reader.__class__)
    p_rate = NCdata.pr_rate_from_flux(p_flux_reader)
p_rate_path = os.path.join(folder, r"created/pr_from_flux_ACCESS1-3.nc")
# p_rate.write(p_rate_path)

# Generate wind direction
with nc.Dataset(uas_test_file_lin, 'r') as uas_reader, \
     nc.Dataset(vas_test_file_lin, 'r') as vas_reader:
    wdir = NCdata.wind_dir_from_components(uas_reader, vas_reader)
wdir_path = os.path.join(folder, r"created/wdir_ACCESS1-3.nc")
# wdir.write(wdir_path)

# Compute monsoon
criteria = criteria_generator(pr_min=5, wd_min=180, wd_max=270)

with nc.Dataset(p_rate_path, 'r') as pr_reader, \
     nc.Dataset(wdir_path, 'r') as wd_reader:
     output = MonsoonData.compute(pr_reader, wd_reader, criteria)

filepath = '/home/rwegener/repos/wnpmonsoon/tests/data/created/monsoon_index_access13_pr5plus_180270wd_nomask.nc'
# output.write(filepath)
src = nc.Dataset(filepath, 'r')
print(src.variables['monsoon'][:])

output.variable = output.variable*5

from wnpmonsoon.netcdf import NetCDFWriter
writer = NetCDFWriter(filepath)
writer.set_global_attributes(**output.globalattrs)
writer.set_global_attributes(model_id=output.model_id)
writer.create_time_variable("time", output.time, units=output.time_units, calendar=output.calendar)
writer.create_grid_variables(output.lats, output.lons)
writer.create_data_variable(output.var_name, ("time", "lat", "lon"), output.variable, units=output.var_units)
writer.set_always_mask(True)


# Testing opening an existing file
# filepath = '/home/rwegener/data/monsoon_test.nc'
# with nc.Dataset(filepath, 'r') as mi_reader:
#     new = MonsoonData(mi_reader)

# Found mistakes here:  (but I guess not?)
p_rate.variable[1, -1, -4:]
wdir.variable[1, -1, -4:]
output.variable[1, -1, -4:]

# Look at test slices
from matplotlib import pyplot as plt
slice = 7
plt.figure(0)
plt.imshow(wdir.variable[slice, :], cmap=plt.cm.get_cmap('Blues', 3), vmin=90, vmax=360)
plt.colorbar()
plt.show()

plt.figure(1)
plt.imshow(p_rate.variable[slice, :], cmap=plt.cm.get_cmap('Blues', 2), vmin=0, vmax=10)
plt.colorbar()
plt.show()

plt.figure(2)
plt.imshow(output.variable[slice, :])
plt.colorbar()
plt.show()
