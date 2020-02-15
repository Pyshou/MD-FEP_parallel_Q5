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

- Add fromated PDB coordinates of aligned ligand (with residue name "LIG") between the protein and the first POPC lipid atom, and add "GAP" string-containing lines before and after the ligand coordinate lines

- Remove clashing waters from it (i.e. with oxygens within 2 Angstroms of ligands' non-hydrogen atoms). You can use the enclosed script as follows:

```./remove_clashes.py LIG -s HOH -t 2.0 rec_noH.pdb``` # Output is rec_noH_noclash.pdb

- Add aligned and fromated binding site crystal waters (same formatting as other waters), and remove Gromacs waters (or lipid residues) that clash with them (check in PyMOL but don't save the PDB with it as it will mess with the formatting!).

- Keep only POPC lipids that have atoms within 30 Angstroms of chosen ligand/residue atom as sphere center, as well as waters within sphere radius - 0.5 Angstromns (radius you choose for simulation sphere, typically between 18 and 30 Angstroms). You can save an HOHin.pdb and a POPin.pdb as reference files and use the enclosed script as follows:
