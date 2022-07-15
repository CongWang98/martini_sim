import mdtraj as md
import os
import sys 

N = int(sys.argv[1])
#output_file = sys.argv[2]
#mole_file_lis = [f for f in os.listdir('./') if f.split('.')[-1] == 'pdb']

#bad_lis = ['2', '14', '19', '20','21', '22', '35', '41', '42']
bad_lis = []
mole_file_lis = [f'mole_{i}.pdb' for i in range(N) if str(i) not in bad_lis]
#mole_file_lis.sort()
mole_lis = [md.load(f) for f in mole_file_lis]
print(f'{len(mole_lis)} pdb files loaded')
print(mole_file_lis)
mole_all = mole_lis[0]
for i in range(len(mole_lis) - 1):
    mole_all = mole_all.stack(mole_lis[i + 1])
print(mole_all)
mole_all.save(f'mole_no_{"_".join(bad_lis)}.pdb')

