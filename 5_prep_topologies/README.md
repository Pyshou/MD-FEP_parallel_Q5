# Prepare topologies for MD

Here, we will make a topology for the MD/FEP transformation of our ligand A both in water and in the receptor. Note that if you instead want to run an amino acid FEP, rather prepare one apo and on holo structure of the receptor.



## **Generation of FEP files**

- This will generate a python dictionnary in an atom name mapping file. Use this type of force field folder architecture for the inputs (as suggested in "section 3" of this repository). PDB files of the compounds will be loaded (make sure they are superimposed):

```python2.7 ./prep_mapping_files.py ff.lig.A/rec.pdb ff.lig.B/rec.pdb 0.2``` # A and B are the name of the respective (biggest and smallest) compounds. 0.2 Angstroms is the distance treshold for atoms to be considered as matched
