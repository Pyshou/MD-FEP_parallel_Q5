# Alternatively, go to https://github.com/esguerra/q6 (this is another more recent, stable version)
mkdir qsource_test_13018
cd qsource_test_13018
git clone https://github.com/qusers/qsource.git --branch testing/akesandgren --single-branch qakesandgren
cd Q5
git fetch
git checkout bugfix
git pull
cd src
module load intel/17.0.4.196
module load impi/5.1.3
make mpi COMP=ifort
make all COMP=ifort
# In the ff/oplsaam2015/ folder, make sure you have the correct parameters for arginine's C302 atom type
# and no van der Waals for polar hydrogens of TIP3P waters ("HT")
# You can get the corrected parameters using the 3_get_lig_ff_params/oplsaam2015/qoplsaa.prm file found in this repository.
