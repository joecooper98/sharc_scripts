#!/bin/bash

no_of_atoms_plus_2=11

filename=output.xyz
outputfile=angles.out


split -d -a4 -l${no_of_atoms_plus_2} $filename

echo "#    t(fs)           plane angle(deg))" >> $outputfile
echo "#-------------------------------------" >> $outputfile

for i in `ls x????`
do
    ./plane_angle_finder.py $i >> $outputfile
done
