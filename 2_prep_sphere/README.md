# Preparation of a spherical system for MD/FEP simulations in Q

Here, we will take a pre-equilibrated snapshot of your system in lipid bilayer as input (see section 1).

- Remove header, chain ID and b-factor stuff (last columns), plus convert TER into GAP flags. You can read the enclosed script as follows:
```./remove_unneccesary_stuff.py eq_clean.pdb``` # output is rec_formated.pdb
- Remove all counter-ions in the output PDB manually
- Rename water oxygens lines using:
```sed -i -e 's/OW  SOL/O   HOH/g' rec_formated.pdb```
- Introduce a "GAP" tag line if your protein is truncated somewhere (i.e. missing intracellular loop...)
- Remove water and receptor hydrogens using the enclosed script as follows:
```remove_hydrogens.py rec_formated.pdb``` # Output is rec_noH.pdb
