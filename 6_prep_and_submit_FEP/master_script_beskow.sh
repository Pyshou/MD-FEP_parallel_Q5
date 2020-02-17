#!/bin/bash -f
# Prepare and run FEP calculations

fep_scripts="/cfs/klemming/nobackup/p/pierrema/scripts/fep/"

for dir in $(ls -d REC/ WAT/);do
    cd $dir
    
    #Remove dirlist file
    if [ -e dirlist ]; then
        rm dirlist*
    fi

    wdir=$PWD
    for subdir in md_step0 md_step1_1 md_step1_2 md_step1_3; do
        echo "#### Preparing $dir $subdir"
        cd $subdir
        mkdir md_rs1 md_rs2 md_rs3
        cp -r input_files md_rs1
        cp -r input_files md_rs2
        cp -r input_files md_rs3
        cd md_rs1
        $fep_scripts/parallel_FEP2_beskow.csh 911
        cd ../md_rs2
        $fep_scripts/parallel_FEP2_beskow.csh 6600
        cd ../md_rs3
        $fep_scripts/parallel_FEP2_beskow.csh 660
        cd $wdir
    done
    bash $fep_scripts/make_submission_file_beskow.sh
    cd ..
done

