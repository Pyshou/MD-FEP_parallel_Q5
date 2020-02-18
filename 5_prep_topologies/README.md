# Prepare topologies for MD

Here, we will make a topology for the MD/FEP transformation of our ligand A both in water and in the receptor. Note that if you instead want to run an amino acid FEP, rather prepare one apo and on holo structure of the receptor. In that case, add the missing Gromacs waters you got in section 3 of the repository for the apo form (where the ligand normally is..).



## **1. Ligand in water**

- Make a new folder i.e. called top_X (X=name of your compound A).

- Go inside and copy the associated "Forcefield" folder you created in section 3 of this repository for compound A of your transformation.

- Also copy the associated rec.pdb you created at that stage (with cleaned up formated coordinates of the ligand from section 3).

- Copy the enclosed qprep_wat.in file and adjust the solvate and boundary lines by changing the "N9" atom name by the one of your ligand you choose as sphere center. In these two lines, also change the "21" to the sphere radius you have chosen when setting up your sphere in section 2 of the repository.

- Inside the Forcefield/ folder, make sure the charge group section in the LIG.lib file starts with a heavy atom. 

Note: If have used ffld_server to generate parameters in section 3 and you are doing amino acid FEPs, you should define neutral (or neat) charge groups by fragmenting the molecule (one line listing atoms per charge group, starting from a heavy atom). If you don't do that (for amino acid FEPs), you will get shake failure errors during the simulations as ligand atoms will not be defined as Q atoms in FEP files (and they will have a cut-off to treat long range interactions with LRF).

- Generate a topology with Qprep. The syntax is as follows:

```$QPATH/bin/qprep5 < qprep_wat.in > qprep.out``` # $QPATH=where you installed Q.. . Install Q5 using the script located in the main folder of this repository if needed. This version will be needed to run and analyze simulations with compatibility with analysis scripts later.

- Check the qprep.out file and that you have no warning about fraction charge groups if you have defined several (if doing amino acid FEPs)!


## **2. Ligand in the receptor**

- Make another folder rather called i.e. top_X_rec (X=name of your compound A).

- Do the same as before (get the "Forcefield" folder of your ligand A) and instead, your rec.pdb is the receptor you prepared in section 2 of this repository.

- Now, replace the ligand coordinates by those of your aligned compound A (rec.pdb prepared in section 3). For the superimposition, you can just use the PyMOL Pair Fitting Wizard and editing mode for adjusting torsions to generate an initial binding mode.. . If you see several possible orientations for the introduced moiety, I would advice generating a topology for each and running i.e. a "moiety anihilation" FEP for all and then only retain the one leading to the lowest relative binding free energy.

- Remove waters clashing with the ligand. To do it fast, use the script of section 2 as follows:

```./remove_clashes.py LIG -s HOH -t 2.0 rec.pdb``` # Output is rec_noclash.pdb. Double-check and this one will become your rec.pdb (rename it!).

- Copy the enclosed qprep_rec.in file and adjust the "boundary" line by changing the "N9" atom name by the one of your ligand you choose as sphere center. In this line, also change the "21" to the sphere radius you have chosen when setting up your sphere in section 2 of the repository.

- Note that there is no solvate section in our case since we use Gromacs waters (and this doesn't work properly with our POPC lipids which are not properly recognized with qprep to estimate density of waters anyway). But use solvate as above if you start from a PDB structure of a soluble protein add want to add Q waters instead.

- Also adjust the "addbond" sections to assign disulfide bridges between cysteines's SG atoms (assignment by residue number, the residue being normally already named "CYX" in your rec.pdb according to section 2 of the repository). 

- As before, inside the Forcefield/ folder, make sure the charge group section in the LIG.lib file starts with a heavy atom. 

Note: If you are doing amino acid FEPs and had to change charge groups above, use the same Forcefield/LIG.lib file as the one used to generate the topology of the ligand in water.

- Generate a topology with Qprep. The syntax is as follows:

```$QPATH/bin/qprep5 < qprep_rec.in > qprep.out``` # $QPATH=where you installed Q..

- Open the topology (topology.top file) and again, find the line containing the "solvent radii" definition. Change the second column by your sphere radius (first column) minus 0.5 Angstroms, corresponding how you kept sphere waters when preparing your sphere in section 2 of the repository (the original value is wrong as it is estimated from the number of waters / solvent density in the system while POPC lipids are ignored). Ignore this for soluble proteins.
