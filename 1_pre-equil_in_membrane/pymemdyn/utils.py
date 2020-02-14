import inspect
import os
import shutil
from string import Template

import sys

def _arrange_dir(src_dir, new_dir, useful_files=[], useful_fixed=[]):
    '''Copy the files in useful files from src_dir and
    fixed files from self.own_dir to new dir, which is created if needed'''

    if not os.path.isdir(new_dir):
        os.makedirs(new_dir)

    for u_f in [x for x in os.listdir(src_dir) if x in useful_files]:
        src = os.path.join(src_dir, u_f)
        tgt = os.path.join(new_dir, u_f)
        shutil.copy(src, tgt)

    for u_f in [x for x in os.listdir(self.own_dir) if x in useful_fixed]:
        src = os.path.join(self.own_dir, u_f)
        tgt = os.path.join(new_dir, u_f)

        shutil.copy(src, tgt)

    return True

def check_forces(pdb, itp, ffield):
    '''A force field must give a set of forces that matches every atom in
    the pdb file. This showed particularly important to the ligands, as they
    may vary along a very broad range of atoms'''

    #The itp matches each residue in the ligand pdb with the force field
    atoms_def = False
    molecules = {}
    for line in open(itp, "r"):
        if "[ atoms ]" in line:
            atoms_def = True
        if "[ bonds ]" in line:
            atoms_def = False
        if atoms_def and not line.startswith(";"):
            data = line.split()
            if len(data) > 6:
                if data[3] not in molecules.keys(): molecules[data[3]] = {}
                #{"LIG": {"C1": "TC1"},}
                molecules[data[3]][data[4]] = data[1]

    atoms = {}
    #The force field matches each atom in the pdb with one line
    atomtypes = False
    for line in open(ffield, "r"):
        if "[ atomtypes ]" in line:
            atomtypes = True
        if atomtypes:
            #We are inside the atomtypes definition, so add the defined atoms
            if (len(line.split()) > 6):
                #{"TC1": "C1"}
                atoms[line.split()[0]] = line.split()[1]
            
    #The pdb has the name of the atom in the third position.
    #Here we cross-check all three files to match their harvested values
    for line in open(pdb, "r"):
        data = line.split()
        if len(data) > 6:
            if molecules[data[3]][data[2]] not in atoms.keys():
                #Some atoms in the pdb have no definition in force field
                # TODO : add a guessing function
                print "Atom {0} have no field definition".format(data[1])
                #return False
            if atoms[molecules[data[3]][data[2]]] not in\
                molecules[data[3]].keys():
                print "Atom {0} have a wrong field definition".format(data[1])
                #return False

    return True

def clean_all(target_dir = "", exclude = []):
        '''Remove all intermediate files from "target_dir"  except that files in "exclude"'''
        to_unlink_dir = os.path.join(os.getcwd(), target_dir)
        #First a security checkout to not delete up a certain point
        minimum = "/home/gpcruser/public"
        if not to_unlink_dir.startswith(minimum): return False
        if not "dynamic" in to_unlink_dir: return False

        targets = os.listdir(to_unlink_dir)

        for file_name in targets:
            target = os.path.join(to_unlink_dir, file_name)
            if file_name not in exclude:
                #Deleting files
                if os.path.isfile(target): os.unlink(target)
                #Deleting subdirs
                if os.path.isdir(target): shutil.rmtree(target)
            else:
                #Changing remaining files to be downloadable by web user
                os.chmod(target, 0775)
                os.chown(target, -1, 8)

        return True

def clean_topol(src = [], tgt = []):
    '''Clean the src topol of path specifics, and paste results in target'''
    source = open(src, "r")
    target = open(tgt, "w")

    for line in source:
        newline = line
        if line.startswith("#include"):
            newline = line.split()[0] + ' "'
            newline += os.path.split(line.split()[1][1:-1])[1]
            newline += '"\n'
        target.write(newline)

    target.close()
    source.close()

    return True

def concat(**kwargs):
    '''Make a whole pdb file with all the pdb provided'''
