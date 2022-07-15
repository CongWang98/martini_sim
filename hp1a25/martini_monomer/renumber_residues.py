import sys
import os
import math
import numpy

N=int(sys.argv[3])

old_file=sys.argv[1]
new_file=sys.argv[2]

old=open(old_file,'r')
new=open(new_file,'w')
line=old.readline()
while line:
    if line[0:4]=='ATOM':
        resid=int(line[22:27])
        resid2=resid%N
        if resid2==0:
            resid2=382
        resid2=str(resid2)
        while len(str(resid2))<4:
            resid2=str(' ')+resid2
        line2=line[0:22]+resid2+' '+line[27:len(line)]
        new.write(line2)
    else:
        new.write(line)
    line=old.readline()