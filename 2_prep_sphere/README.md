# Preparation of a spherical system for MD/FEP simulations in Q

Here, we will take a pre-equilibrated snapshot of your system in lipid bilayer as input (see section 1).

- Remove header, chain ID and b-factor stuff (last columns), plus convert TER into GAP flags with the following script:
```
remove_unneccesary_stuff.py <equilibrated_rec.pdb>
```
output is rec_formated.pdb
