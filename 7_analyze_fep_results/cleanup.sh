#!/bin/bash

for folder in $(ls -d REC WAT)
do
        if [ "$folder" != "Phe_to_H_21A/" ]; then
                echo $folder
                rm $folder/md_step*/md_rs*/dc*/eq*.log
#               rm $folder/md_step*/md_rs*/*en # If using option 1 for analyzing the data
                gzip $folder/md_step*/md_rs*/dc*/dc*.log
                gzip $folder/md_step*/md_rs*/dc*/dc*.en
                for i in {0..5}
                do
                        rm $folder/md_step*/md_rs*/dc*/eq$i.re
                done
        fi
done

inp=$(pwd)
for fold in $(ls -d REC/md_step*/md_rs*/ WAT/md_step*/md_rs*/)
do
        cd $fold
        nb_dc=$(echo $(ls -d dc*/ | wc -l)-1 | bc)
        for i in $(seq 2 $nb_dc)
        do
                rm $inp/$fold/dc$i/dc$i.dcd
                rm $inp/$fold/dc$i/lig.fep
                rm $inp/$fold/dc$i/topology.top
                rm $inp/$fold/dc$i/eq*inp
        done
        cd $inp
done
