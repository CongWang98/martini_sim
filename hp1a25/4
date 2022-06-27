import sys
import os
import math
import numpy
import MDAnalysis as mda
from MDAnalysis.lib.distances import distance_array

TPR='prod_0.tpr'
XTC='prod_0.xtc'
cut=10
eq=1001
nchain=47


def contact_mat(tpr_file,xtc_file,cutoff,start,nchain):
    u1=mda.Universe(tpr_file,xtc_file)

    # Read in trajectory and get COG
    protien = u1.select_atoms("all")
    N1 = int(len(protien) / nchain)
    L=len(u1.trajectory)
    inter_mat=numpy.zeros((N1,N1))
    intra_mat = numpy.zeros((N1, N1))

    AA={"TRP":0,"TYR":1,"PHE":2,"HIS":3,"LEU":4,"ILE":5,"MET":6,"VAL":7,"ALA":8,"CYS":9,"GLY":10,"PRO":11,"THR":12,"ASN":13,"SER":14,"GLN":15,"ARG":16,"LYS":17,"ASP":18,"GLU":19}

    count=0
    for ts in u1.trajectory:
        if ts.frame<start:
            pass
        else:
            print(ts.frame)
            box=u1.dimensions
            for i in range(0,nchain):
                for j in range(i, nchain):
                    # select atoms in chain i
                    index1=i*N1
                    index2 = ((i+1) * N1)
                    atoms1=u1.atoms[index1:index2]
                    # select atoms in chain j
                    index3 = j * N1
                    index4 = ((j + 1) * N1)
                    atoms2 = u1.atoms[index3:index4]
                    # calculate distances
                    dist_mat = distance_array(atoms1.positions, atoms2.positions, box)
                    # convert dist_mat to contact_mat
                    contact=numpy.where(dist_mat<cutoff, 1, 0)

                    if i==j: # Same dimer, intra_mat
                        intra_mat=intra_mat+contact

                    else: # other dimer, inter_mat
                        inter_mat = inter_mat + contact
            count=count+1

        # insert break for debugging
        #if count>1:
        #    break


    print(count)
    intra_mat=intra_mat / (count*nchain)
    inter_mat=inter_mat / (count*nchain)

    # matrix of contacts by AA type
    AA_mat=numpy.zeros((20,20))
    # for inter, divide into the frequency of AA contacts
    for i in range(0,N1):
        for j in range(i,N1):
            # get residues from sequence
            res1=u1.atoms.resnames[i]
            res2 = u1.atoms.resnames[j]
            # check sequence matches expectation
            #if i==0:
            #    print(res2)
            # convert resid to index of AA_mat
            index1=AA[res1]
            index2=AA[res2]
            if i==j:
                AA_mat[index1, index2] = inter_mat[i, j]
            else:
                # matrix should be symeteric (TYR-ARG is the same as ARG-TYR)
                AA_mat[index1,index2]=(inter_mat[i,j]+inter_mat[j,i])
                AA_mat[index2, index1] = (inter_mat[i, j] + inter_mat[j, i])
    # key with AA's
    key_string="TRP\t\t\tTYR\t\t\tPHE\t\t\tHIS\t\t\tLEU\t\t\tILE\t\t\tMET\t\t\tVAL\t\t\tALA\t\t\tCYS\t\t\tGLY\t\t\tPRO\t\t\tTHR\t\t\tASN\t\t\tSER\t\t\tGLN\t\t\tARG\t\t\tLYS\t\t\tASP\t\t\tGLU"


    return inter_mat,intra_mat,AA_mat,key_string


inter,intra,AAc,key_string=contact_mat(TPR,XTC,cut,eq,nchain)

numpy.savetxt('contacts_inter.txt',inter)
numpy.savetxt('contacts_intra.txt',intra)
numpy.savetxt('AA_contacts.txt',AAc,header=key_string)

