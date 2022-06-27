# MOFF->MARTINI Guide
By Andrew Latham and Bin Zhang
Please cite XXX

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
In this folder, we have the instructions to necessary to convert MOFF simulations to MARTINI

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
What you will need:
- STRIDE: Use the stide web interface to generate a secondary structure prediction from your input PDB (http://webclu.bio.wzw.tum.de/cgi-bin/stride/stridecgi.py)
- martinize2: install vermouth / martinize2 to help get MARTINI representations (https://github.com/marrink-lab/vermouth-martinize)
- GROMACS: used to run simulations (https://www.gromacs.org)
- AMBER: use ambertools to generate unrelaxed all-atom configurations (https://ambermd.org/AmberTools.php)
- completed MOFF simulations of the system. See our GitHub page (https://github.com/ZhangGroup-MITChemistry/MOFF)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Steps:
1. Convert MOFF trj file (XXX.xtc) into a single PDB (XXX.pdb) at a given time (ttt)
echo 0 0 | gmx_mpi trjconv -f eq3.xtc -s eq3.tpr -pbc mol -o XXX.pdb -center -b ttt -e ttt

2. Convert MOFF to initial all atom simulation using AMBERtools (in build.leap: XXX.pdb is the MOFF PDB, XXX_AA1.pdb is the all-atom PDB, and YYY  YYY YYY is the box size in angstroms, which should be taken from PDB file)
tleap -f build.leap

3. Convert XXX_AA1.pdb to MARTINI (may need many warnings, note that the topology will likely be incorrect at this step, but the PDB should be fine)
martinize2 -f XXX_AA1.pdb -nt -o PROA.top -ff martini3001 -x XXX_MARTINI1.pdb -maxwarn YYY

4. Remove all chains but 1 from XXX_AA1.pdb, rename this file XXX_AA2.pdb

5. Generate MARTINI with this single chain representation. This topology will be used in our simulations.
Note1: that secondary structure (-ss) should be used in many cases, and can be taken from the STRIDE analysis of the input configuration (often RaptorX) used by MOFF. For ELPs, we assumed random coil secondary structure.
Note2: elastic bonds (-elastic) should be used in ordered regions
martinize2 -f XXX_AA2.pdb -nt -o PROA.top -ff martini3001 -x XXX_MARTINI2.pdb

6. From steps 3 and 5, there are 2 files that are important:
#1 XXX_MARTINI1.pdb, the coordinate representation of the overall system
#2 Protein.itp, the topology of your single protein

7. Copy the MARTINI_template folder. This has all of the extra scripts necessary to run our simulations. Add XXX_MARTINI1.pdb to this folder.
Note: Here, we have options for 2 force fields. MARTINI3_1.0 is the default MARTINI3 force field. MARTINI3_1.1 is the MARTINI3 force field with water scaled by 1.1, as is suggested for IDPs by Thomasen et al. (https://pubs.acs.org/doi/10.1021/acs.jctc.1c01042)
Copy your Protein.itp to the MARTINI3_1.0 or MARTINI3_1.1, depending on which you plan to use

8. Edit these lines of PROA.top. Replace X with the scaling being used for the water. Make sure reference to the ion file matches with the modified (1.1) or unmodified (1.0) ions
#include "MARTINI3_1.X/martini3_W1.X.itp"
#include "MARTINI3_1.X/martini_v3.0_ions.itp"
#include "MARTINI3_1.X/Protein.itp"

9. Ensure protein is centered in the simulation box
gmx_mpi editconf -f XXX_MARTINI1.pdb -c -o XXX_MARTINI1.pdb -box  YYY YYY YYY

10. Solvate the protein in water
/home/gridsan/aplatham/Programs/gromacs-2021/bin/gmx_mpi solvate -cp XXX_MARTINI1.pdb -cs water.gro -o solvated.gro -p PROA.top -radius 0.21

10b. Add drug molecules. See gromacs insert-molecules

11. Add ions with Monte Carlo sampling
/home/gridsan/aplatham/Programs/gromacs-2021/bin/gmx_mpi grompp -f ions.mdp -c solvated.gro -p PROA.top -o ions.tpr
/home/gridsan/aplatham/Programs/gromacs-2021/bin/gmx_mpi genion -s ions.tpr -o start.gro -p PROA.top -pname NA -nname CL -conc 0.15

12. Run energy minimization
gmx_mpi grompp -f step4.1_minimization.mdp -c start.gro -p PROA.top -o min.tpr
mpirun -np 1 mdrun_mpi  -deffnm min -dlb yes -maxh 191.9 -ntomp 5 -pin on -nb gpu

13. Run nvt equilibration
gmx_mpi grompp -f step4.2_equilibration.mdp -c min.gro -p PROA.top -o nvt.tpr
mpirun -np 1 mdrun_mpi  -deffnm nvt -dlb yes -maxh 191.9 -ntomp 5 -pin on -nb gpu


14. Run npt equilibration
gmx_mpi grompp -f step4.3_equilibration.mdp -c nvt.gro -t nvt.cpt -p PROA.top -o npt.tpr
mpirun -np 1 mdrun_mpi  -deffnm nvt -dlb yes -maxh 191.9 -ntomp 5 -pin on -nb gpu

15. Run production
gmx_mpi grompp -f step5.0_production.mdp -c npt.gro -t npt.cpt -p PROA.top -o prod.tpr
mpirun -np 1 mdrun_mpi  -deffnm prod -dlb yes -maxh 191.9 -ntomp 5 -pin on -nb gpu
