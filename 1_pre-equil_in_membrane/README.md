# Pre-equilibration of your favorite GPCR in a POPC lipid bilayer 

Preparation of a new system for MD/FEP caculations might take a few days each time. But your caclulations will all depend on that step and you need to do it properly. Also ask around if an MD/FEP colleague has already prepared your system in a successful project before (it can be advantageous and you could then skip this).

## **1. Preparing the receptor structure (skip if using option 2 in next section)**

Go to https://opm.phar.umich.edu/ and search for your PDB code of interest and download the equivalent **OPM** PDB file (containing membrane delimiters). 

In **PyMOL**,
- Fetch your PDB of interest and load the downloaded OPM equivalent as well. If the structure is multimeric, only keep the prefered monomer of you receptor (unless you want to study a particular oligomer)! 
- Remove the nanobody if any (typically "resi 1000-*"), as well as ligands and crystallization agents ("organic"), waters ("resn HOH") and ions ("metal"). 
- If any mutation in your structure (information found in the PDB file), mutate back to wild type with the "Wizzard Mutagenesis Tool" (choose relevant rotamer and eventually use a template if any).
- Check that all occupancies are 1.00 for each residue or you will need to choose a romater among the solutions found in the PDB structure (remove atoms of the undesired solution then..).
- Align your PDB of interest to its OPM equivalent and save it! 

