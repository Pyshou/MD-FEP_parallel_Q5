#!/bin/csh -f
# Jens Carlsson 2010
# Generates OPLSAA 2005 force field file for HETATM using Maestro

if ($#argv != 1) then
    echo "--------------------------------------------------------------------"
    echo "Extracts OPLS-AA parameters for a small molecule in a mol2 file.    "
    echo "The pdb file has to to have hydrogens                               "
    echo " "
    echo "USAGE:  plop_ff_params.csh file.mol2 "
    echo "--------------------------------------------------------------------"
else

	set SCHRUTIL = /software/sse/easybuild/prefix/software/Schrodinger/2018-3-nsc1/utilities
	$SCHRUTIL/mol2convert -imol2 $1 -omae $1:r.mae
	$SCHRUTIL/hetgrp_ffgen 2005 $1:r.mae
	$SCHRUTIL/pdbconvert -imae $1:r.mae -opdb $1:r_out.pdb
	$SCHRUTIL/mol2convert -imae $1:r.mae -omol2 $1:r_out.mol2

endif
