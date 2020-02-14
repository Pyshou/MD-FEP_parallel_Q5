# MD-FEP
https://opm.phar.umich.edu/

fetch PDB_CODE
load Download/XXX.pdb
# Remove nanobody or extra stuff. Usually remove resi 1000-* will do it but it might depend on the numbering in your particular PDB
align PDB_CODE and name CA, XXX and name CA
remove organic
remove resn HOH
remove metal
# Save PDB_CODE object to PDB
# Check that all occupancies are 1.00 in your PDB (otherwise you will need to chose between the rotamers of your amino acid and eliminate the other)

# Mutate receptor back to wild type with the PyMOL Wizzard Mutation Tool (if mutated crystal structure).
https://salilab.org/modeller/download_installation.html # Go there and install modeller
modX.XX add_missing_atoms_modeller.py PDB_CODE.pdb # mod command according to your modeller version
# Output is PDB_CODE_full.pdb

# Reconstruct missing loops if in sphere, using http://open.gpcr-modsim.org/projects/new/ (add missing part to your PDB)

mv 2ydo_full.pdb rec_aligned.pdb

# Generate membrane-inserted system

Option 1. http://open.gpcr-modsim.org/projects/new/
# Upload your PDB
# Run dynamics, can take a day to wait
# Download files and use the unaltered hexagon.pdb full system for next steps

Option 2. Take an already prepared system with closely related protein (Check the Gromacs_templates folder), align yours and insert new coordinates instead and remove clashing elements

Option 3. Run the standalone verison of PyMemDyn (GPCRModSim tool) found here: bash run_tetralith_short.sh (to be fixed to now run on Tetralith with Python compatibility)


# Copy the Restrained_equil_files within the Gromacs_templates folder
# CSB: module load gromacs/2019
# gmx_d, gmx_seq or gmx sometimes
# Extract protein coordinates of full system into protein.pdb (copy and remove other atoms)
gmx_d pdb2gmx -f protein.pdb -o protein_gmx.pdb -ignh -his # Choose OPLS-AA, TIP3P, choose histidine protonations states (can add -glu flag i.e. to neutralize a GLU residue at the membrane interface, or -asp for ASP2.50 for agonist-bound structures)
mv topol.top protein.itp
mv '#topol.top.1#' topol.top
# In protein.itp, rename the object ("Protein_chain_A") in the [ moleculetype ] section to "protein" or at least to match the name in topol.top
# Remove the "#include "oplsaa.ff/forcefield.itp" line as it will be already loaded from the topol.top mother topology
# At the end of the file, remove everything from "; Include Position restraint file" / after the improper section
# Now replace the protein coordinates in the full system PDB file by those of the newly formated protein_gmx.pdb file (generated by pdb2gmx)
# I would typically copy protein_gmx.pdb to a system.pdb file, replace the header by those of the full system's PDB (including box coordinates), remove the TER and ENDMDL lines at the end of system.pdb and:
grep POP hexagon.pdb >> system.pdb
grep SOL hexagon.pdb >> system.pdb
grep CL hexagon.pdb >> system.pdb 
grep NA hexagon.pdb >> system.pdb # If any sodium (and if no chlorine, replace CL by NA in topol.top with the correct number of CL atoms mentioned)
echo "TER" >> system.pdb
echo "ENDMDL" >> system.pdb
# Now adjust the number of POPC lipids, Solvent molecules and ions in the end of topol.top. You can for instance use:
nbPOPatm=$(grep POP system.pdb | wc -l); echo $nbPOPatm"/52"|bc # 52 atoms per lipid
nbSOLatm=$(grep SOL system.pdb | wc -l); echo $nbSOLatm"/3"|bc # 3 atoms per water
grep CL system.pdb | wc -l # CL

# Make a test compiling information for minimization
gmx_d grompp -f minmize.mdp -p topol.top -c system.pdb -o minmize.tpr
# If the charge of the system is not zero, replace ions in the PDB by ions of opposite charge or remove some (also update the count in the end of topol.top). You can also remove hydrogens of a water molecule you identified in a good spot and change the atom and residue names to those of the ions you want to replace it by and place the new ion lines in the ion coordinates part of the PDB. Then update topol.top and check that the charge is neutral after using grompp.

gmx_d make_ndx -f system.pdb -o index.ndx
# Make an index group called "Water_and_ions" as specified in eq.mdp by selecting the index number of "SOL" and "Ion" with "|" between i.e. "16|18" in my case
# Rename it by typing "name 22 Water_and_ions", number 22 being the newly created group in my case
q # To exit and save the index.ndx index file (used for temperature coupling groups in equilibration)

# Make restraints file with high force constant on protein's heavy atoms in all dimensions
gmx_d genrestr -f system.pdb -fc 5000 5000 5000 -n index.ndx -o posre.itp
# Type "2" (Protein's heavy atoms)

# Now compile for minimization with restraints
gmx_d grompp -f minmize.mdp -p topol.top -c system.pdb -r system.pdb -o minmize.tpr

# Run the minimization (can be done on login node in up to few minutes or in parallel using gmx mdrun_mpi / gmx_mpi mdrun.. depending on Gromacs installation)
gmx_d mdrun -s minmize.tpr -deffnm minmize

# Prepare equilibration
gmx_d grompp -f eq.mdp -p topol.top -c minmize.gro -r minmize.gro -o eq.tpr -n index.ndx -maxwarn 1

# Run equilibration in parrallel. Put something like that in your submission script:
gmx_mpi mdrun -s eq.tpr -deffnm eq # On Beskow. PS. Load the coorresponding gromacs module on login node + inside the script first, i.e. gromacs/2019.3 on Beskow

# When done, center trajectory and have a look:
gmx_d trjconv -f eq.gro -s eq.tpr -center -n index.ndx -o eq_centered.pdb # Select group for centering and then for output (i.e. '3' for Calpha, and '0'=everything for output)

# Rename residues to have things clean displayed correctly in PyMOL
gmx editconf -f eq_centered.pdb -resnr 1 -o eq_clean.pdb
