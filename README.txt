🎬 To get start with SOMA, clone the repository found here: git@github.com:anl-ecucuzzella/compass.git. Follow provided instructions to set up perturbed parameter ensemble experiments.

🗂️ There are a few initial errors from the compass repository that might lead to errors if job scripts are submitted with the forwards configured as-is. These include:
1) clobber_mode in all streams.ocean files is set to 'overwrite' instead of 'truncate,' resulting in errors when restarting or rerunning experiments.
2) Results are set up to record at a daily interval instead of a yearly interval, which results in way too much data for processing.
Therefore, by running the Python scripts provided in setup_files (using the command "python3 editing_streams_xxxx.py"), you can avoid the issues outlined here. Just make sure that you are setting the range in each Python file to the number of forward runs you have available.

🚦 We wanted to collect the results of the SOMA simulation after three years of running; however, we did not need data from years one and two. Therefore, we needed to run a restart. After the restart, certain parameters need to be altered in the namelist.ocean and streams.ocean files in each of the forwards, namely:
1) The restart interval 
2) Where the restart was located
3) The starting input
4) The stopping time
By running the Python scripts provided in restart_files (using the command "python3 editing_XXXXX_XXXXX.py"), you can alter these conditions following the first two years of output. Just make sure that you are setting the range in each Python file to the range of forwards for which you already have two years of output.

📊 Finally, we want to be able to transform our data outputs in each forwards' output folder, saved as .nc files, in a format that is conducive to training. We chose to save our data in a .hdf5 file using the h5py package in Python. There is a lot of post-processing required in order to complete this transition, however. For starters, the data needs to be regrid. We used ncremap for this.
The first file in the data_postprocessing folder is from_mpas.py. Running "python3 from_mpas.py" and giving it one of the .nc output files will generate a scrip.nc file that ncremap can use for regridding. Then, calling "ncremap -g grd.nc -G latlon=100,100#snwe=21.0,49.0,-17.0,17.0 #lon_typ=grn_ctr" gets a grd.nc file. The scrip.nc file transforms every variable in the original output file to work with the new latitude and longitude grid; the grd.nc file sets up the exact dimensions of that grid. Generate one scrip.nc file and one grd.nc for your first output file before proceeding to the rest of the data postprocessing.
The next file in the data_postprocessing folder is DATAPREPROCESSINGFORTRAINING.py which combines all of the first months' outputs for each forward into a .hdf5 file after spatial interpolation procedures. This code is thoroughly documented. 
