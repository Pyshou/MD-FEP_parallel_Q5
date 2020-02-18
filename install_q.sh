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
