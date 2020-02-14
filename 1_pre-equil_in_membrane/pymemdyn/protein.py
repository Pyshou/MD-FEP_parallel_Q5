import os
import shutil
import tempfile

class ProteinComplex(object):
    def __init__(self, *args, **kwargs):
        self.cres = 0 #Central residue
        self.trans = [0, 0, self.cres] #Module for translating complex
        self.n_wats = 0 #Number of experimental waters

        if "monomer" in kwargs.keys():
            self.setMonomer(kwargs["monomer"])
        if "ligand" in kwargs.keys():
            self.setLigand(kwargs["ligand"])
        if "waters" in kwargs.keys():
            self.setWaters(kwargs["waters"])
        if "ions" in kwargs.keys():
            self.setIons(kwargs["ions"])
        if "cho" in kwargs.keys():
            self.setCho(kwargs["cho"])
        if "alosteric" in kwargs.keys():
            self.setAlosteric(kwargs["alosteric"])

    def setMonomer(self, value):
        '''Sets the monomer object'''
        self.monomer = value
    def getMonomer(self):
        return self.monomer
    property(getMonomer, setMonomer)

    def setLigand(self, value):
        '''Sets the ligand object'''
        self.ligand = value
    def getLigand(self):
        return self.ligand
    property(getLigand, setLigand)

    def setWaters(self, value):
        '''Sets the crystal waters object'''
        self.waters = value
    def getWaters(self):
        return self.waters
    property(getWaters, setWaters)

    def setIons(self, value):
        '''Sets the ions object'''
        self.ions = value
    def getIons(self):
        return self.ions
    property(getIons, setIons)

    def setCho(self, value):
        '''Sets the cholesterol object'''
        self.cho = value
    def getCho(self):
        return self.cho
    property(getCho, setCho)

    def setAlosteric(self, value):
        '''Sets the alosteric object'''
        self.alosteric = value
    def getAlosteric(self):
        return self.alosteric
    property(getAlosteric, setAlosteric)

    def set_nanom(self):
        '''Set some meassurements to nanometers, as GROMACS wants'''
        NANOM = 10
        self.gmx_prot_xy = self.prot_xy / NANOM
        self.gmx_prot_z = self.prot_z / NANOM

class Protein(object):
    def __init__(self, *args, **kwargs):
        '''This is a proxy to determine if a protein is a Monomer or a Dimer'''
        self.pdb = kwargs["pdb"]
        if not os.path.isfile(self.pdb):
            raise IOError("File '{0}' missing".format(self.pdb))

    def check_number_of_chains(self):
        '''Determine if a PDB is a Monomer or a Dimer'''
        
        chains = []
        with open(self.pdb, "r") as pdb_fp:
            for line in pdb_fp:
                if (len(line) > 21) and (
                    line.startswith(("ATOM", "TER", "HETATM"))):
                    if (line[21] != " ") and (line[21] not in chains):
                        chains.append(line[21])
    
        if len(chains) < 2:
            return Monomer(pdb = self.pdb)
        elif len(chains) == 2:
            return Dimer(pdb = self.pdb, chains = chains) 

class Monomer(object):
    def __init__(self, *args, **kwargs):
        self.pdb = kwargs["pdb"]
        if not os.path.isfile(self.pdb):
            raise IOError("File '{0}' missing".format(self.pdb))

        self.group = "protlig"
        self.delete_chain()
        self._setHist()

    def delete_chain(self):
        '''PDBs which have a chain column mess up with pdb2gmx, creating
        an unsuitable protein.itp file by naming the protein ie "Protein_A".
        Here we remove the chain value

        According to http://www.wwpdb.org/documentation/format33/sect9.html,
        the chain value is in the column 22'''

        shutil.move(self.pdb, self.pdb + "~")
        pdb = open(self.pdb + "~", "r")
        pdb_out = open(self.pdb, "w")

        replacing = False
        for line in pdb:
            new_line = line
            if len(line.split()) > 2:
                #Remove chain id
                if line[21] != " ":
                    replacing = True
                    new_line = list(line) #Transform the line into a list...
                    new_line[21] = " " 
                    new_line = "".join(new_line)
            pdb_out.write(new_line)

        if replacing: print "Removed chain id from your protein pdb!"
        pdb.close()
        pdb_out.close()
 
        return True

    def _setHist(self):
        '''Change Histidines in pdb to the format preferred by gromacs'''
        tgt = open(self.pdb.replace(".pdb", "-his.pdb"), "w")
        self.pdb_his = tgt.name

        for line in open(self.pdb, "r"):
            if len(line.split()) > 3:
                if line.split()[3] == "HIE":
                    tgt.write(line.replace('HIE ','HISE'))
                elif line.split()[3] == "HID":
                    tgt.write(line.replace('HID ','HISD'))
                elif line.split()[3] == "HIP":
                    tgt.write(line.replace('HIP ','HISH'))
                else:
                    tgt.write(line)
            else:
                tgt.write(line)
        tgt.close()

        return True

