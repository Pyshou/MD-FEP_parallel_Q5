import os

class BasicInit(object):
    def __init__(self, **kwargs):
        # First we have to make a list of ordered steps
        self.steps = ["pdb2gmx", "set_itp", "concat", "editconf",
                      "set_protein_size", "editconf2", "set_protein_size2",
                      "set_popc", "editconf3", "editconf4", "make_topol",
                      "editconf5", "genbox", "set_water", "editconf6",
                      "editconf7", "genbox2", "count_lipids", "make_topol2",
                      "make_topol_lipids", "make_ffoplsaanb", "set_grompp",
                      "grompp", "trjconv", "get_charge", "genion", "grompp2",
                      "trjconv2", "grompp3", "trjconv3", "set_chains"]

        # And then we have to define each step
        self.recipe = \
        {"pdb2gmx": {"gromacs": "pdb2gmx", #0
          "options": {"src": "",
                      "tgt": "proteinopls.pdb",
                      "top": "protein.top"}},
         "set_itp": {"command": "set_itp", #1
          "options": {"src": "protein.top",
                      "tgt": "protein.itp"}},
         "concat": {"command": "concat",
          "options": {"src": "proteinopls.pdb",
                      "tgt": ""}},
         "editconf": {"gromacs": "editconf", #2
          "options": {"src": "proteinopls.pdb",
                      "tgt": "proteinopls.pdb",
                      "dist": ""}},
         "set_protein_size": {"command": "set_protein_size", #3
          "options": {"src": "proteinopls.pdb",
                      "dir": "xy"}},
         "editconf2": {"gromacs": "editconf", #4
          "options": {"src": "proteinopls.pdb",
                      "tgt": "proteinopls.pdb",
                      "dist": ""}},
         "set_protein_size2": {"command": "set_protein_size", #5
          "options": {"src": "proteinopls.pdb",
                      "dir": "z"}},
         "set_popc": {"command": "set_popc", #6
          "options": {"tgt": "popc.pdb"}},
         "editconf3": {"gromacs": "editconf", #7
          "options": {"src": "proteinopls.pdb",
                      "tgt": "proteinopls.pdb",
                      "box": "",
                      "angles": ["90", "90", "120"],
                      "bt": "tric"}},
         "editconf4": {"gromacs": "editconf", #8
          "options": {"src": "popc.pdb",
                      "tgt": "popc.pdb",
                      "box": ""}},
         "make_topol": {"command": "make_topol",
          "options": {}}, #9
         "editconf5": {"gromacs": "editconf", #10
          "options": {"src": "proteinopls.pdb",
                      "tgt": "proteinopls.pdb",
                      "translate": ["0", "0", "0"]}},
         "genbox": {"gromacs": "genbox", #11
          "options": {"cp": "proteinopls.pdb",
                      "cs": "popc.pdb",
                      "tgt": "protpopc.pdb",
                      "top": "topol.top"}},
         "set_water": {"command": "set_water", #12
          "options": {"tgt": "water.pdb"}},
         "editconf6": {"gromacs": "editconf", #13
          "options": {"src": "water.pdb",
                      "tgt": "water.pdb",
                       "box": ""}},
         "editconf7":{"gromacs": "editconf", #14
          "options": {"src": "protpopc.pdb",
                       "tgt": "protpopc.pdb",
                       "box": "",
                       "angles": ["90", "90", "120"],
                       "bt": "tric"}},
         "genbox2": {"gromacs": "genbox", #15
          "options": {"cp": "protpopc.pdb",
                       "cs": "water.pdb",
                       "tgt": "tmp.pdb",
                       "top": "topol.top"}},
         "count_lipids": {"command": "count_lipids", #16
          "options": {"src": "tmp.pdb",
                       "tgt": "popc.pdb"}},
         "make_topol2": {"command": "make_topol",#17
          "options": {}},
         "make_topol_lipids": {"command": "make_topol_lipids"}, #18
         "make_ffoplsaanb": {"command": "make_ffoplsaanb",
          "options": {}},
         "set_grompp": {"command": "set_grompp", #19
          "options": {"steep.mdp": "steep.mdp",
                       "popc.itp": "popc.itp",
                       #"ffoplsaanb_mod.itp": "ffoplsaanb_mod.itp",
                       "ffoplsaabon_mod.itp": "ffoplsaabon_mod.itp",
                       "ffoplsaa_mod.itp": "ffoplsaa_mod.itp"}},
         "grompp": {"gromacs": "grompp", #20
          "options": {"src": "steep.mdp",
                       "src2": "tmp.pdb",
                       "tgt": "topol.tpr",
                       "top": "topol.top"}},
         "trjconv": {"gromacs": "trjconv", #21
          "options": {"src": "tmp.pdb",
                       "src2": "topol.tpr",
                       "tgt": "tmp.pdb",
                       "pbc": "mol"},
          "input": "1\n0\n"},
         "get_charge": {"command": "get_charge",
          "options": {"src": "steep.mdp",
                       "src2": "tmp.pdb",
                       "tgt": "topol.tpr",
                       "top": "topol.top"}}, #22
         "genion": {"gromacs": "genion", #23
          "options": {"src": "topol.tpr",
                       "src2": "topol.top",
                       "tgt": "output.pdb",
                       "np": "",
                       "nn": ""},
          "input": "SOL\n"},
         "grompp2": {"gromacs": "grompp", #24
          "options": {"src": "steep.mdp",
                       "src2": "output.pdb",
                       "tgt": "topol.tpr",
                       "top": "topol.top"}},
         "trjconv2": {"gromacs": "trjconv", #25
          "options": {"src": "output.pdb",
                       "src2": "topol.tpr",
                       "tgt": "output.pdb",
                       "trans": [],
                       "pbc": "mol"},
          "input": "0\n"},
         "grompp3": {"gromacs": "grompp", #26
          "options": {"src": "steep.mdp",
                       "src2": "output.pdb",
                       "tgt": "topol.tpr",
                       "top": "topol.top"}},
         "trjconv3": {"gromacs": "trjconv", #27
          "options": {"src": "output.pdb",
                       "src2": "topol.tpr",
                       "tgt": "hexagon.pdb",
                       "ur": "compact",
                       "pbc": "mol"},
          "input": "1\n0\n"},
         "set_chains": {"command": "set_chains",#28
          "options": {"src": "proteinopls.pdb"}},
           }

        self.breaks = \
            {"pdb2gmx": {"src": "membrane_complex.complex.monomer.pdb_his"},
             "concat": {"tgt": "membrane_complex.complex"},
             "editconf": {"dist": "membrane_complex.box_height"},
             "editconf2": {"dist": "membrane_complex.box_width"},
             "editconf3": {"box": "membrane_complex.trans_box_size"},
             "editconf4": {"box": "membrane_complex.bilayer_box_size"},
             "editconf6": {"box": "membrane_complex.embeded_box_size"},
             "editconf7": {"box": "membrane_complex.protein_box_size"},
             "genion": {"nn": "membrane_complex.complex.positive_charge",
                        "np": "membrane_complex.complex.negative_charge"},
             "make_topol": {"complex": "membrane_complex.complex"},
             "make_topol2": {"complex": "membrane_complex.complex"},
             "make_ffoplsaanb": {"complex": "membrane_complex.complex"},
             "trjconv2": {"trans": "membrane_complex.complex.trans"}
            }

        if kwargs["debug"] or False:
            self.recipe["set_grompp"]["options"]["steep.mdp"] = "steepDEBUG.mdp"

