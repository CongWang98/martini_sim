import mdtraj as md

file_lis= [f'mole_{i}.pdb' for i in range(47)]


mole_lis = [md.load(f) for f in file_lis]