class Dimer(Monomer):
    def __init__(self, *args, **kwargs):
        super(Dimer, self).__init__(self, *args, **kwargs)

        self.chains = kwargs.get("chains")
        self.points = dict.fromkeys(self.chains, [])

    def delete_chain(self):
        '''Overload the delete_chain method from Monomer'''
        return True

class Compound(object):
    '''This is a super-class to provide common functions to added compounds'''
    def __init__(self, *args, **kwargs):
        self.check_files(self.pdb, self.itp)

    def check_files(self, *files):
        '''Check if files passed as *args exist'''
        for src in files:
            if not os.path.isfile(src):
                raise IOError("File {0} missing".format(src))

class Ligand(Compound):
    def __init__(self, *args, **kwargs):
        self.pdb = kwargs["pdb"]
        self.itp = kwargs["itp"]
        super(Ligand, self).__init__(self, *args, **kwargs)

        self.group = "protlig"

        self.force_field = kwargs["ff"]

        self.check_forces()

    def check_forces(self):
        '''A force field must give a set of forces that matches every atom in
        the pdb file. This showed particularly important to the ligands, as they
        may vary along a very broad range of atoms'''

        #The itp matches each residue in the ligand pdb with the force field
        atoms_def = False
        molecules = {}
        for line in open(self.itp, "r"):
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
        for line in open(self.force_field, "r"):
            if not line.startswith(";"):
                if (len(line.split()) > 6):
                    #{"TC1": "C1"}
                    atoms[line.split()[0]] = line.split()[1]

        #The pdb have the name of the atom in the third position.
        #Here we cross-check all three files to match their harvested values
        for line in open(self.pdb, "r"):
            data = line.split()
            if len(data) > 6:
                if molecules[data[3]][data[2]] not in atoms.keys():
                    #Some atoms in the pdb has no definition in force field
                    # TODO : add a guessing function
                    print "Atom {0} have no field definition".format(data[1])
                    #return False
                if atoms[molecules[data[3]][data[2]]] not in\
                    molecules[data[3]].keys():
                    print "Atom {0} have a wrong field definition".format(
                        data[1])
                    #return False

        return True

class CrystalWaters(Compound):
    def __init__(self, *args, **kwargs):
        self.pdb = kwargs.get("pdb", "hoh.pdb")
        self.itp = kwargs.get("itp", "hoh.itp")
        super(CrystalWaters, self).__init__(self, *args, **kwargs)

        self.group = "wation"

        self.posre_itp = "posre_hoh.itp"
        self._setITP()
        self._n_wats = self.count_waters()

    def setWaters(self, value):
        '''Sets the crystal waters'''
        self._n_wats = value
    def getWaters(self):
        '''Get the crystal waters'''
        return self._n_wats
    number = property(getWaters, setWaters)

    def count_waters(self):
       '''Count and set the number of crystal waters in the pdb'''
#       return len([x for x in open(self.pdb, "r") if "OW" in x])
       return len([x for x in open(self.pdb, "r") if "HOH" in x])/3

    def _setITP(self):
        '''Create the itp to this structure'''
        s = "\n".join([
            "; position restraints for crystallographic waters (resn HOH)",
            "[ position_restraints ]",
            ";  i funct       fcx        fcy        fcz",
            "   1    1       1000       1000       1000"])

        tgt = open(self.posre_itp, "w")
        tgt.writelines(s)
        tgt.close()

class Ions(Compound):
    def __init__(self, *args, **kwargs):
        self.pdb = kwargs.get("pdb", "ions_local.pdb")
        self.itp = kwargs.get("itp", "ions_local.itp")
        super(Ions, self).__init__(self, *args, **kwargs)

        self.group = "wation"

        self.posre_itp = "posre_ion.itp"
        self._setITP()

        self._n_ions = self.count_ions()

    def setIons(self, value):
        '''Sets the crystal ions'''
        self._n_ions = value
    def getIons(self):
        '''Get the crystal ions'''
        return self._n_ions
    number = property(getIons, setIons)

    def count_ions(self):
       '''Count and set the number of ions in the pdb'''
       ions = ["NA", "CA", "MG", "CL", "ZN"]
       ion_count = 0
       for line in open(self.pdb, "r"):
           if len(line.split()) > 2:
               if line.split()[2] in ions:
                   ion_count += 1
       return ion_count

    def _setITP(self):
        '''Create the itp to this structure'''
        s = "\n".join([
            "; position restraints for ions (resn HOH)",
            "[ position_restraints ]",
            ";  i funct       fcx        fcy        fcz",
            "   1    1       1000       1000       1000"])

        tgt = open(self.posre_itp, "w")
        tgt.writelines(s)
        tgt.close()

