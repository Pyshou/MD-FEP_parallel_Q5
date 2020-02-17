## **1. Checking data integrity after job completion**

You can use a bash loop like that to list unfinished or problematic simulations:

```for fold in $(ls -d A_to_B/*/md_step*/md_rs*/dc*/); do nb=$(tail $fold/dc*log | grep "terminated normally" | wc -l); if [ $nb -eq 0 ]; then echo $fold" is not finished!"; fi; done```


## **2. Analyzing the data**

**Option 1. Fast but not taking advantage of the possible combinations of replica choices per window**

Inside each REC/ and WAT/ folder, run the enclosed script after adjusting the paths to the Qfep executable and the input_files/ folder (see enclosed template folder):

```python2 ./analyse_energies.py```

Note 1: This input_files/ folder requires a qfepX.in file for each main transformation step, loading the corresponding energy files sequentially (which means you should have a qfep11.in file there when having 11 lambda windows, i.e. as default in step0), Also, the first column of the third row should corresponding to RT in kcal/mol according to the target temperature in your simulations (here 300K).

Note 2: This scripts normally considers up to 9 replica (the CSV output will have several time the same replica-wise value when using less so ignore the duplicated values). the deltadeltaG results will be the average in the receptor minus in water and you can also look for the forward-reverse hysteresis error (forward-reverse) and see from the full_data.csv output if there are unconverged steps (if so, look at the next next section to add intermediate steps). And ultimately, use an SEM between replica data as main error (you might want to add replica later if needed)

**Option 2. Slow but smart**

Alternatively, you can reserve a computing node (memory needed) for up to several hours to run:

```python2 ./analyse_energies_scamble.py```

Instead of assuming only 3 combinations of window-wise replica point, the script will scramble the choice of replica for each window 1000 times and return an average and standard deviation (bootstrapping)

After running it in the REC/ and WAT/ folders, go one folder behind and run: 

```python2 ./analyse_scambled_data.py``` # This returns summed up results (average dG in receptor minus dG in water with standard deviation for 1000 agains 1000 points (10^6), using the other output from previous script)

### **3. Extracting MD snapshots**

After adjusting the path to your Qprep excecutable at the beggining of the following scripts, go to the corresponding */md_step*/md_rs*/ folder (replica of step0 of last one) use:

- For extract the last snapshot of an MD trajectory:

```bash ./extract_dc_last_frame.sh dcX PATH_TO_TOPOLOGY_FOLDER/``` # X being the intermediate state number (likely 1 for step0 and 41 for last step to check end states / respective compounds) and the second argument being a path to the folder where you built the corresponding topology for the transformed compound A (should contain a "Forcefield/" folder).

- For extracting average coordinates from an MD trajectory (expect weird structures for flexible parts but good to check what remains very stable or doesn't really move):

```bash ./extract_dc_average.sh dcX PATH_TO_TOPOLOGY_FOLDER/``` # Same syntax.

 - For the last snapshot of the last equilibration step:

```bash ./extract_eq_last_frame.sh dcX PATH_TO_TOPOLOGY_FOLDER/``` # Same syntax.

## **4. Add intermediate steps**

If the forward-reverse hysteresis is too high for a given transfromation step (see option 1 for analyzing the data), you can easily add intemediate states where there is a large gap in free energy difference from analysis using Zwanzig's equation. Go to the corresponding md_step*/ folder and run:

```python ./FEP_converger_v2_multireplica.py``` # This will suggest lambda values in a text file.

- Use a loop, something like that to prepare submission folders:

```i=0; for fold in $(ls -d md_rs*/); do mkdir $fold/New_lambdas; cp -r md_rs1/input_files $fold/New_lambdas/; rm $fold/New_lambdas/input_files/dc*.inp; cp lambdas.txt $fold/New_lambdas/input_files/; cd $fold/New_lambdas/input_files/; PATH_TO_SCRIPTS/make_fep_files_parallell.py -i FEP.in; cd ..; i=$(echo $i+1|bc); $PATH_TO_SCRIPTS/parallel_FEP2_beskow.csh $i911; cd ../..; done``` # Just adapt this (just an idea as usually done, not tried). $i911 is for generating seed number for having different initial velocities for different replica.

- Now make a submission script to run qdyn sequentially on the eq*.inp and dc*.inp files inside the md_rs*/New_lambdas/dc*/ folders (you can use the dirlist folder generated from the scripts inside the above loop).

- When jobs are complete, go to each md_rs*/ folder and run (eventually backup the data somewhere else in case):

```python2 ./DC_reordering.py``` # This will read lambda values inside dc*.inp files to re-order dc*/ folders. Make sure you have them (lost for intermediate states if you have used the next section to cleanup the FEP folder so restore from the input_files/ folder)

- Now, you can re-run the data analysis as before.

## **5. Cleaning up FEP folder**

This is for when you're sure you're done with the data for your FEP and want to free as much space as possible. Inside the main FEP folder, just run:

```bash ./cleanup.sh``` # This will delete files that are not needed anymore and zip energy files as well as production log files