# This recipe modifies the previous one taking a ligand into account
class LigandInit(BasicInit):
    def __init__(self, **kwargs):
        super(LigandInit, self).__init__(**kwargs)

        self.steps.insert(9, "genrestr_lig")
        self.recipe["genrestr_lig"] =\
            {"gromacs": "genrestr",
             "options": {"src": "",
                         "tgt": "posre_lig.itp",
                         "index": "ligand_ha.ndx",
                         "forces": ["1000", "1000", "1000"]},
             "input": "2\n"}

        self.steps.insert(9, "make_ndx_lig")
        self.recipe["make_ndx_lig"] =\
            {"gromacs": "make_ndx",
             "options": {"src": "",
                         "tgt": "ligand_ha.ndx",
                         "ligand": True},
             "input": "! a H*\nq\n"}

        self.breaks["make_ndx_lig"] =\
            {"src": "membrane_complex.complex.ligand.pdb"}
        self.breaks["genrestr_lig"] =\
            {"src": "membrane_complex.complex.ligand.pdb"}

# This recipe modifies the previous one taking an alosteric into account
class LigandAlostericInit(LigandInit):
    def __init__(self, **kwargs):
        super(LigandAlostericInit, self).__init__(**kwargs)

        self.steps.insert(9, "genrestr_alo")
        self.recipe["genrestr_alo"] =\
            {"gromacs": "genrestr",
             "options": {"src": "",
                         "tgt": "posre_alo.itp",
                         "index": "alosteric_ha.ndx",
                         "forces": ["1000", "1000", "1000"]},
             "input": "2\n"}

        self.steps.insert(9, "make_ndx_alo")
        self.recipe["make_ndx_alo"] =\
            {"gromacs": "make_ndx",
             "options": {"src": "",
                         "tgt": "alosteric_ha.ndx",
                         "alosteric": True},
             "input": "! a H*\nq\n"}

        self.breaks["make_ndx_alo"] =\
            {"src": "membrane_complex.complex.alosteric.pdb"}
        self.breaks["genrestr_alo"] =\
            {"src": "membrane_complex.complex.alosteric.pdb"}

