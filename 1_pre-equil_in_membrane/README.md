# Equilibration of your favorite GPCR in a pre-equilibrated 1-palmitoyl-2-oleoyl-glycero-3-phosphocholine (POPC) lipid bilayer 

## **1. Preparing the receptor structure**

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

**Option 1. Using GPCR-ModSim (You might have to wait for a day to get the output though)**

- Upload your formated PDB on http://open.gpcr-modsim.org using the "Model a GPCR" section, and choose to run a molecular dynamics simulation. 
- After typically one day, you will be able to download outputs and get the unaltered **hexagon.pdb** structure of the full system

Note: Unfortunately, we cannot stop GPCR-ModSim early. You can look at option 3 if you want to use the standalone version of PyMemDyn and stop it early to get this file.


**Option 2. Using an already prepared closely-related GPCR structure as template**

- Check the "Gromacs_templates/Structures" folder enclosed.
- Align your receptor to the chosen template (i.e. Using PyMOL) and save new coordinates.
- Insert your new coordinates inside the PDB of the full template system by replacing those of the template receptor.
- Then remove clashing elements (waters, ions and membrane residues), i.e. in PyMOL: "select clashingHOH, byres resn SOL and name OW within 2 of not resn SOL+CL+NA+POP and not hydro" for waters oxygens within 2 Angstroms of receptor heavy atoms (inspect and remove clashing ones).

Note: Make sure the template structure is close enough so you don't have to either remove too many waters or lipids or potentially lack a lot!


**Option 3. Using the standalone version of PyMemDyn (classical)**

- To run pymemdyn, you need an old Gromacs version (4.6.3 works) and python2.7(.6). This verison used to work on the old Triolith supercomputing ressources. To run it, use the following (you can eventually add options according to the manual):

```pymemdyn -p rec_aligned.pdb```

This script can be found within the corresponding pymemdyn script folder. You can kill it after a few seconds. You will only need an **hexagon.pdb** file. 

Note: If you need a new version or some help running it, ask Hugo Gutiérrez de Terán (PI of development team) or yout colleague Jon Kapla who has been able to run it recently with an adaptation using the CHARMM force field (note that we will be using OPLS-AA here).