#    for compound_class in ["ligand", "waters", "ions", "cho", "alosteric"]:
    for compound_class in ["ligand", "ions", "cho", "alosteric", "waters"]:
        #Does the complex carry the group?
        if hasattr(kwargs["tgt"], compound_class):
            if getattr(kwargs["tgt"], compound_class):
                _file_append(kwargs["src"],
                             getattr(kwargs["tgt"], compound_class).pdb)

def _file_append(f_src, f2a):
    '''Add (concatenate) a f2a pdb file to another src pdb file'''
    src = open(f_src, "r")
    f2a = open(f2a, "r")
    tgt = open("tmp_" + f_src, "w")

    for line in src:
        if ("TER" or "ENDMDL") not in line:
            tgt.write(line)
        else:
            for line_2_add in f2a:
                tgt.write(line_2_add)
            break
    tgt.write("TER\nENDMDL\n")
    tgt.close()
    f2a.close()
    src.close()

    shutil.copy(tgt.name, f_src)

    return True

def make_cat(dir1, dir2, name):
    '''Very tight function to make a list of files to inject 
    in some GROMACS suite programs
    '''
    traj_src = [os.path.join(dir1, name)]
    traj_src.extend([os.path.join(dir1, "{0}", name).format(x)
                     for x in range(800, 0, -200)])
    traj_src.extend([os.path.join(dir2, name)])

    return traj_src

def make_ffoplsaanb(complex = None):
    '''Join all OPLS force fields needed to run the simulation'''
    ff = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                      "templates", "ffoplsaanb_")

    base = "{0}base.itp".format(ff) # This is the ff for proteins and other
    lip = "{0}lip.itp".format(ff)   # This for the lipids
    cho = "{0}cho.itp".format(ff)   # This for cholesterol

    to_concat = []
    if hasattr(complex, "ligand"):
        if hasattr(complex.ligand, "force_field"):
            to_concat.append(complex.ligand.force_field)
    if hasattr(complex, "alosteric"):
        if hasattr(complex.alosteric, "force_field"):
            to_concat.append(complex.alosteric.force_field)
    if hasattr(complex, "cho"):
        to_concat.append(cho)

    to_concat.extend([lip, base])

    output = "[ atomtypes ]\n"
    for ff_i in to_concat:
        output += open(ff_i).read()
        if not output.endswith("\n"): output += "\n"

    open("ffoplsaanb_mod.itp", "w").write(output)

    return True

def make_topol(template_dir = \
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates"),
    target_dir = "",  #Dir where topol.top should land
    working_dir = "", #Dir where script is working
    complex = None):  # The MembraneComplex object to deal
    '''Make the topol starting from our topol.top template'''

#    protein = dimer = lig = hoh = na = cho = alo = 0
#    lig_name = hoh_name = ions_name = cho_name = alosteric_name = ""
    protein = dimer = lig = na = cho = alo = hoh = 0
    lig_name = ions_name = cho_name = alosteric_name = hoh_name = ""
    if hasattr(complex, "monomer"):
        protein = 1
        if getattr(complex, "monomer").__class__.__name__ == "Dimer":
            dimer = 1
    if hasattr(complex, "ligand"):
        if complex.ligand:
            lig = 1
            lig_name = complex.ligand.itp
    if hasattr(complex, "ions"):
        if hasattr(complex.ions, "number"):
            na = complex.ions.number
            ions_name = complex.ions.itp
    if hasattr(complex, "cho"):
        if hasattr(complex.cho, "number"):
            cho = complex.cho.number
            cho_name = complex.cho.itp
    if hasattr(complex, "alosteric"):
        if complex.alosteric:
            alo = 1
            alosteric_name = complex.alosteric.itp
    if hasattr(complex, "waters"):
        if hasattr(complex.waters, "number"):
            hoh = complex.waters.number
            hoh_name = complex.waters.itp


