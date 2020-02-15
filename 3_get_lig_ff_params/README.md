# Get OPLS ligand force field parameters

For each FEP, you will need the force field parameters of both the MD topology's ligand (usually the biggest) and of the one to compare it to. I would advice to run a few relevant retrospective predictions to calibrate your MD/FEP protocol first (i.e. protonation states in the binding site, sphere size, simulation time..) and see if it allows to reproduce experimental binding affinities.


## **Option 1. Using hetgrp_ffgen (still accessible on Tetralith, at least on Pierre's account)**



## **Option 2. Using ffld_server (accessible on CSB)**

Go t

## **Option 3. Using new force field parameters (LigParGen)**

Go to http://zarbi.chem.yale.edu/ligpargen/index.html . For Q (as other MD engines), this can generate a ligand force field library file as well as paramterers to insert in your "Qopplsaa.prm" force field file. But do not use it until they have fix the problem of wrongly multiplied force constants for bonded parameters for Q. 

What you can eventually do though is to use better quality partial charges by translating the information from the generated "LIG.lib" file (especially if you will carry out transformations of heterocycles, atypical chemical moieties or do scaffold hopping/optimization in general).

```./prep_mapping_files_ligpargen2Q.py rec.pdb LIG.pdb 0.2```

```./ligpargen2Q_charges.py LIG.lib LIG_prgn.lib N9```
