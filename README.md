# sharc_scripts

The script takes the output from a SHARC surface hopping calculation and cuts off the simulation when the energy between S_0 and the current state gets lower than a set threshold energy. 

It accomplishes this by considering the potential energy at the current time step, which in surface hopping is the energy of the current state.

To compare this with S_0, we look at the data in the spin.dat file, which contains the number of unpaired spinds for each diagonal state (or whatever that means in the "diagonal" representation). The one with S<1 (it's actually rather close to the MCH state in the tested case) and the lowest energy (or rather the leftmost state in the spin.dat file with spin under 1) is considered to be the S_0, or the state that the excited states (in both TDDFT and ADC2) can't get close to.

In future I could fairly easily generalise this to the MCH representation, but the option to change that is already available in SHARC on performing the trajectories.

The script finds this time step, and then alters the output.log and output.xyz file to remove the steps from that point forward. You can then use SHARC's built in data extractor to regenerate the data for plotting.
