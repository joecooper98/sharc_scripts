#!/usr/bin/python

import numpy as np


filename="collected_data_1_2_0_sy_cX.type3.txt"

pivot=180. # last allowed value - eck the sign in the finding of the pivot index!!!

abovequestionmark=True


data=np.genfromtxt(filename)

times=data[:,0]

numberofbins=np.count_nonzero(times==0.)

numberofsteps=int(times[-1]*2+1) # will only work for 0.5fs steps. if others needed, count number of unique times.

firststep=data[:numberofbins,:]

pivotindexprim=np.count_nonzero(firststep[:,1]<pivot)-1 # last point below pivot


for j in range(numberofsteps):
    pivotindex=numberofbins*j+pivotindexprim
    if abovequestionmark==True:
        for i in range(min(pivotindexprim,numberofbins-pivotindexprim)-1):
            data[pivotindex+i+1,2]+=data[pivotindex-i,2]
            data[pivotindex-i,2]=0.
    elif not abovequestionmark:
        for i in range(min(pivotindexprim,numberofbins-pivotindexprim)-1):
            data[pivotindex-i,2]+=data[pivotindex+i+1,2]
            data[pivotindex+i+1,2]=0.

fout=open("out.out", 'a')

for i in range(np.shape(data)[0]):
    data[i,:].tofile(fout, sep='    ', format='%.6e')
    fout.write("\n")
    if (i+1)%numberofbins==0:
        fout.write("\n")