##########################################################################
#                 Minimization                                           #
##########################################################################

class BasicMinimization(object):
    def __init__(self, **kwargs):
        self.steps = ["set_stage_init", "mdrun"]
        self.recipe = {
         "set_stage_init": {"command": "set_stage_init", #0
          "options": {"src_dir": "",
                      "src_files": ["topol.tpr"],
                      "tgt_dir": "Rmin",
                      "repo_files": ["eq.mdp"]}},
         "mdrun": {"gromacs": "mdrun", #1
          "options": {"dir": "Rmin",
                      "src": "topol.tpr",
                      "tgt": "traj.trj",
                      "energy": "ener.edr",
                      "conf": "confout.gro",
                      "log": "md.log"}},
        }
        self.breaks = {}

        if kwargs["debug"] or False:
            self.recipe["set_stage_init"]["options"]["repo_files"] =\
                ["eqDEBUG.mdp"]

class LigandMinimization(BasicMinimization):
    def __init__(self, **kwargs):
        super(LigandMinimization, self).__init__(**kwargs)

class LigandAlostericMinimization(BasicMinimization):
    def __init__(self, **kwargs):
        super(LigandAlostericMinimization, self).__init__(**kwargs)

##########################################################################
#                 Equilibration                                          #
##########################################################################

class BasicEquilibration(object):
    def __init__(self, **kwargs):
        self.steps = ["editconf", "make_ndx", "grompp", "set_stage_init",
                      "set_stage_init2", "mdrun"]
        self.recipe = {
         "editconf": {"gromacs": "editconf", #0
          "options": {"src": "Rmin/confout.gro",
                      "tgt": "min.pdb"}},
         "make_ndx": {"command": "make_ndx", #1
          "options": {"src": "min.pdb",
                      "tgt": "index.ndx"}},
         "grompp": {"gromacs": "grompp", #2
          "options": {"src": "Rmin/eq.mdp",
                      "src2": "min.pdb",
                      "top": "topol.top",
                      "tgt": "topol.tpr",
                      "index":"index.ndx"}},
         "set_stage_init": {"command": "set_stage_init", #3
          "options": {"src_dir": "Rmin",
                      "src_files": ["eq.mdp"],
                      "tgt_dir": "eq"}},
         "set_stage_init2": {"command": "set_stage_init", #4
          "options": {"src_dir": "",
                      "src_files": ["topol.tpr", "posre.itp", "posre_A.itp",
                                   "posre_B.itp", "posre_hoh.itp",
                                   "posre_ion.itp", "posre_lig.itp",
                                   "posre_alo.itp", "posre_cho.itp"],
                      "tgt_dir": "eq"}},
         "mdrun": {"gromacs": "mdrun", #5
          "options": {"dir": "eq",
                      "src": "topol.tpr",
                      "tgt": "traj.trr",
                      "energy": "ener.edr",
                      "conf": "confout.gro",
                      "traj": "traj.xtc",
                      "log": "md_eq1000.log"}},
        }
        self.breaks = {}

        if kwargs["debug"] or False:
            self.recipe["grompp"]["options"]["src"] = "Rmin/eqDEBUG.mdp"
            self.recipe["set_stage_init"]["options"]["src_files"] =\
                ["eqDEBUG.mdp"]

class LigandEquilibration(BasicEquilibration):
    def __init__(self, **kwargs):
        super(LigandEquilibration, self).__init__(**kwargs)
        self.steps.insert(2, "genrestr")
        self.recipe["genrestr"] = \
            {"gromacs": "genrestr",
             "options": {"src": "Rmin/topol.tpr",
                         "tgt": "protein_ca200.itp",
                         "index": "index.ndx",
                         "forces": ["200", "200", "200"]},
             "input": "3\n"}

