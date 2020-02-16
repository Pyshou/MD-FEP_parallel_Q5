# Prepare FEP files for alchemical ligand transformations

Here, we will conveniently pre-generate and edit input files for Q stating the alchemical transformations to carry out based on a single topology approach (the instructions assume that you will only go from the biggest ligand to the smallest one, starting from the topology of the biggest ligand, "compound A"). 

I usually carry out the transformation in four major steps: (i) updating the electrostatic potential to the one of compound B, (ii) adding a softcore potential for atoms that will be anihilated, (iii) setting van der Waals parameters to zero to anihilate those atoms and (iv) applying bonded term changes together with van der Waals transformation for remaining atoms. 

Note: The scripts will work if you have used the protocol/formatting of section 3 to generate force field parameters. Also, different Schrodinger versions of formatting might lead to different outputs (even when the parameters are the same), and very small things might need to be adjusted in those scripts (I can do that very easily if you provide me your inputs and I will also try to cleanup and comment the scripts further in the future)



## **Generation of FEP files**

- This will generate a python dictionnary in an atom name mapping file. Use this type of force field folder architecture for the inputs (as suggested in "section 3" of this repository). PDB files of the compounds will be loaded (make sure they are superimposed):

```python2.7 ./prep_mapping_files.py ff.lig.A/rec.pdb ff.lig.B/rec.pdb 0.2``` # A and B are the name of the respective (biggest and smallest) compounds. 0.2 Angstroms is the distance treshold for atoms to be considered as matched

- Now open the generated mapping .txt file and whenever atoms are beyond the distance treshold, a "?" will be added so correct the information if needed and remove the "?". For atoms that will be anihilated, introduce a "DU" name instead of the one of the closest found atom

- Now pre-generate FEP files:

```python2 ./prep_fep_file_ffld_server/main.py ff.lig.A/Forcefield/LIG.lib ff.lig.B/Forcefield/LIG.lib mapping_A_to_B.txt``` # same as before (A and B are the name of the respective compounds). If you rather used hetgrp_ffgen to generate ligand ff parameters (section 3 of repository), use the corresponding script instead

- Now, check the partial charges in lig_step0.fep (they are normally always right). The first column corresponds to atom indices in compound A, the second the corresponding partial charges and the third the partial charge in state B (compound B)

- Use this script to double check that the charge is neat in both states:

```python2 ./check_fractional_charges_LIGfep.py lig_step0.fep``` # You might see something as -0.0 or 0.0 (as you know, for the computer, operations on floating numbers often lead to a residual errors but what you see is a charge rounded to six decimals so only one zero shown means you just have zeros for the next five digits and it is in fact zeros.. ^^).

- If you have no atom to anihilate in your transformations, just remove lig_step1_1.fep as well as all softcore statements in lig_step1_2.fep (at the beggining + [softcore] section) and then skip next 2 points.

- Verify the [softcore] section in lig_step1_1.fep file. It should be applied to atoms of compound A that will be anihilated in compound B only (third column has a "20" which is the potential's limit at overlap with other atoms in kcal/mol, which makes the atoms somehow already smaller)

- In lig_step1_2.fep, change the "XX" in the softcore section to 0 if this is correct (turning off softcore, not mandatory to turn it off though since the atom will not exist in state B anyway. But Q will not understand "XX". This is just for you to check)

- In this file, also remove all "?" characters in the [change_atoms] section when this is correct (in this step, we go to a "DU" / dummy atom as defined in the [atom_types] section and which has basically no more van der Waals potential in state B of that transformation step)

```cp lig_step1_2.fep lig_step1_3.fep``` # Move to lig_step1.fep instead if no anihilation

- Update previous changes (introduced changes of column 3 into column 2 ("DU" for anihilations)) and add remaining van der waals (atom type) changes into columb 3 (look at respective Qoplsaa.prm parameter files in the "NONBONDED LIG PARAMETERS" section for respective compounds). You might need to define new atoms in the "[atom_types]" section

- Now check for bonded term changes:

```python2 ./compare_bonffparams_Qoplsaa_ffld_server.py ff.lig.A/Forcefield/Qoplsaa.prm ff.lig.B/Forcefield/Qoplsaa.prm mapping_A_to_B.txt``` # If you rather used hetgrp_ffgen to generate ligand ff parameters, use the corresponding script instead. The script will display human-friendly changes for you and write FEP sections for Q in changes.fep

- Add bonded term changes to the last transformation step with the following:

```echo "" >> lig_step1_3.fep```

```cat changes.fep >> lig_step1_3.fep```

## **LigParGen variant scripts**

One script has been made for the case when you use LigParGen parameters but I would avoid that as the bonded parameters for Q are wrong (see section 3 of this repository).

## **Amino acid FEPs**

There are also variants for amino acid transformations (where the thermodynamics cycle implies a transformation of the amino acid in both the apo and holo receptor to evaluate the effect of mutations on ligand binding). Extract coordinates of the two amino acids to compare and superimpose them as much as you can to generate a mapping file as shown above. For the pre-generation of FEP files, you will need a .lib library for each amino acids (A and B) instead of a .prm file. To generate them, use the following:

```python2 ./make_amino_acid_lib.py Forcefield/Qoplsaa.lib ARG``` # For arginine, for example

Then use the respective .lib files instead of .prm files for the bonded term change evaluation script. It will also be looking for a Forcefield/Qoplsaa.prm file where your run the script:

```python2 ./compare_bonffparams_Qoplsaa_amino_acids.py AA1.lib AA2.lib mapping_file.txt```
