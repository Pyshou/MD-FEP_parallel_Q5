# Prepare topologies for MD

Here, we will make a topology for the MD/FEP transformation of our ligand A both in water and in the receptor. Note that if you instead want to run an amino acid FEP, rather prepare one apo and on holo structure of the receptor. In that case, add the missing Gromacs waters you got in section 3 of the repository for the apo form (where the ligand normally is..).



## **1. Ligand in water**

- Make a new folder i.e. called top_X (X=name of your compound A).

- Go inside and copy the associated "Forcefield" folder you created in section 3 of this repository for compound A of your transformation.

- Also copy the associated rec.pdb you created at that stage (with cleaned up formated coordinates of the ligand from section 3).

- Copy the enclosed qprep_wat.in file and 

- Inside the Forcefield/ folder, make sure the charge group section in the LIG.lib file starts with a heavy atom. 

Note: If you are doing amino acid FEPs, you should define neutral (or neat) charge groups by fragmenting the molecule (one line listing atoms per charge group, starting from a heavy atom). If you don't do that (for amino acid FEPs), you will get shake failure errors during the simulations as ligand atoms will not be defined as Q atoms in FEP files (and they will have a cut-off to treat long range interactions with LRF).

```
