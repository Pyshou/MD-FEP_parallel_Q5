import complex
import gromacs
import protein
import queue
import recipes
import membrane

import os, shutil, sys

#Remove all previous files
to_unlink = ["#index.ndx.1#", "#ligand_ha.ndx.1#", "#mdout.mdp.1#",
             "#mdout.mdp.2#",
             "#mdout.mdp.3#",
             "#output.pdb.1#", "#output.tpr.1#",
             "#popc.pdb.1#",
             "#posre.itp.1#", "#proteinopls.pdb.1#", "#proteinopls.pdb.2#",
             "#proteinopls.pdb.3#", "#proteinopls.pdb.4#","#protein.top.1#",
             "#protpopc.pdb.1#", "#protpopc.pdb.2#", "#tmp.pdb.1#",
             "#topol.top.1#", "#topol.top.2#", "#topol.top.3#",
             "#topol.tpr.1#", "#topol.tpr.2#", "#topol.tpr.3#",
             "#topol.tpr.4#", "#water.pdb.1#",
             "protein_ca200.itp", "ffoplsaabon_mod.itp", "ffoplsaa_mod.itp",
             "ffoplsaanb_mod.itp", "GROMACS.log",
             "genion.log", "hexagon.pdb", "index.ndx",
             "ligand_ha.ndx", "mdout.mdp", "min.pdb", "output.pdb",
             "output.tpr",
             "popc.pdb",
             "popc.itp", 
             "posre.itp", "posre_lig.itp", "protein.itp", "protein.top",
             "protein_ca200.itp",
             "proteinopls.pdb",
             "proteinopls-ligand.pdb", "protpopc.pdb", "steep.mdp",
             "traj.xtc", "tmp.pdb", "topol.top", "topol.tpr",
             "Y1_min-his.pdb", "water.pdb"]

dirs_to_unlink = ["Rmin", "eq", "eqCA"]

for target in to_unlink:
    if os.path.isfile(target): os.unlink(target)

for target in dirs_to_unlink:
    if os.path.isdir(target): shutil.rmtree(target)

#sys.exit()
#First we define all parts to be used

monomer = protein.Monomer(pdb = "Y1_min.pdb")
ligand = protein.Ligand(pdb = "lig.pdb", itp = "lig.itp")
membr = membrane.Membrane()
g = gromacs.Gromacs()

#Now we create a complex membrane + protein(s) + ligand

prot_complex = protein.ProteinComplex(monomer = monomer, ligand = ligand)
full_complex = complex.MembraneComplex()
full_complex.complex = prot_complex
full_complex.membrane = membr

#Now we call gromacs to make all the operations

g = gromacs.Gromacs(membrane_complex = full_complex)

#Now we can peek inside any object to look for its properties:
# g.membrane_complex.tpr
# g.membrane_complex.box_height
# g.membrane_complex.complex.monomer.pdb
# g.membrane_complex.complex.ligand.pdb
# g.membrane_complex.membrane.pdb
# g.repo_dir
# ... and so on

#g.run_recipe()

# At this point we should have our hexagon, and the useful files topol.tpr
# to make a minimization with eq.mdp file.
# Through the execution of the recipe we set some new properties:
# g.membrane_complex.trans_box_size
# g.membrane_complex.bilayer_box_size
# g.membrane_complex.embeded_box_size
# g.membrane_complex.protein_box_size
# g.membrane_complex.membrane.bilayer_z
# g.membrane_complex.membrane.lipids_up
# g.membrane_complex.membrane.lipids_down
# g.membrane_complex.membrane.n_wats
# g.membrane_complex.complex.positive_charge
# g.membrane_complex.complex.negative_charge
# g.membrane_complex.complex.prot_xy
# g.membrane_complex.complex.prot_z

#g.run_recipe() #This is the basic recipe (should be explicit?)
#
g.recipe = recipes.MonomerLigandRecipe("debug")
g.run_recipe()
slurm = queue.Slurm()
g.queue = slurm
sys.exit()
#
g.recipe = recipes.BasicMinimization("debug")
g.run_recipe()
#sys.exit()
#
g.recipe = recipes.BasicEquilibration("debug")
g.run_recipe()
#sys.exit()
#
g.recipe = recipes.BasicRelax("debug")
g.run_recipe()
sys.exit()
#
g.recipe = recipes.CAEquilibrate("debug")
g.run_recipe()