class LigandAlostericEquilibration(LigandEquilibration):
    def __init__(self, **kwargs):
        super(LigandAlostericEquilibration, self).__init__(**kwargs)
        self.steps.insert(2, "genrestr")
        self.recipe["genrestr"] = \
            {"gromacs": "genrestr",
             "options": {"src": "Rmin/topol.tpr",
                         "tgt": "protein_ca200.itp",
                         "index": "index.ndx",
                         "forces": ["200", "200", "200"]},
             "input": "3\n"}

##########################################################################
#                    Relaxation                                          #
##########################################################################

class BasicRelax(object):
    def __init__(self, **kwargs):
        self.steps = []
        self.recipe = {}
        for const in range(800, 0, -200):
            self.steps.extend(["relax{0}".format(const),
                               "grompp{0}".format(const),
                               "mdrun{0}".format(const)])
            tgt_dir = "eq/{0}".format(const)
            src_dir = "eq"
            self.recipe["relax%d" % const] =\
             {"command": "relax", #0, 3, 6, 9
              "options": {"const": const,
                          "src_dir": src_dir,
                          "tgt_dir": tgt_dir,
                          "posres": [],
                          "mdp": "eq.mdp"}}
            self.recipe["grompp%d" % const] =\
             {"gromacs": "grompp", #1, 4, 7, 10
              "options": {"src": os.path.join(tgt_dir, "eq.mdp"),
                          "src2": os.path.join(src_dir, "confout.gro"),
                          #top": os.path.join(tgt_dir, "topol.top"),
                          "top": "topol.top",
                          "tgt": os.path.join(tgt_dir, "topol.tpr"),
                          "index": "index.ndx"}}
            #TODO ese confout.gro de abaixo hai que copialo, non vale asi
            self.recipe["mdrun%d" % const] =\
             {"gromacs": "mdrun", #2, 5, 8, 11
              "options": {"dir": tgt_dir,
                          "src": "topol.tpr",
                          "tgt": "traj.trr",
                          "energy": "ener.edr",
                          "conf": "../confout.gro",
                          "traj": "traj.xtc",
                          "log": "md_eq{0}.log".format(const)}}
        self.breaks = {}

        if kwargs["debug"] or False:
            for i in [x for x in self.recipe.keys() if x.startswith("relax")]:
                self.recipe[i]["options"]["mdp"] = "eqDEBUG.mdp"

class LigandRelax(BasicRelax):
    def __init__(self, **kwargs):
        super(LigandRelax, self).__init__(**kwargs)
        self.recipe["relax800"]["options"]["posres"].append("posre_lig.itp")

class LigandAlostericRelax(LigandRelax):
    def __init__(self, **kwargs):
        super(LigandAlostericRelax, self).__init__(**kwargs)
        self.recipe["relax800"]["options"]["posres"].append("posre_alo.itp")

##########################################################################
#                    Alpha Chains Relaxation                             #
##########################################################################

class BasicCARelax(object):
    def __init__(self, **kwargs):
        self.steps = ["set_stage_init", "genrestr", "grompp", "mdrun"]
        self.recipe = {
             "set_stage_init": {"command": "set_stage_init", #0
              "options": {"src_dir": "eq",
                          "tgt_dir": "eqCA",
                          "src_files": ["confout.gro"],
                          "repo_files": ["eqCA.mdp"]}},
             "genrestr": {"gromacs": "genrestr", #1
              "options": {"src": "Rmin/topol.tpr",
                          "tgt": "posre.itp",
                          "index": "index.ndx",
                          "forces": ["200"] * 3},
              "input": "3\n"},
             "grompp": {"gromacs": "grompp", #2
              "options": {"src": "eqCA/eqCA.mdp",
                          "src2": "eqCA/confout.gro",
                          "top": "topol.top",
                          "tgt": "eqCA/topol.tpr",
                          "index": "index.ndx"}},
             "mdrun": {"gromacs": "mdrun", #3
              "options": {"dir": "eqCA",
                          "src": "topol.tpr",
                          "tgt": "traj.trr",
                          "energy": "ener.edr",
                          "conf": "confout.gro",
                          "traj": "traj.xtc",
                          "log": "md_eqCA.log"}},
        }

        self.breaks = {}

        if kwargs["debug"] or False:
            self.recipe["set_stage_init"]["options"]["src_files"] =\
                ["confout.gro", "eqDEBUG.mdp"]
            self.recipe["grompp"]["options"]["src"] = "eqCA/eqDEBUG.mdp"

