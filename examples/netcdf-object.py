from wnpmonsoon.netcdfdata import NetcdfData
from wnpmonsoon.wind_direction import wind_direction

folder = r"C:\repos\luigi-database\preprocessing_cmip5\spatial_subset\ACCESS1-0"
precip_test_file = folder + r"\pr_day_ACCESS1-0_rcp85_r1i1p1_20060101-21001231_spatial_clip.nc"
uas_test_file = folder + r"\uas_day_ACCESS1-0_rcp85_r1i1p1_20060101-21001231_spatial_clip.nc"
vas_test_file = folder + r"\vas_day_ACCESS1-0_rcp85_r1i1p1_20060101-21001231_spatial_clip.nc"

precip_access0 = NetcdfData(precip_test_file, 'pr')

# convert precip units
precip_access0.pr_unit_conversion()

# write out unit converted data
# precip_miroc.write(folder + r"\unit_conversion" + "\pr_day_MIROC5_rcp85_r1i1p1_203001-20391231_mm_day.nc")

# define uas and vas
uas_access0 = NetcdfData(uas_test_file, 'uas')
vas_access0 = NetcdfData(vas_test_file, 'vas')

wd_access0 = wind_direction(uas_access0, vas_access0)
