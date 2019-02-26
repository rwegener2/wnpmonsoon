## input data type: netcdf ; output = netcdf
## depends on netcdf writer module (netcdf.py must be in the same folder as this code while it runs)
## writen by Rachel Wegener (rachel.e.wegener@gmail.com)
# This code takes wind speed of size (34 lat x 34 lon x 10710 time) and makes it a new matrix of size (33 lat x 33 lon x 10710 time) by averaging together element i and i+1 along each row and each column (in the end four boxes are averaged together)

######## BEGINNING STEPS #############################
#####################################################

# import libraries
import numpy as np
import sys, os,glob, time
import netCDF4 as nc
from netcdf import NetCDFWriter

# start the all important timer
start = time.time()
# these variables do not affect the coordinate process, just the naming and finding of files
yr_strt = 1988
yr_end = 2005
period = "historical"

# select the file
ws_file = "/snfs1/users/nasa_develop/projections/monsoon/ws_day_ACCESS1-0_"+period+"_r1i1p1_"+str(yr_strt)+"0101-"+str(yr_end)+"1231_25clip.nc"
wd_file = "/snfs1/users/nasa_develop/projections/monsoon/wd_day_ACCESS1-0_"+period+"_r1i1p1_"+str(yr_strt)+"0101-"+str(yr_end)+"1231_25clip.nc"

# extract the data from the original netcdf files
dataset_ws = nc.Dataset(ws_file,'r')
dataset_wd = nc.Dataset(wd_file,'r')
model_ws = np.asarray(dataset_ws.variables["wind_speed"])
model_wd = np.asarray(dataset_wd.variables["wind_direction"])
	# wind speed -- 34 x 34 x 10710 matrix
lat = np.asarray(dataset_ws.variables["lat"][:])
	# lat - 34 length array
lon = np.asarray(dataset_ws.variables["lon"][:])
	# lon - 34 length array
time_ = np.asarray(dataset_ws.variables["time"])
	# time - 34 length array

########### CALCULATE NEW LATITUDE ##################
#####################################################
# create index
cnt = 0
# create stop variable so the last latitude element is ignored
stop = len(lat)-1
# predefine new matrix
latnew = np.full(((len(lat)-1),1),np.NaN)
# loop through each latitude
for lt in lat:
	# as long as we have not reached the last element
	if cnt != stop:
		# average together the two adjacent elements and save them in the place of the first one
		latnew[cnt] = (lat[cnt] + lat[int(cnt)+1])/2
		cnt +=1
	else:
		break

############## CALCULATE NEW LONGITUDE ###############
######################################################
# create index
cnt = 0
# create stop variable so the last longitude element is ignored
stop = len(lon)-1
# predefine new matrix
lonnew = np.full(((len(lon)-1),1),np.NaN)
# loop
for ln in lon:
        # as long as we have not reached the last element
	if cnt != stop:
		# average together the two adjacent elements and save them in the place of the first one
                lonnew[cnt] = (lon[cnt] + lon[int(cnt)+1])/2
                cnt +=1
        else:
                break

# reformat the new lat and long arrays so they can be properly rewritten later
latnew = np.array(latnew)
lonnew = np.array(lonnew)
latnew = latnew.flatten('C')
lonnew = lonnew.flatten('C')

###################### CREATE NEW WIND SPEED MATRIX #############
#################################################################
# predefine new matrix
wsnew = np.full(((model_ws.shape[0]),(model_ws.shape[1]-1),(model_ws.shape[2]-1)),np.NaN)
wdnew = np.full(((model_wd.shape[0]),(model_wd.shape[1]-1),(model_wd.shape[2]-1)),np.NaN)
# for each of the time elements (10710)
for k in range(model_ws.shape[0]):
#	print("processing ws data round 1 for k = ",k,"of 25932")
	# move through each latitude (34)
	for i in range(model_ws.shape[1]-1):
		# and each longitude (34)
		for j in range(model_ws.shape[2]-1):
			# and average together the four adjacent elements.  then put that number in the new matrix
			wsnew[k,i,j] = (model_ws[k,i,j] + model_ws[k,i,(j+1)]+model_ws[k,(i+1),j]+model_ws[k,(i+1),(j+1)])/4
			wdnew[k,i,j] = (model_wd[k,i,j] + model_wd[k,i,(j+1)]+model_wd[k,(i+1),j]+model_wd[k,(i+1),(j+1)])/4
