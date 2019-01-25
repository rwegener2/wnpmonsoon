# WAS monsoon_index_hist.py ***
# calculate monsoon index using pr, ws, and wd and and output to a matrix of the same size marked by 1 as monsoon and
# 0 as not monsoon (Jan 1 2030 all blank)

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
clip = "extclip"
if clip == "extclip":
    num_days = int(2196)
else:
    num_days = int(2754)

## open all files
pr_file = "/snfs1/users/nasa_develop/projections/monsoon/JJAS_pr_hrly_day_ACCESS1-0_historical_r1i1p1_1988-2005_"+clip+".nc"
ws_file = "/snfs1/users/nasa_develop/projections/monsoon/JJAS_ws_adj_day_ACCESS1-0_historical_r1i1p1_1988-2005_"+clip+".nc"
wd_file = "/snfs1/users/nasa_develop/projections/monsoon/JJAS_wd_adj_day_ACCESS1-0_historical_r1i1p1_1988-2005_"+clip+".nc"

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
                # if model_wd[k,i,j] > int(wd_min) and model_wd[k,i,j] < int(wd_max) and model_pr[k,i,j] > 0 and model_pr[(k-1),i,j] > 0:
                if model_wd[k,i,j] > int(wd_min) and model_wd[k,i,j] < int(wd_max) and model_wd[(k-1),i,j] > \
                        int(wd_min)and model_wd[(k-1),i,j] < int(wd_max) and model_wd[(k-2),i,j] > int(wd_min) \
                        and model_wd[(k-2),i,j] < int(wd_max) and model_wd[(k-3),i,j] > int(wd_min) \
                        and model_wd[(k-3),i,j] < int(wd_max) and model_wd[(k-4),i,j] > int(wd_min) \
                        and model_wd[(k-4),i,j] < int(wd_max):
                    index[k, i, j] += 1
                    if index[(k-1), i, j] == 0:
                        index[(k-1), i, j] = 1
                    if index[(k-2), i, j] == 0:
                        index[(k-2), i, j] = 1
                    if index[(k-3), i, j] == 0:
                        index[(k-3), i, j] = 1
                    if index[(k-4), i, j] == 0:
                        index[(k-4), i, j] = 1

sum_ = np.zeros((model_wd.shape[1],model_wd.shape[2]))

sum_ = index.sum(0)
print(sum_.shape,"sum shape")

## write out new file
writer = NetCDFWriter("/snfs1/users/nasa_develop/projections/monsoon/MI_hist_raw_cnt_"+clip+"_wd_5day.nc")
#writer.create_time_variable("time",time_,units=dataset_pr.variables['time'].units)
writer.create_grid_variables(lat,lon)
writer.create_data_variable("yrly_freq",("lat","lon"),sum_,units="boolean monsoon")

end = time.time()
print("total run time is",(end-start),"seconds, ",(end-start)/60,"minutes")