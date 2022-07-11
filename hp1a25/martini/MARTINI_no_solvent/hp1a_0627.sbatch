#!/bin/bash    
#SBATCH -N 1  
##SBATCH -n 16

#SBATCH -p sched_mit_binz_gpu
#SBATCH --time=48:00:00  
#SBATCH --exclusive
#SBATCH --mail-type=BEGIN, END
#SBATCH --mail-user=congwang@mit.edu

module unload cuda
module load gromacs/2018.4-gpu

#gmx_mpi solvate -cp XXX_MARTINI1.pdb -cs water.gro -o solvated.gro -p PROA.top -radius 0.21

#gmx_mpi grompp -f ions.mdp -c XXX_MARTINI1.pdb  -p PROA.top -o ions.tpr
#echo 13 | gmx_mpi genion -s ions.tpr -o start.gro -p PROA.top -pname NA -nname CL -conc 0.15 #-neutral

gmx_mpi grompp -f step4.1_minimization.mdp -c XXX_AMRTINI1.pdb -p PROA.top -o min.tpr
mpirun -np 1 gmx_mpi mdrun -deffnm min -dlb yes -maxh 191.9 -ntomp 5 -pin on -v 
# -nb gpu

gmx_mpi grompp -f step4.2_equilibration.mdp -c min.gro -p PROA.top -o nvt.tpr
mpirun -np 1 gmx_mpi mdrun -deffnm nvt -dlb yes -maxh 191.9 -ntomp 5 -pin on -v
#-nb gpu

gmx_mpi grompp -f step4.3_equilibration.mdp -c nvt.gro -t nvt.cpt -p PROA.top -o npt.tpr
mpirun -np 1 gmx_mpi mdrun -deffnm nvt -dlb yes -maxh 191.9 -ntomp 5 -pin on -v
#-nb gpu

gmx_mpi grompp -f step5.0_production.mdp -c npt.gro -t npt.cpt -p PROA.top -o prod.tpr
mpirun -np 1 gmx_mpi mdrun -deffnm prod -dlb yes -maxh 191.9 -ntomp 5 -pin on -v
#-nb gpu