##########################################################################
#                    Collect all results & outputs                       #
##########################################################################
class BasicCollectResults(object):
    def __init__(self, **kwargs):
        '''This recipe navigates through the output of GROMACS, generating and
        collecting various files and logs, and finally putting it all together
        in a tar file.

        Provides list "steps" as the order to execute the recipe.
        dict "recipe" as the variables to pass to funcions.
        dict "breaks" as points where objects calling can put their vars.'''
        self.breaks = {}
        self.steps = ["trjcat", "trjconv", "eneconv", "g_rms", "tot_ener",
            "temp", "pressure", "volume", "set_end", "clean_topol",
            "set_end_2", "set_end_3", "set_end_4", "set_end_5", "set_end_6",
            "tar_it"]#,
            #"final_clean"] This is dangerous, could delete undesired files
        self.recipe = {"trjcat":
            {"gromacs": "trjcat", #1
                "options": {"dir1": "eq",
                    "dir2": "eqCA",
                    "name": "traj.xtc",
                    "tgt": "traj_EQ.xtc"},
                "input": "c\n" * 6},
            "trjconv": {"gromacs": "trjconv", #27
                "options": {"src": "traj_EQ.xtc",
                     "src2": "topol.tpr",
                     "tgt": "traj_out.xtc",
                     "ur": "compact",
                     "pbc": "mol"},
                "input": "1\n0\n"},
            "eneconv": {"gromacs": "eneconv", #2
                "options": {"dir1": "eq",
                    "dir2": "eqCA",
                    "name": "ener.edr",
                    "tgt": "ener_EQ.edr"},
                "input": "c\n" * 6},
            "g_rms": {"gromacs": "g_rms", #3
                "options": {"src": "eq/topol.tpr",
                    "src2": "traj_EQ.xtc",
                    "tgt": "rmsd.xvg"},
                "input": "4\n" * 2},
            "eneconv": {"gromacs": "eneconv", #4
                "options": {"dir1": "eq",
                    "dir2": "eqCA",
                    "name": "ener.edr",
                    "tgt": "ener_EQ.edr"},
                "input": "c\n" * 6},
            "set_end": {"command": "set_stage_init", #9
                "options": {"src_dir": "eqCA",
                    "src_files": ["traj.xtc", "confout.gro", "topol.tpr"],
                    "repo_files": ["popc.itp", "README.md",
                        "prod.mdp"],
                    "tgt_dir": "finalOutput"}},
            "clean_topol": {"command": "clean_topol",
                "options": {"src": "topol.top",
                    "tgt": "finalOutput/topol.top"}},
            "set_end_2": {"command": "set_stage_init", #9
                "options": {"src_dir": "",
                    "src_files": ["ffoplsaa_mod.itp", "ffoplsaabon_mod.itp",
                        "ffoplsaanb_mod.itp", "hexagon.pdb", "protein.itp",
                        "index.ndx", "traj_EQ.xtc", "ener_EQ.edr", "rmsd.xvg",
                        "traj_out.xtc"],
                    "tgt_dir": "finalOutput"}},
            "set_end_3": {"command": "set_stage_init", #9
                "options": {"src_dir": "",
                    "src_files": ["tot_ener.xvg", "tot_ener.log", "temp.xvg",
                        "temp.log", "pressure.xvg", "pressure.log",
                        "volume.xvg", "volume.log"],
                    "tgt_dir": "finalOutput/reports"}},
            "set_end_4": {"command": "set_stage_init", #9
                "options": {"src_dir": "eq",
                    "src_files": ["md_eq1000.log"],
                    "tgt_dir": "finalOutput/logs"}},
            "set_end_5": {"command": "set_stage_init", #9
                "options": {"src_dir": "eq",
                    "src_files": ["{0}/md_eq{0}.log".format(const)
                        for const in range(800, 0, -200)],
                    "tgt_dir": "finalOutput/logs"}},
            "set_end_6": {"command": "set_stage_init", #9
                "options": {"src_dir": "eqCA",
                    "src_files": ["md_eqCA.log"],
                    "tgt_dir": "finalOutput/logs"}},
            "tar_it": {"command": "tar_out",
                "options": {"src_dir": "finalOutput",
                    "tgt": "MD_output.tgz"}},
         #   "final_clean": {"command": "clean_all",
         #       "options": {"target_dir": "",
         #           "exclude": ["MD_output.tgz", "GROMACS.log"]}},
        }

        options = {"tot_ener": "13\n", "temp": "14\n", "pressure": "15\n",
            "volume": "20\n"}
        for option, gro_key in options.iteritems():
            self.recipe[option] =\
                {"gromacs": "g_energy",
                    "options": {"src": "ener_EQ.edr",
                        "tgt": "{0}.xvg".format(option),
                        "log": "{0}.log".format(option)},
                    "input": gro_key}
