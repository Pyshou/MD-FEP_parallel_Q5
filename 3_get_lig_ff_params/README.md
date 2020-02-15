# Get OPLS ligand force field parameters

For each FEP, you will need the force field parameters of both the MD topology's ligand (usually the biggest) and of the one to compare it to. Prepare a force field folder for each compound of an MD/FEP transformation and do the following. You can preliminarily build and save a MOL2 file for your ligands using Chimera's Structure Editing Builder Tool ideally starting from a template structure (very convenient). Name the ligand residue "LIG" everywhere for compatibility with different scripts later.

PS. I would advice to run a few relevant retrospective predictions with already tested compounds to calibrate your MD/FEP protocol first (i.e. protonation states in the binding site, sphere size, simulation time..) and see if it allows to reproduce experimental binding affinities.


## **Option 1. Using ffld_server (accessible on CSB)**

```/home/apps/schrodinger2015/utilities/ffld_server -imol2 rec.mol2 -opdb rec.pdb -print_parameters > LIG.ffld``` # Use a rec.mol2 file for the compound to generate force field parameters for

```module load python/2.7.6```

```source /home/apps/qtools/0.5.11/qtools_init.sh```

```python2.7 /home/apps/qtools/0.5.11/qscripts-cli/q_ffld2q.py LIG.ffld rec.pdb -o LIG``` # Note that you can download and install qtools on your account from the following repository: https://github.com/mpurg/qtools .

- In the generated LIG.lib and LIG.prm files, change "lig." to "T" for compatibility with scripts later (juse use a sed..).
- Also just remove the header in the LIG.lib library file (starting with "#", not sure that Q likes that).
- All that and the following can be put in a script... .

```mkdir Forcefield```

```cp oplsaam2015/popc_hugo.lib Forcefield/``` # oplsaam2015 folder downloadable from here

```cp oplsaam2015/qoplsaa.lib Forcefield/Qoplsaa.lib```

```cp oplsaam2015/qoplsaa_withpopc.prm Forcefield/Qoplsaa.prm```

```mv LIG.lib Forcefield/```

```./jorgensen_to_Q.py Qoplsaa.prm LIG.prm``` # Merge with the new protein force field

```mv Qoplsaa_2.prm Forcefield/Qoplsaa.prm``` # Replace old by merged force field

```rm LIG.prm``` # Optional, not needed anymore

## **Option 2. Using hetgrp_ffgen (still accessible on Tetralith, at least on Pierre's account)**

```module load Schrodinger/2018-3-nsc1```

- Use the following enclosed script:

```./get_ff_parameters.csh rec.mol2```

```./extract_ff_parameters.pl lig```

- in LIG.lib, change 'lig' to 'LIG' in first line and change charge_groups content to a single horizontal line
- Modify zero masses to the good ones in NBON.prm
- Remove columns of floating numbers 2 and 4 in IPHI.prm (only a force constant and equilibrium angle should remain)

```mkdir Forcefield``` # Will merge with the oplsaam2015 protein force field (can put those line in a script om du vill..)

```cp oplsaam2015/popc_hugo.lib Forcefield/``` # oplsaam2015 folder downloadable from here

```cp oplsaam2015/qoplsaa.lib Forcefield/Qoplsaa.lib```

```cp oplsaam2015/qoplsaa_withpopc.prm Forcefield/Qoplsaa.prm```

```mv LIG.lib Forcefield/```

```cat NBON.prm BOND.prm THET.prm PHI.prm IPHI.prm  > Qoplsaa.prm``` # New Qoplsaa.prm file !

```./oplsaa2005_to_oplsaam2015.py Forcefield/Qoplsaa.prm Qoplsaa.prm```

```mv Qoplsaa_2.prm Forcefield/Qoplsaa.prm```

```rm BOND.prm IPHI.prm lig NBON.prm PHI.prm PRM rec.mae rec_out.mol2 THET.prm Qoplsaa.prm``` # Cleaning up et voila!

## **Complementary Option. Using improved force field parameters (LigParGen)**

Go to http://zarbi.chem.yale.edu/ligpargen/index.html . For Q (as other MD engines), this can generate a ligand force field library file as well as paramterers to insert in your "Qopplsaa.prm" force field file. But do not use it until they have fix the problem of wrongly multiplied force constants for bonded parameters for Q (which might also be why they haven't benchmarked their energies with Q in their paper). 

What you can eventually do though is to use better quality **partial charges** by translating the information from the generated "LIG.lib" file (especially if you will carry out transformations of heterocycles, atypical chemical moieties or do scaffold hopping/optimization in general). These partial charges have been used in combination with OPLSAA-2005 by Jorgensen before.

- After generating a force field from option 1 or 2, go to the webserver and use 1.14\*CM1A-LBCC charges if there are not charged ligands in your series and note that the resulting partial charges from electrostatic potential fit will be dependent on the provided conformation of the uploaded ligand. Before the next step, make sure the LigParGen PDB (that you can download from the OpenMM "result" section) matches the coordinates of your initial PDB (if not, use the Wizzard pair fitting tool and editing mode for torsions in PyMOL to sumperimpose, match and save the new structure). Also download the generated QLIB file in the Q section. And run:

```./prep_mapping_files_ligpargen2Q.py rec.pdb LIG.pdb 0.2``` # rec.pdb being the initial structure and LIG.pdb the one generated by LigParGen. Here using an 0.2 Angstroms distance treshold to define atoms as identical for sure. Check the generated mapping_ligpargen2Q.txt mapping file (minimal distances beyond that treshold will generate guessed atom names followed by "?", so correct or remove these characters if correct), and run:

```./ligpargen2Q_charges.py LIG.lib LIG_prgn.lib N9``` # LIG.lib is a library obtained from the above procedure (option 1 or 2) and LIG_prgn.lib the one form LigParGen. This generates a LIG_new.lib file with new partial charges and original atom names (replace the old one by it then).


**Torsion Scans**

If you have rotabable bonds attached to atypical heterocycles for instance, you might have improperly described torsional terms in the original force field, which covers only a tiny fraction of chemical space. This could just kill your results by sampling wrong and largely penalizing orientations for the FEPed moieties (have a look at https://www.nature.com/articles/s41598-017-04905-0). Improvements should be seen in the costly OPLS3 force field from Scrhodinger (or the new LigParGen parameters which are not fixed for Q yet though). If you want to check and reparametrize key torsions for some substituents on a particular position (in control MD/FEP calculations?), then go to the Torsion_Scan folder of this repository.
