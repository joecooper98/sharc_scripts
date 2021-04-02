#!/usr/bin/env python3

# The problem of finding the angle between a plane and a vector is the same as finding the angle between two vectors, one normal to the plane and the vector that we can to analyse
# This script does this.
# The notation is thus  - central point is the point common to both the vector the plane (if there is more than one point which does this, your vector is a sub-space of the plane or you are very non-euclidean)
#                       - vector point is the other point of the vector (i.e. the non planar atom)
#                       - plane points are the two opther atoms which define the plane
#
# Use
# $ split -d  --a4 -l(no_of_atoms) output.xyz
# $ for i in `ls x????`: do ./plane_angle_finder.py $i >> output.out ; done



import numpy as np
import sys

filename=sys.argv[1]

f = open(filename, 'r')

s=f.readlines()


geom=np.genfromtxt(filename, skip_header=2,usecols=(1,2,3))

cpa=4
vpa=8
pp1a=0
pp2a=3

def vec_pla_ang(central_point, vector_point, plane_point_1, plane_point_2):

    def norm(vector):
        if np.size(vector)!=3:
            print("Not a three vector!")
        else:
            return np.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

    p_v_1 = central_point - plane_point_1 # defines a vector that is on the plane
    p_v_2 = central_point - plane_point_2 #  defines a vector that is on the plane

    b_v = vector_point - central_point # this is effectively the bond vector

    plane_vector=np.cross(p_v_1,p_v_2) # this finds the vector that defines the plane.
    normbv=norm(b_v)
    normpv=norm(plane_vector)
    scaled_dot_prod=np.dot(plane_vector, b_v)/(normbv*normpv)
    radangle=np.arccos(scaled_dot_prod)
    angle=np.rad2deg(radangle)

    if angle<90:
        newangle=angle+90
    elif angle>90:
        newangle=270-angle

    return newangle

print("    ", s[1].split()[1], "       ", vec_pla_ang(geom[cpa,:],geom[vpa,:],geom[pp1a,:],geom[pp2a,:]))
