## **1. Checking data integrity after job completion**

You can use a bash loop like that to list unfinished or problematic simulations:

```for fold in $(ls -d A_to_B/*/md_step*/md_rs*/dc*/); do nb=$(tail $fold/dc*log | grep "terminated normally" | wc -l); if [ $nb -eq 0 ]; then echo $fold" is not finished!"; fi; done```


## **2. Analyzing the data**

**Option 1. Fast but not taking advantage of the possible combinations of replica choices per window**

Inside each REC/ and WAT/ folder, run the enclosed:

```python2 ./analyse_energies.py```

This script after adjusting the paths to the Qfep executable and the input_files/ folder (see enclosed template folder). This folder requires a qfepX.in file for each main transformation step, loading the corresponding energy files sequentially (which means you should have a qfep11.in file there when having 11 lambda windows, i.e. as default in step0), Also, the first column of the third row should corresponding to RT in kcal/mol according to the target temperature in your simulations (here 300K). 

This scripts normally considers up to 9 replica (the CSV output will have several time the same replica-wise value when using less so ignore the duplicated values). the deltadeltaG results will be the average in the receptor minus in water and you can also look for the forward-reverse hysteresis error (forward-reverse) and see from the full_data.csv output if there are unconverged steps (if so, look at the next next section to add intermediate steps). And ultimately, use an SEM between replica data as main error (you might want to add replica later if needed)

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

Inside the main FEP folder, just run:

```bash ./cleanup.sh``` # This will delete files that are not needed anymore, as well as 

## **5. Cleaning up FEP folder**

This is for when you're sure you're done with the data for your FEP and want to free as much space as possible. Inside the main FEP folder, just run:

```bash ./cleanup.sh``` # This will delete files that are not needed anymore and zip energy files, production log files.