#    order = ("protein", "dimer", "lig", "hoh", "na", "cho", "alo")
    order = ("protein", "dimer", "lig", "na", "cho", "alo", "hoh")
    comps = {"protein": {"itp_name": "protein.itp",
                 "ifdef_name": "POSRES",
                 "posre_name": "posre.itp"},
             "dimer": {"name": "Protein_chain_B",
                 "itp_name": "protein_Protein_chain_B.itp",
                 "ifdef_name": "POSRES",
                 "posre_name": "posre_Protein_chain_B.itp"},
             "lig": {"itp_name": lig_name,
                 "ifdef_name": "POSRESLIG",
                 "posre_name": "posre_lig.itp"},
             "na": {"itp_name": ions_name,
                 "ifdef_name": "POSRESION",
                 "posre_name": "posre_ion.itp"},
             "cho": {"itp_name": cho_name},
                 #"ifdef_name": "POSRESCHO",
                 #"posre_name": "posre_cho.itp"}
             "alo": {"itp_name": alosteric_name,
                 "ifdef_name": "POSRESALO",
                 "posre_name": "posre_alo.itp"},
             "hoh": {"itp_name": hoh_name,
                 "ifdef_name": "POSRESHOH",
                 "posre_name": "posre_hoh.itp"},
             }

    if dimer:
        comps["protein"] = {"name": "Protein_chain_A",
            "itp_name": "protein_Protein_chain_A.itp",
            "ifdef_name": "POSRES",
            "posre_name": "posre_Protein_chain_A.itp"}

    src = open(os.path.join(template_dir, "topol.top"), "r")
    tgt = open(os.path.join(target_dir, "topol.top"), "w")

    t = Template("".join(src.readlines()))
    src.close()

    itp_include = []
    for c in order:
        if locals()[c]:
            itp_name = comps[c]["itp_name"]
            if "posre_name" in comps[c].keys():
                posre_name = comps[c]["posre_name"]
            itp_include.append('#include "{0}"'.format(comps[c]["itp_name"]))
            if "posre_name" in comps[c].keys():
                itp_include.extend(['; Include Position restraint file',
                '#ifdef {0}'.format(comps[c]["ifdef_name"]),
                '#include "{0}"'.format(os.path.join(target_dir,
                    comps[c]["posre_name"])),
                '#endif'])

            if comps[c].has_key("name"):
                comps[c]["line"] = "{0} {1}".format(
                    comps[c]["name"], locals()[c])
            else:
                comps[c]["line"] = "{0} {1}".format(c, locals()[c])
        else:
            comps[c]["line"] = ";"

    if working_dir: working_dir += "/" #Root dir doesn't need to be slashed

    tgt.write(t.substitute(working_dir = working_dir,
                           protein = comps["protein"]["line"],
                           dimer = comps["dimer"]["line"],
                           lig = comps["lig"]["line"],
                           na = comps["na"]["line"],
                           cho = comps["cho"]["line"],
                           alosteric = comps["alo"]["line"],
                           hoh = comps["hoh"]["line"],
                           itp_includes = "\n".join(itp_include)))
    tgt.close()

    return True

def make_topol_lines(itp_name = "",
    ifdef_name = "",
    posre_name = ""):
    '''Make the topol lines to be included'''

    return "\n".join(['#include "{it}"',
        '; Include Position restraint file',
        '#ifdef {id}',
        '#include "{po}"',
        '#endif']).format(it = itp_name,
                          id = ifdef_name,
                          po = posre_name)

def tar_out(src_dir = [], tgt = []):
    '''Tar everything in a src_dir to the tar_file'''
    import tarfile

    t_f = tarfile.open(tgt, mode="w:gz")
    base_dir = os.getcwd()
    os.chdir(src_dir) #To avoid the include of all parent dirs
    for to_tar in os.listdir(os.path.join(base_dir, src_dir)):
        t_f.add(to_tar)
    t_f.close()
    os.chdir(base_dir)

def tune_mdp(groups):
    '''Adjust the tc-groups of eq.mdp to be in line with our system'''
    shutil.move("Rmin/eq.mdp", "Rmin/eq.mdp~")
    eq = open("Rmin/eq.mdp~", "r")
    eq_out = open("Rmin/eq.mdp", "w")
    
    for line in eq:
        new_line = line
        if line.startswith("tc-grps"):
            new_line = line.replace("POP", groups["lipids"])
            new_line = line.replace("wation", groups["solvent"])
            new_line = line.replace("Protein", groups["complex"])
        eq_out.write(new_line)
    eq.close()
    eq_out.close()

    return True
    
