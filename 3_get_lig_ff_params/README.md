# Get OPLS ligand force field parameters

For each FEP, you will need the force field parameters of both the MD topology's ligand (usually the biggest) and of the one to compare it to. Prepare a force field folder for each compound of an MD/FEP transformation (called like ff.lig.YOURLIGNAME, convenient for scripts in next steps) and do the following. You can preliminarily build and save a MOL2 file for your ligands using Chimera's Structure Editing Builder Tool ideally starting from a template structure (very convenient). Name the ligand residue "LIG" everywhere for compatibility with different scripts later.

PS. I would advice to run a few relevant retrospective predictions with already tested compounds to calibrate your MD/FEP protocol first (i.e. protonation states in the binding site, sphere size, simulation time..) and see if it allows to reproduce experimental binding affinities.

Use one of the following options and always the same for the same project (as you will see later, seperate scripts that map forcefield parameters of two liands have been made as the markers/comments in force field files differ and are needed)! Note that the force field parameters are the same if you are using ffld_server with the default version (14) as here.


## **Option 1. Using ffld_server (accessible on CSB)**

```/home/apps/schrodinger2015/utilities/ffld_server -imol2 rec.mol2 -opdb rec.pdb -print_parameters > LIG.ffld``` # Use a rec.mol2 file for the compound to generate force field parameters for

```module load python/2.7.6```

```source /home/apps/qtools/0.5.11/qtools_init.sh```

```python2.7 /home/apps/qtools/0.5.11/qscripts-cli/q_ffld2q.py LIG.ffld rec.pdb -o LIG``` # Note that you can also download and install qtools from the following repository: https://github.com/mpurg/qtools .

- In the generated rec.pdb ligand coordinate file, check that all atom names are properly columned (i.e. not shifted when there are like 4 characters). Make sure that your residue name is "LIG" (needed later with scripts). And also cleanup the PDB that will be used to generate topologies with Q (i.e. ligands in water), using the following:

```./cleanup_LIGpdb4Q.pdb rec.pdb``` # Then replace old by the generated rec_clean.pdb file

- In the generated LIG.lib and LIG.prm files, change "lig." to "T" for compatibility with scripts later (juse use a sed..).
- Also just remove the header in the LIG.lib library file (starting with "#", not sure that Q likes that).
- And make sure the charge group section in the LIG.lib file starts with a heavy atom.
- Then, all that and the following can be put in a script... .

```mkdir Forcefield```

```cp oplsaam2015/popc_hugo.lib Forcefield/``` # oplsaam2015 folder downloadable from here

```cp oplsaam2015/qoplsaa.lib Forcefield/Qoplsaa.lib```

```cp oplsaam2015/qoplsaa_withpopc.prm Forcefield/Qoplsaa.prm```

```mv LIG.lib Forcefield/```

```./jorgensen_to_Q.py Qoplsaa.prm LIG.prm``` # Merge with the new protein force field

```mv Qoplsaa_2.prm Forcefield/Qoplsaa.prm``` # Replace old by merged force field

```rm LIG.prm``` # Optional, not needed anymore


## **Option 2. Using hetgrp_ffgen (still accessible on Tetralith, at least on Pierre's account)**

This option might be convenient for amino acid FEPs as you will have charge groups defined for the compound (you will see later).

```module load Schrodinger/2018-3-nsc1```

- Use the following enclosed script:

```./get_ff_parameters.csh rec.mol2```

```./extract_ff_parameters.pl lig```

- In the generated rec.pdb ligand coordinate file, check that all atom names are properly columned (usually shifted when there are like 4 characters). Make sure that your residue name is "LIG" (needed later with scripts). And also cleanup the PDB that will be used to generate topologies with Q (i.e. ligands in water), using the following:

```./cleanup_LIGpdb4Q.pdb rec.pdb``` # Then replace old by the generated rec_clean.pdb file

- in LIG.lib, change 'lig' to 'LIG' in first line and change charge_groups content to a single horizontal line unless you are doing amino acid FEPs and make sure the charge group section starts with a heavy atom.
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

```./ligpargen2Q_charges.py LIG.lib LIG_prgn.lib N9``` # LIG.lib is a library obtained from the above procedure (option 1 or 2, likely in the corresponding "Forcefield/" folder) and LIG_prgn.lib the one form LigParGen. The "N9" atom is here the name of a burried atom I wanted to offset by minus the residual charge by in order to neutralize my compound. This generates a LIG_new.lib file with new partial charges and original atom names (replace the old one by it then).


## **Torsion Scans**

If you have rotabable bonds attached to atypical heterocycles for instance, you might have improperly described torsional terms in the original force field, which covers only a tiny fraction of chemical space. This could just kill your results by sampling wrong and largely penalizing orientations for the FEPed moieties (have a look at https://www.nature.com/articles/s41598-017-04905-0). Improvements should be seen in the costly OPLS3 force field from Scrhodinger (or the new LigParGen parameters which are not fixed for Q yet though). If you want to check and reparametrize key torsions for some substituents on a particular position (in control MD/FEP calculations?), then check the following.

Ideally, use a fragment "tool" compound representing your molecular scaffold with the attached moiety you want to scan a torsion for. This will be faster, avoid crashes and potential clashes during the scan as well.

- On Tetralith via Thinlinc or GUI / ssh -X:

```module load gaussian/G09RevE.01-bdist```

- Edit a .com file using the one enclosed as template, with the atoms and coordinates of you compound PDB instead, with the torsion atoms in order within the 4 first lines for convenience later.

- Also adjust the basis set if needed as well as the overall charge of the system and the overall spin multiplicity ("0 1" in my case).

- Open the viewer:

```gview```

- Open your LIG_cartesian.com with and check the structure as well as torsion atom indices.

- Save a new Gaussian input LIG.com file (uncheck the "cartesian" option) and use the header of the old file!

- Check that torsion atoms in order are 1, 2, 3 and 4 respectively

- In the last block, identify the line starting with "D1" (torsion 1), check the starting angle value and at the end of the line, add "  S 18 10.0", for instance if rotating 18 times by 10 degrees (symmetric molecule, I would advise a full rotation to double check symmetry in the scan though). Also leave two blank lines at the end of the file.

- Then use the enclosed submission script on Tetralith.

- When done, you can open the output (LIG.out file) with gview, check structures and save the scan data. Also save each structure (see below).

- Converts the energies from Hartree to kcal/mol and offset by the minimum (will become zero). 

- Generate a Q topology for each saved structure in vaccuum (don't use solvate with qprep!). 

- Run a short, close to 0 K simulation in Q for each point with atoms tightly restrained to their initial coordinates. 

- Get the total potential from the generated Q log files for each and offset by the minimum (will become zero). 

- Then compare the profiles and define new torsional terms to fit the QM scan if needed (you can use regression tools in R or so if things are not obvious).

- Then re-use those parameters within your Forcefield/Qoplsaa.prm file to generate "corrected" topologies. And re-run an MM scan to double-check that the new relative potential energies match the QM ones now.
