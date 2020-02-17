# Preparing FEP folders, submitting the jobs and analyzing the results

## **1. Preparing FEP submission folder**

We will set up and submit an MD/FEP transformation where every intermediate state will be equilibrated and equilibrated independently. This is advantageous to get results relatively fast when you can run a lot of jobs on a supercomputer and also, you will need much less replica for achieving convergence since you will avoid getting trapped in low energy regions of intermediate states that may result in not sampling the last state (compound B) fairly. This can be easily scripted for each case if more convenient.

- Now that you have all the needed files, create a FEP folder (i.e. A_to_B/) and within it, one for the ligand transformation in water (WAT/), and one for the transformation in the receptor binding site (REC/). 

- Each of those should contain an md_step0/, md_step1_1/, md_step1_2/ and md_step1_3/ folder (or just md_step0/ and md_step1/ if you are not anihilating any atom). 

- Within each, create an input_files/ folder containing the appropriate template Q input files as enclosed, as well as the corresponding topology.top (water or receptor topology of your compound A created in section 5 of the repository), and the respective lig_step*.fep file generated in section 4, named as lig.fep.

- For the lig.fep files within the REC/md_step*/input_files/ folders, change the "offset residue" to the residue number of the compound to FEP in the previously generated topology.pdb (then indices in the FEP file will start from 1 for the first ligand atom).

- Inside the */md_step*/input_files/*.inp and */md_step*/input_files/dc0 files, change she shell_radius (inner sphere radius) to your sphere radius minus 3 Angstroms inside the REC/ folder and minus 1 Angstrom inside the WAT/ folder (defining the outer shell shielding region for all simulations).

- Inside the REC/md_step*/input_files/eq*.inp files, adjust the sequence_restraints (atom index "4926" should become the index of the last solute (ligand) atom as found in the previously generated topology.pdb).

- Inside the WAT/md_step*/input_files/eq*.inp and the WAT/md_step*/input_files/dc0 files, adjust the atom restraints section (first column is atom index of sphere center ligand atom as defined when you made the water topology, second third and fourth are its initial coordinates). This will keep this atom in the center of the sphere (otherwise, hydrophobic molecules might move close to the border of the sphere or so..).

- The */md_step*/input_files/dc0 is a template for MD production with by default 100 ps (100000 steps) in water and 250 ps for the productions in the receptor. You can extend them as well if you want to assess convergence over simulation time later (and also adjust the eq*.inp files if you want to extend equilibrations as well).

- Now, inside each */md_step*/input_files/ folder, generate a production file for each intermediate state (typically 11 for electrosatics and turning on softcore potential (step0 and step1_1), 21 for anihilations (step1_2) and 41 for the last step. For that, edit a template FEP.in file listing the lambda values from 1 to 0 (see enclosed). You can also use the following script to generate the numbers accoridng to the desired number of intermediate states:

```python3 ./lambda_generator.py 1 0 0.1 | wc -l``` # You will need numpy to be installed. This generates such a FEP.in file and the pipe also print the corresponding number of states where first argument is lambda value of state A (1.0), second lambda of state B (0.0) and third is the increment between lambda values for generating intermediate states (adapt this!).

- Then, generate those production files out of the dc0 template using:

```python2 make_fep_files_parallell.py -i FEP.in``` # You will now see dc*.inp files with lambda values stated in the end.

## **2. Submitting jobs**

Outside the FEP folder, run the enclosed **master_script_beskow.sh** script that you can adjust (path to called scripts at the beginning, folders to go to and more lines if running more than 3 replica per lambda window / intermediate state), as well as the enclosed scripts it calls (some lines in **make_submission_file_beskow.sh** might need to be changed if you are not running those on Beskow implying a different configuration of nodes and if using another allocation project ID than "2019-2-16")

## **3. Checking data integrity after job completion **

You can use a bash loop like that to list unfinished or problematic simulations:

```for fold in $(ls -d A_to_B/*/md_step*/md_rs*/dc*/); do nb=$(tail $fold/dc*log | grep "terminated normally" | wc -l); if [ $nb -eq 0 ]; then echo $fold" is not finished!"; fi; done```

## **4. Analyzing results **

Inside each REC/ and WAT/ folder, run the enclosed **analyse_energies.py** script after adjusting the paths to the Qfep executable and the input_files/ folder (see enclosed template folder). This folder requires a qfepX.in file for each main transformation step, loading the corresponding energy files sequentially (which means you should have a qfep11.in file there when having 11 lambda windows, i.e. as default in step0), Also, the first column of the third row should corresponding to RT in kcal/mol according to the target temperature in your simulations (here 300K). This scripts normally considers up to 9 replica (the CSV output will have several time the same replica-wise value when using less so ignore the duplicated values). the deltadeltaG results will be the average in the receptor minus in water and you can also look for the forward-reverse hysteresis error (forward-reverse) and see from the full_data.csv output if there are unconverged steps (if so, look at the next section to add intermediate steps). And ultimately, use an SEM between replica data as main error (you might want to add replica later if needed).

Alternatively, you can reserve a computing node (memory needed) for up to several hours to run **analyse_energies_scamble.py** which instead instead of assuming only 3 combinations of window-wise replica point, will scramble the choice of replica for each window 1000 times and return an average and standard deviation (bootstrapping). After running it in the REC/ and WAT/ folders, go one folder behind and run **analyse_scambled_data.py** to get the summed up results (average dG in receptor minus dG in water with standard deviation for 1000 agains 1000 points (10^6), using the other output from previous script).

**Extracting MD snapshots**

## **5. Add intermediate steps**

## **6. Cleaning up FEP folder**
