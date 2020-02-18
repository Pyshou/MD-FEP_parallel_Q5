# Preparation of a spherical system for MD/FEP simulations in Q

Here, we will take a pre-equilibrated snapshot of your system in lipid bilayer as input (see section 1). We will prepare it for MD simulations in Q using spherical boundary conditions. All this could be further automated but I like paying attention to each of these steps and they don't take long when you are used to that (also very important as your MD/FEP calculations will inherit from your system preparation).

**Cleanup and format structure for Q**

- Remove header, chain ID and b-factor stuff (last columns), plus convert TER into GAP flags. You can read the enclosed script as follows:

```./remove_unneccesary_stuff.py eq_clean.pdb``` # output is rec_formated.pdb

- Remove all counter-ions in the output PDB manually

- Rename water oxygen atoms "OW" into "O " (a sed will do that):

- Introduce a "GAP" tag line if your protein is truncated somewhere (i.e. missing intracellular loop...)

- Remove water and receptor hydrogens using the enclosed script as follows:

```remove_hydrogens.py rec_formated.pdb``` # Output is rec_noH.pdb

- Add fromated PDB coordinates of aligned smallest ligand of your FEP series (with residue name "LIG") between the protein and the first POPC lipid atom, and add "GAP" string-containing lines before and after the ligand coordinate lines. It is convenient to have the smallest compound of the MD/FEP series as you will have all needed waters already there and will only need to remove clashing ones when growing / adding moieties.

- Remove clashing waters from it (i.e. with oxygens within 2 Angstroms of ligands' non-hydrogen atoms). You can use the enclosed script as follows:

```./remove_clashes.py LIG -s HOH -t 2.0 rec_noH.pdb``` # Output is rec_noH_noclash.pdb

- Add aligned and fromated binding site crystal waters (same formatting as other waters), and remove Gromacs waters (or lipid residues) that clash with them (check in PyMOL but don't save the PDB with it as it will mess with the formatting!).

- Keep only waters within sphere radius - 0.5 Angstroms of chosen ligand/residue atom chosen as sphere center (radius you choose for simulation sphere, typically between 18 and 30 Angstroms). You can use the enclosed script as follows:

```./remove_waters_outside_sphere.py rec_noH_noclash.pdb N9 18``` Here, the sphere center is atom N9 of residue 'LIG' and the chosen sphere radius is 18 Angstroms. The output will be rec_noH_noclash_sphered.pdb.

- Renumber residues sequentially using the enclosed script as follows (will be needed to assign protonation states and prepare Q topologies the way Q sees the structure):

```./residue_renumbering.py rec_noH_noclash_sphered.pdb``` # You get an output.pdb file.

- Change the "CD " atom name of all ILE residues into "CD1" (just use a sed englobing isoleucines only..)

- Then identify your C-terminal residue and rename it's "O1" oxygen to "O " and remove the "O2" extra atom of this residue (Q won't complain then and you don't care about CAPs when the termini are located outside your sphere as most of the time)!


**Assign protonation states**

- Now, note residue numbers for cysteines involved in disulfide bridges (will be named "CYX") as well as delta- (HID), epsilon- (HIE) and doubly-protonated (HIP) histidines.

In Q, you will define an inner sphere treated normally while solute atoms in the outer sphere will be tightly restrained to their initial coordinates, residues in this outer sphere will all need to be neutral as this region is used as a schild since nothing will be included for non-bonded interactions outside (and some restraints will also be applied on solvent molecules in this region according to the SCAAS model)!

- No worries, Q will take care of this but read and do the following! For receptor-ligand complexes, the outer sphere will typically be everything between the sphere radius minus 3 Angstroms and the sphere radius to the sphere center (chosen central ligand atom for all simulations). All glutamate, aspartate, lysines and arginines in your PDB will have to be renamed into "GLH", "ASH", "LYN" and "ARGN" so write down associated residue numbers (use PyMOL, making a selection for the sphere, one for the innter sphere and then, the outer one will be all in the sphere that do no belong to the inner region! Then look at the sequence for ARG,LYS,GLU and ASP there and check if there are side chain atoms in the outer sphere!)

- Then you can prepare a file you can name "ionize" with the following format. It will be used as input for formatting the PDB:

```
50 ASH
159 GLH
73 HID
236 HIE
249 HID
263 HID
CYX 75
CYX 164
CYX 245
CYX 248
```

- Run this:

```./prep_structureQ.pl rec0.pdb ionize``` # rec0.pdb should be your output.pdb from before.. . Now you get a formatted rec.pdb file that will be used to make receptor-ligand topologies later!