class Cholesterol(Compound):
    def __init__(self, *args, **kwargs):
        self.pdb = kwargs.get("pdb", "cho.pdb")
        self.itp = kwargs.get("itp", "cho.itp")
        super(Cholesterol, self).__init__(self, *args, **kwargs)

        self.group = "membr"

        self.check_pdb()
        self._n_cho = self.count_cho()

    def setCho(self, value):
        '''Sets the crystal cholesterol'''
        self._n_cho = value
    def getCho(self):
        '''Get the crystal cholesterols'''
        return self._n_cho
    number = property(getCho, setCho)

    def check_pdb(self):
       '''Check the cholesterol file meet some standards'''
       shutil.move(self.pdb, self.pdb + "~")
       pdb = open(self.pdb + "~", "r")
       pdb_out = open(self.pdb, "w")

       replacing = False
       for line in pdb:
           new_line = line
           if len(line.split()) > 2:
               #Ensure the cholesterol is labeled as CHO
               if line.split()[3] != "CHO":
                   replacing = True
                   new_line = new_line.replace(line.split()[3], "CHO")
           pdb_out.write(new_line)

       if replacing: print "Made some CHO replacements in cho.pdb!"
       pdb.close()
       pdb_out.close()

       return True

    def count_cho(self):
       '''Count and set the number of cho in the pdb'''
       cho_count = 0
       for line in open(self.pdb, "r"):
           if len(line.split()) > 2:
               if line.split()[3] in ["CHO", "CLR"]:
                   cho_count += 1
       return cho_count / 74 #Each CHO has 74 atoms

class Lipids(Compound):
    def __init__(self, *args, **kwargs):
        self.pdb = kwargs.get("pdb", "lip.pdb")
        self.itp = kwargs.get("itp", "lip.itp")
        super(Lipids, self).__init__(self, *args, **kwargs)

        self.group = "membr"

#        self.posre_itp = "posre_lip.itp"
#        self._setITP()

        self._n_lip = self.count_lip()

    def setLip(self, value):
        '''Sets the crystal lipids'''
        self._n_lip = value
    def getLip(self):
        '''Get the crystal lipids'''
        return self._n_lip
    number = property(getLip, setLip)

    def count_lip(self):
       '''Count and set the number of lipids in the pdb'''
       lip_count = []
       for line in open(self.pdb, "r"):
           if len(line.split()) > 2:
               if (line.split()[3] == "LIP" and
                   line.split()[4].isdigit() and
                   line.split()[4] not in lip_count):
                   #Lipid + number + new
                   lip_count.append(line.split()[4])
       return len(lip_count)

    def _setITP(self):
        '''Create the itp to this structure'''
        s = "\n".join([
            "; position restraints for lipids (resn LIP)",
            "[ position_restraints ]",
            ";  i funct       fcx        fcy        fcz",
            "   1    1       1000       1000       1000"])

        tgt = open(self.posre_itp, "w")
        tgt.writelines(s)
        tgt.close()

class Alosteric(Compound):
    '''This is a compound that goes as a ligand but in other place'''
    def __init__(self, *args, **kwargs):
        self.pdb = kwargs["pdb"]
        self.itp = kwargs["itp"]
        super(Alosteric, self).__init__(self, *args, **kwargs)

        self.check_pdb()

        self.force_field = kwargs["ff"]
        self.check_itp()

        self.group = "protlig"

    def check_pdb(self):
       '''Check the alosteric file meet some standards'''
       shutil.move(self.pdb, self.pdb + "~")
       pdb = open(self.pdb + "~", "r")
       pdb_out = open(self.pdb, "w")

       replacing = False
       for line in pdb:
           new_line = line
           if len(line.split()) > 2:
               #Ensure the alosteric compound is labeled as ALO
               if line.split()[3] != "ALO":
                   replacing = True
                   new_line = new_line.replace(line.split()[3], "ALO")
           pdb_out.write(new_line)

       if replacing: print "Made some ALO replacements in %s!" % self.pdb
       pdb.close()
       pdb_out.close()

       return True

    def check_itp(self):
        '''Check the force field is correct'''
        shutil.move(self.itp, self.itp + "~")
        itp = open(self.itp + "~", "r")
        itp_out = open(self.itp, "w")
 
        molecule_type = atoms = False
        for line in itp:
            new_line = line
            if line.startswith("[ moleculetype ]"): molecule_type = True
            if molecule_type:
                if not line.startswith(";"): #Not a comment
                    if len(line.split()) == 2:
                        #Change the user name to "alo"
                        new_line = line.replace(line.split()[0], "alo")
                        molecule_type = False

            if line.startswith("[ "): #Next section (after atoms) reached
                atoms = False
            if line.startswith("[ atoms ]"): atoms = True
            if atoms:
                if not line.startswith(";"):
                    if len(line.split()) > 4:
                        #Change the name of the compound to "ALO"
                        new_line = line.replace(line.split()[3], "ALO")
            itp_out.write(new_line)

        itp.close()
        itp_out.close()
  
        return True
