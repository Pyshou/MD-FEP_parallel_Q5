# Preparation of a spherical system for MD/FEP simulations in Q

Here, we will take a pre-equilibrated snapshot of your system in lipid bilayer as input (see section 1). All this could be further automated but I like paying attention to each of these steps and they don't take long when you are used to that (also very important as your MD/FEP calculations will inherit from your system preparation).

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

- Keep only waters within sphere radius - 0.5 Angstroms of chosen ligand/residue atom chosen as sphere center (radius you choose for simulation sphere, typically between 18 and 30 Angstroms). You can use the enclosed script as follows:

```./remove_waters_outside_sphere.py rec_noH_noclash.pdb N9 18``` Here, the sphere center is atom N9 of residue 'LIG' and the chosen sphere radius is 18 Angstroms. The output will be rec_noH_noclash_sphered.pdb.

- Renumber residues sequentially using the enclosed script as follows:

```./residue_renumbering.py rec_noH_noclash_sphered.pdb``` # You get an output.pdb file.

- You eventually need to do the following renamings from Gromacs to Q:

```sed -i -e 's/CD  ILE/CD1 ILE/g' output.pdb```

- Then identify your C-terminal residue and rename it's "O1" oxygen to "O " (here, I had a Serine):

```sed -i -e 's/O1  SER/O   SER/g' hexagon.pdb```

- Also remove the "O2" extra atom of this residue!
