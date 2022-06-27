from tqdm import tqdm
import os

os.makedirs('molecules', exist_ok=True)

mole_lis = []
with open('XXX_AA1.pdb', 'r') as f:
    first_line = f.readline()
    mole_i = []
    line_i = f.readline()
    while line_i:
        if line_i[:3] == 'END':
            break
        if line_i[:3] == 'TER':
            mole_lis.append(mole_i)
            mole_i = []
        elif line_i[:3] == 'ATO':
            mole_i.append(line_i)
        line_i = f.readline()
for i in tqdm(range(len(mole_lis))):
    with open(f'molecules/mole_{i}.pdb', 'w') as f:
        mole_i = mole_lis[i]
        f.write(first_line)
        for line in mole_i:
            f.write(line)
os.makedirs('molecules_MARTINI', exist_ok=True)
with open('MARTINI.bash', 'w') as f:
    for i in range(len(mole_lis)):
        f.write(f'martinize2 -f molecules/mole_{i}.pdb -nt -o molecules_MARTINI/PROA_{i}.top -ff martini3001 -x molecules_MARTINI/mole_{i}.pdb\n')


