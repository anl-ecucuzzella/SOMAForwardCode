import numpy as np
import netCDF4
import h5py
import os

#NAME: get_variables
#PURPOSE: to get the variables that are spatially and temporally varying
#We want only those that are spatially and temporally varying because we 
#want the variables that change throughout the whole grid and also 
#change over the course of a year.
#PARAMETERS: data which is the netCDF4 file 
#RETURNS: the list of variables of size (30, 60, 100, 100)
def get_variables(data):
	list_of_variables = []
	for v in list(data.variables.keys()):
		if data.variables[v][:].shape == (30, 60, 100, 100):
			list_of_variables.append(v)
	return list_of_variables

#NAME: get_GM
#PURPOSE: get the GM value for a particular forward because we need to
#include it in our dataset as it is the input for training.
#PARAMETERS: forward which is the number of the forward we care about
#RETURNS: the gm value for that particular forward
def get_GM(forward):
	os.chdir(f"output_{forward}")
	namelist = open("namelist.ocean")
	namelist_lines = namelist.readlines()
	gm = float(namelist_lines[81][31:-1])
	namelist.close()
	os.chdir("..")
	return gm

#NAME: populate_empty_array
#PURPOSE: to populate the array with the values for all of the different 
#variables that we care about, i.e. the ones that we found from 
#calling get_variables
#PARAMETERS: list_of_variables which is the result of calling 
#get_variables, data which is the netCDF4 file for a forward, and gm 
#which is the result of calling get_GM
#RETURNS: a numpy array that is of size (30, 60, 100, 100, 17) that 
#contains the data for each of the different variables that we care about
def populate_empty_array(list_of_variables, data, gm):
	all_the_data = []
	for v in list_of_variables:
		init = np.array(data.variables[v][:])
		reshaped_init = np.reshape(init, (30, 60, 100, 100, 1))
		all_the_data.append(reshaped_init)
	all_the_data.append(np.full((30, 60, 100, 100, 1), gm))
	return np.concatenate(all_the_data, axis = 4)

#NAME: find_max_depth_index
#PURPOSE: to figure out the index where the maximum depth of a particular
#spatial point is exceeded. This is necessary because past a certain 
#depth, some cells return NaNs.
#PARAMETERS: x and y which is the location of the point in question, data
#which is the netCDF4 data for a forward
#RETURNS: the index of the last vertical layer where data should exist 
#based on the layer thicknesses and maximum depths 
def find_max_depth_index(x, y, data):
	thickness = list(data.variables["refBottomDepth"][:])
	bottom = list(data.variables["bottomDepth"][:])[x][y]
	for t in range(len(thickness)):
		if bottom < thickness[t]:
			return t 
	return len(thickness) - 1

#open a hdf5 file to write the results to 
f = h5py.File("thedataset4.hdf5", "w")
for forward in range(100):
    #os.chdir(f"output_{forward}")
    #os.system("cp ../output_0/scrip.nc scrip.nc")
    #os.system("cp ../output_0/grd.nc grd.nc")
    #need to regrid each of the .nc files for a forward based on the 
    #scrip.nc and grd.nc files 
    #os.system("ncremap -P mpas -s scrip.nc -g grd.nc output.0003-01-01_00.00.00.nc output.0003-01-01_00.00.00-rgr.nc")
    #os.chdir("..")
    #currently just getting data for the first month for Yixuan's training 
    data = netCDF4.Dataset(f"output_{forward}/output.0003-01-01_00.00.00-rgr.nc")
    list_of_variables = get_variables(data)
    #grp = f.create_group("forward_" + str(forward))
    gm = get_GM(forward)
    result = populate_empty_array(list_of_variables, data, gm)
    for x in range(100):
    	for y in range(100):
    		t = find_max_depth_index(x, y, data)
    		if t != 59 and t != 60:
    			for t_ in range(t+1, 60):
    				result[:,t_,x,y] = np.zeroes(17)
    #create a dataset for each of the forwards 
    dset = f.create_dataset(f"forward_{forward}", result.shape, dtype = 'f', data = result)

