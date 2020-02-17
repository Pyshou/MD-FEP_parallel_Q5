#!/bin/csh
# Jens Carlsson 2012
# Preparation of jobs for paralell execution of FEP
# Modifieed by N. Panel for submission on beskow

# Options
if ($#argv < 1) then
    echo
    echo "paralell_FEP2.csh randomseed"
    echo
else

set randoms = $1

foreach file (input_files/dc*.inp)
	# Prepare each file in order
	set dir = $file:t:r
	echo "Preparing $dir"
	mkdir $dir
	cd $dir
		# 1. Copy data collection, equilibration, and submission files
		cp ../$file .
		cp ../input_files/eq*.inp .
		cp ../input_files/lig.fep .
		cp ../input_files/topology.top .
		# Set random seed in this run
		echo "Setting randomsseed to $randoms"
		sed -i "s/slumptal/${randoms}/g" eq*.inp
		# 2. Add specific lambda to equilibration files
		tail -2 $file:t > lambda_value
		foreach eq (eq*)
			cat $eq lambda_value >! eq_tmp
			mv eq_tmp $eq
		end
		# 3. Write path of the directory for submission
		echo $PWD >> ../../../dirlist
	cd ..
end
