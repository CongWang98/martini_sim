import sys
import mdtraj
import numpy as np
import math

pdb_file = sys.argv[1]
atom_index = int(sys.argv[2])

p = mdtraj.load(pdb_file)
xyz = p.xyz
print(xyz.shape)

atom_xyz = xyz[0][atom_index - 1]

dxyz = xyz[0] - atom_xyz

distance2 = (dxyz**2).sum(1)

argsort = distance2.argsort()

for i in range(10):
    min_i = argsort[i]
    print(min_i + 1, math.sqrt(distance2[min_i]), xyz[0][min_i])

