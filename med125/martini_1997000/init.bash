cp ../XXX_1997000.pdb XXX.pdb
cp ../martini/build.leap ./
cp ../martini/split.py ./

tleap -f build.leap
sed -i "s/HIE/HIS/g" XXX_AA1.pdb

python split.py 981

mkdir MARTINI_1by1
cp -r ../martini/MARTINI_1by1/MARTINI3_1.0 MARTINI_1by1/
cp -r ../martini/MARTINI_1by1/MARTINI3_1.1 MARTINI_1by1/
cp -r ../martini/MARTINI_1by1/mole_template MARTINI_1by1/
cp -r MARTINI_1by1/mole_template MARTINI_1by1/mole_all

source MARTINI.bash
cp ../martini/molecules_MARTINI/merge.py molecules_MARTINI/
cd molecules_MARTINI
python merge.py 20 _
cp mole_no__.pdb ../MARTINI_1by1/mole_all/mole_all.pdb

cd ../MARTINI_1by1/mole_all

sbatch med1_0715.sbatch



