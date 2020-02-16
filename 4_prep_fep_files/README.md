# Prepare FEP files for alchemical ligand transformations

Here, we will conveniently pre-generate and edit input files for Q stating the alchemical transformations to carry out based on a single topology approach (the instructions assume that you will only go from the biggest ligand to the smallest one, starting from the topology of the biggest ligand, "compound A"). 

I usually carry out the transformation in four major steps: (i) updating the electrostatic potential to the one of compound B, (ii) adding a softcore potential for atoms that will be anihilated, (iii) setting van der Waals parameters to zero to anihilate those atoms and (iv) applying bonded term changes together with van der Waals transformation for remaining atoms. 

Note: The scripts will work if you have used the protocol/formatting of section 3 to generate force field parameters. Also, different Schrodinger versions might lead to different outputs (even when the parameters are the same), and small things might need to be changed in those scripts (I can adjust them easily if you provide me your inputs and I will try to cleanup and comment the scripts further in the future)

Note2 (ADD BELOW): You will need to skip the second and third steps if there is no anihilation, and to remove the pre-generated softcore statements if any.


## **Generation of FEP files**

```/home/apps/schrodinger2015/utilities/ffld_server -imol2 rec.mol2 -opdb rec.pdb -print_parameters > LIG.ffld``` # Use a rec.mol2 file for the compound to generate force field parameters for
