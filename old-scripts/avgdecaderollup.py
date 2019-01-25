# WAS monsoon_indx_hist_sum.py
## calculate monsoon index using pr, ws, and wd and and output to a matrix of the same size marked by 1 as monsoon and 0 as not monsoon (Jan 1 2030 all blank)

## import libraries ##
import numpy as np
import netCDF4 as nc
import sys, os, glob, time
from netcdf import NetCDFWriter
from netCDF4 import num2date
import datetime
from datetime import date

start = time.time()

yr_strt = 1988
yr_end = 2005
period = "historical"
clip = "25clip"
if clip == "extclip":
	num_days = int(2196)
else:
	num_days = int(2754)

## open all files
pr_file = "/snfs1/users/nasa_develop/projections/monsoon/JJASO_pr_hrly_day_ACCESS1-0_historical_r1i1p1_1988-2005_"+clip+".nc"
ws_file = "/snfs1/users/nasa_develop/projections/monsoon/JJASO_ws_adj_day_ACCESS1-0_historical_r1i1p1_1988-2005_"+clip+".nc"
wd_file = "/snfs1/users/nasa_develop/projections/monsoon/JJASO_wd_adj_day_ACCESS1-0_historical_r1i1p1_1988-2005_"+clip+".nc"

wd_min = "180"
wd_max = "270"

dataset_pr = nc.Dataset(pr_file,'r')
dataset_ws = nc.Dataset(ws_file,'r')
dataset_wd = nc.Dataset(wd_file,'r')

model_pr = np.asarray(dataset_pr.variables["pr"])
model_ws = np.asarray(dataset_ws.variables["wind_speed"])
model_wd = np.asarray(dataset_wd.variables["wind_direction"])

time_ = np.asarray(dataset_pr.variables["time"])
lat = np.asarray(dataset_pr.variables["lat"])
lon = np.asarray(dataset_pr.variables["lon"])


## create blank output counter ##
index = np.zeros((model_pr.shape[0],model_pr.shape[1],model_pr.shape[2]))

## set conditions to create index
for k in range(1,model_pr.shape[0]):
	dtk1 = num2date(time_[k],"days since 1988-01-01",calendar = 'proleptic_gregorian')
       	dtk0 = num2date(time_[(k-1)],"days since 1988-01-01",calendar = 'proleptic_gregorian')
       	if dtk1.year == dtk0.year:
		for j in range(model_pr.shape[2]):
			for i in range(model_pr.shape[1]):
				if model_wd[k,i,j] > int(wd_min) and model_wd[k,i,j] < int(wd_max) and model_pr[k,i,j] > 0 and model_pr[(k-1),i,j] > 0:
					index[k,i,j] += 1
					if index[(k-1),i,j] == 0:
						index[(k-1),i,j] == 1

## create yearly sums
y_range = ["88","89","90","91","92","93","94","95","96","97","98","99","00","01","02","03","04","05"]
cnt_y_ran = 0
yearly_days = np.zeros((18,model_pr.shape[1],model_pr.shape[2]))
for y in y_range:
	print("processing for y range ",y)
	for k in range(model_pr.shape[0]):
       		dtk0 = num2date(time_[(k)],"days since 1988-01-01",calendar = 'proleptic_gregorian')
		year = str(dtk0.year)
        	if year[2:4] == str(y):
			yearly_days[cnt_y_ran] = yearly_days[cnt_y_ran] + index[k]
	cnt_y_ran += 1

print("final cnt_y_range",cnt_y_ran,"---should be 17")
## calculate average number of days per year from the yearly frequency sums
avg_days_per_year = (yearly_days.sum(0) / 18)
print("maximum value of average days per year is",avg_days_per_year.max())
perc_mon = (index.sum()/(21*33*num_days))*100
print("percent monsoon",perc_mon)

## write out new file
writer = NetCDFWriter("/snfs1/users/nasa_develop/projections/monsoon/MI_hist_yrly_avg_freq_"+clip+".nc")
#writer.create_time_variable("time",time_,units=dataset_pr.variables['time'].units)
writer.create_grid_variables(lat,lon)
writer.create_data_variable("yrly_freq",("lat","lon"),avg_days_per_year,units="average number of days per year that registered as monsoon")

end = time.time()
print("total run time is",(end-start),"seconds, ",(end-start)/60,"minutes")