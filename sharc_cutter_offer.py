#!/usr/bin/env python3


# SHARC trajectory cut-off-er
# This script goes into a SHARC directory, and then finds the first time where
# the energy gap between the current state and a defined 'ground' state is less
# than a set threshold. After that, it alters the output.xyz and output.dat
# 
# use command 
# for i in `ls -d */`; do cd $i ; ./thisscript.py ; $SHARC/data_extractor.x newoutput.dat ; cd .. ; done 
#
# this requires that you've already run $SHARC/data_extractor.x - if you haven't, do, or uncomment the first os.system command
# this will print the changed output to files called newoutput.dat and newoutput.xyz - imaginatively corresponding to output.dat and output.xyz respectively
#
# according to the source code of SHARC (from mar 21), the output.dat file is the only file that is needed to generate the data - the .lis and .log files are purely for humans
#
# Will only work with a BASH-like operating system (I think also will work with z-shell)

import os
import numpy as np

#os.system("$SHARC/data_extractor.x output.dat")

energy_threshold = 0.15 # eV - the smallest allowed energy between occupied and ground state

no_atoms=9  # I assume this is fairly self-explanatory... change to number of atoms of your molecule

step_time = 0.5 # fs - fairly standard value, but change if needed.


energy_file="output_data/energy.out" #  the spin data for each step

spin_file="output_data/spin.out" # the spin data for each step

energy_data=np.genfromtxt(energy_file, skip_header=3) # parse data

spin_data=np.genfromtxt(spin_file, skip_header=3) # parse data


print("Threshold = "+str(energy_threshold)+" eV") # for checking...

for i in range(np.shape(energy_data)[0]): # for each time step
    state_number = np.argmax(spin_data[i,2:]<1)+1 # The state to which we cannot get close - this finds the lowest energy state of 2S less than 1 - i.e. S_0
    if energy_data[i,2]-energy_data[i,state_number+3] < energy_threshold: # if the current potential energy (i.e. the current state's energy) is closer than energy_threshold eV away from S_0
        print("Time that energy is below threshold = " + str(energy_data[i-1,0])+" fs") # print time
        time_break=energy_data[i,0] # time is gets to that condition - this is the FIRST timestep we DON'T want
        break
    

step_number=int(time_break/step_time + 1) # the step number of that state


os.system("k=`grep -n  '! 0 Step' output.dat | head -n"+ str(step_number) +" | tail -n1 | cut -d':' -f1` ; head -n`expr $k - 1` output.dat > newoutput.dat") # finds the point in the .dat file whence we don't want, and deletes all lines after
os.system("head -n"+str((step_number-1)*(no_atoms+2))+" output.xyz > newoutput.xyz") # deletes all geometries we don't want
#os.system("$SHARC/data_extractor.x newoutput.dat") # uncomment if you want to run the command from this script
