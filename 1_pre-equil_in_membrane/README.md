# Equilibration of your favorite GPCR in a pre-equilibrated 1-palmitoyl-2-oleoyl-glycero-3-phosphocholine (POPC) lipid bilayer 

## **1. Cleaning up the receptor structure**

Go to https://opm.phar.umich.edu/ and search for your PDB code of interest and download the equivalent **OPM** PDB file (containing membrane delimiters). 

In **PyMOL**,
- Fetch your PDB of interest and load the downloaded OPM equivalent as well. If the structure is multimeric, only keep the prefered monomer of you receptor (unless you want to study a particular oligomer)! 
- Remove the nanobody if any, as well as ligands and crystallization agentds ("organic"), waters ("resn HOH") and ions ("metal"). 
- If any mutation in your structure (information found in the PDB file), mutate back to wild type with the "Wizzard Mutagenesis Tool" (choose relevant rotamer and eventually use a template if any). 
- Align your PDB of interest to its OPM equivalent and save it! 
Note: Check that all occupancies are 1.00 for each residue or you will need to choose a romater among the solutions found in the PDB structure (remove atoms of the undesired solution then..).

If any residue is incomplete, use modeller to ass missing atoms with the enclosed script (PS. You can get modeller here: https://salilab.org/modeller/download_installation.html). Syntax is as follows:
```modX.XX add_missing_atoms_modeller.py YOUR_SAVED_STRUCTURE.pdb #X.XX according to your modeller version.```

The output is named like YOUR_SAVED_STRUCTURE_full.pdb. You will run MD/FEP simulations in spherical boundary conditions (system reduced to a sphere of a given radius, typically 18-30 Angstroms centered on a ligand atom). If any loop is incomplete and might be included in your simulation sphere, reconstruct it with modeller or simply with a morphing process after modelling the full receptor on GPCR-ModSim (http://open.gpcr-modsim.org/).

## 2. Inserting your receptor in a membrane**

**Option 1.** Using GPCR-ModSim

Using 