If any residue is incomplete, use modeller to ass missing atoms with the enclosed script (PS. You can get modeller here: https://salilab.org/modeller/download_installation.html). Syntax is as follows:
```modX.XX add_missing_atoms_modeller.py YOUR_SAVED_STRUCTURE.pdb #X.XX according to your modeller version.```

The output is named like YOUR_SAVED_STRUCTURE_full.pdb. You will run MD/FEP simulations in spherical boundary conditions (system reduced to a sphere of a given radius, typically 18-30 Angstroms centered on a ligand atom). If any loop is incomplete and might be included in your simulation sphere, reconstruct it with modeller or simply with a morphing process after modelling the full receptor on GPCR-ModSim (http://open.gpcr-modsim.org/).


## 2. Inserting your receptor in a membrane

**Option 1. Using GPCR-ModSim (Easy but you might have to wait for a day to get the output though)**

- Upload your formated PDB on http://open.gpcr-modsim.org using the "Model a GPCR" section, and choose to run a molecular dynamics simulation. 
- After typically one day, you will be able to download outputs and get the unaltered **hexagon.pdb** structure of the full system

Note: Unfortunately, we cannot stop GPCR-ModSim early. You can look at option 3 if you want to use the standalone version of PyMemDyn and stop it early to get this file.



**Option 2. Using an already prepared closely-related GPCR structure as template**

- Check the **Gromacs_templates/Structures** folder enclosed.
- Align your receptor to the chosen template (i.e. Using PyMOL) and save new coordinates.
- Insert your new coordinates inside the PDB of the full template system by replacing those of the template receptor.
- Then remove clashing elements (waters, ions and membrane residues), i.e. in PyMOL:

```select clashingHOH, byres resn SOL and name OW within 2 of not resn SOL+CL+NA+POP and not hydro``` 

for waters oxygens within 2 Angstroms of receptor heavy atoms (inspect and remove clashing ones).

Note: Make sure the template structure is close enough so you don't have to either remove too many waters or lipids or potentially lack a lot!



**Option 3. Using the standalone version of PyMemDyn (classical)**

- To run pymemdyn, you need an old Gromacs version (4.6.3 works) and python2.7(.6). This verison used to work on the old Triolith supercomputing ressources. To run it, use the following (you can eventually add options according to the manual):

```pymemdyn -p rec_aligned.pdb```

This script can be found within the corresponding pymemdyn script folder. You can kill it after a few seconds. You will only need an **hexagon.pdb** file.

Note: If you need a new version or some help, ask Hugo Gutiérrez de Terán (PI of development team), or your colleague Jon Kapla who has been able to run it recently with an adaptation using the CHARMM force field (note that we will be using OPLS-AA here).


## 3. Running restrained equilibration with Gromacs

**Assigning of protonation states**

PyMemDyn (GPCR-ModSim) only runs a short restrained equilibration, and if you let it run, releases restraints gradually in subsequent steps (which we do not want). It also uses default protonation states of residues and all histidines are protonated in the delta position... . So we will need some manual edits!

- Copy files located in the enclosed Gromacs_templates/Restrained_equil_files folder
- On CSB:
```module load gromacs/2019```
- Copy the full system (i.e. the "hexagon.pdb" file) into a "protein.pdb" file where you only keep protein coordinates.
- Run PDB2GMX to extract protein force field parameters and also generate a formated PDB for the protein:

``` gmx_d pdb2gmx -f protein.pdb -o protein_gmx.pdb -ignh -his```
Choose OPLS-AA, TIP3P waters and assign histidine protonation states (PS. You can also add -glu/-asp/-arg/-lys flags i.e. to neutralize a usually charged residue located at the membrane interface, or ASP2.50 for agonist-bound structures)

**Updating topology**

- Rename the generated file and restore mother topology

```mv topol.top protein.itp```

```mv '#topol.top.1#' topol.top```

- In protein.itp, rename the object (i.e. "Protein_chain_A") in the [ moleculetype ] section to "protein" or at least to match the object name in topol.top
- Remove the "#include "oplsaa.ff/forcefield.itp" line as it will be already loaded from the topol.top mother topology and Gromacs will complain about that.
- At the end of the file, remove everything from "; Include Position restraint file" / after the improper section (same thing)
- Now replace the protein coordinates in the full system PDB file (i.e. hexagon.pdb) by those of the previously generated protein_gmx.pdb file
- Now adjust the number of POPC lipids, solvent molecules and ions in the end of topol.top . For counting residues, you can for instance use the following for POPC lipids (same applies for "SOL" molecules, dividing by 3 and not 52 while for ions, the counting is straighforward):

```nbPOPatm=$(grep POP system.pdb | wc -l); echo $nbPOPatm"/52"|bc``` # 52 atoms per Berger united atom POPC lipid
- Make a test compiling information for minimization

```gmx_d grompp -f minmize.mdp -p topol.top -c system.pdb -o minmize.tpr```
- If the note tell you that the charge of the system is not zero, the system will explode in PBC! So remove ions in the PDB or replace their atom and residue names by those of ions of opposite charge. You can also remove hydrogens of a water molecule you identified in a good spot and change the oxygen's atom and residue name to those of the ions you want to replace it by, and then move the new ion lines in the coorresponding ion coordinates part of the PDB. Then update the ion counts in topol.top and run the previous command again.
- Let's make an index file containing temperature coupling groups needed for equilibration later:

**Preparing simulations**

```gmx_d make_ndx -f system.pdb -o index.ndx``` # Select the index number of "SOL" and of "Ion" with "|" between i.e. "16|18" in my case. Rename the new group by typing "name 22 Water_and_ions", number 22 being the newly created group in my case.
```q``` (exit)
- Make restraints file with high force constant on protein's heavy atoms in all dimensions:

```gmx_d genrestr -f system.pdb -fc 5000 5000 5000 -n index.ndx -o posre.itp``` # Type '2' (protein heavy atoms)
- Now run the minimization (can be done on login node in up to few minutes or in parallel as well):

**Running minimization and equilibration in a parallel job**

```gmx_d mdrun -s minmize.tpr -deffnm minmize```
- Prepare equilibration (Note: Check the eq.mdp file if you want to change settings or simulation time):

```gmx_d grompp -f eq.mdp -p topol.top -c minmize.gro -r minmize.gro -o eq.tpr -n index.ndx -maxwarn 1```
- Run equilibration in parrallel. Put something like that in your submission script:

```gmx_mpi mdrun -s eq.tpr -deffnm eq``` # Syntax on Beskow. PS. Load the coorresponding gromacs module on login node + inside the script as well, i.e. module load gromacs/2019.3 on Beskow.
- When done, center last frame of trajectory and have a look:

**Checking last MD snapshot (input for next steps)**

```gmx_d trjconv -f eq.gro -s eq.tpr -pbc mol -center -n index.ndx -o eq_centered.pdb``` # Select group for centering and then for output (i.e. '3' for Calpha, and '0'=everything for output).
- Rename residues to have things clean displayed correctly in PyMOL (Particularly POPC lipids):

```gmx editconf -f eq_centered.pdb -resnr 1 -o eq_clean.pdb```

- Check in PyMOl that your receptor is well solvated and that the membrane seems well packed around the receptor structure and is correctly equilibrated.
