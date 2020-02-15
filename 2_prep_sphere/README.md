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

- Add fromated PDB of aligned ligand (with residue name "LIG") between the protein and the first POPC lipid atom, and add "GAP" string-containing lines before and after the ligand coordinate lines

- Remove clashing waters from it (i.e. with oxygens within 2 Angstroms of ligands' non-hydrogen atoms). You can use the enclosed script as follows:

```./remove_clashes.py LIG -s HOH -t 2.0 rec_noH.pdb``` # Output is rec_noH_noclash.pdb
