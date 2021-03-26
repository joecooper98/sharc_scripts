#!/usr/bin/env python3


# SHARC trajectory cut-off-er
# This script goes into a SHARC directory, and then finds the first time where
# the energy gap between the current state and a defined 'ground' state is less
# than a set threshold. After that, it alters the output.xyz and output.dat
# 
# use command 
# for i in `ls -d */`; do cd $i ; ./thisscript.py ; $SHARC/data_extractor.x newoutput.dat ; cd .. ; done 

import os
import numpy as np

energy_threshold = 0.15 # eV - the smallest allowed energy between occupied and ground state

no_atoms=9

step_time = 0.5


energy_file="output_data/energy.out"

spin_file="output_data/spin.out"

energy_data=np.genfromtxt(energy_file, skip_header=3)

spin_data=np.genfromtxt(spin_file, skip_header=3)

print("Threshold = "+str(energy_threshold)+" eV")

for i in range(np.shape(energy_data)[0]):
    state_number = np.argmax(spin_data[i,2:]<1)+1 # The state to which we cannot get close
    if energy_data[i,2]-energy_data[i,state_number+3] < energy_threshold:
        print("Time that energy is below threshold = " + str(energy_data[i-1,0])+" fs")
        time_break=energy_data[i,0]
        break
    

step_number=int(time_break/step_time + 1)


os.system("k=`grep -n  '! 0 Step' output.dat | head -n"+ str(step_number) +" | tail -n1 | cut -d':' -f1` ; head -n`expr $k - 1` output.dat > newoutput.dat")
os.system("head -n"+str((step_number-1)*(no_atoms+2))+" output.xyz > newoutput.xyz")
#os.system("$SHARC/data_extractor.x newoutput.dat")