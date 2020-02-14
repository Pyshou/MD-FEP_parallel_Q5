pyMEMdyn Version 1.1
================================================================================

pyMEMdyn is  a standalone python  package to setup  membrane molecular
dynamics  calculations  using the  **GROMACS**  set  of programs.  The
package can be  used either in a desktop environment,  or in a cluster
with popular queuing systems such as Torque or Slurm.  


**py-MEMdyn** is hosted in a bitbucket repository at:  

<https://bitbucket.org/gpcrmodsim/pymemdyn.git>  

You can download any version of **py-MEMdyn** by cloning the repository
to your local machine using git.  

You will need to create a free personal account at bitbucket and send
and e-mail to: [gpcruser@gmail.com](gpcruser@gmail.com) and you will be
given access to the free repository.  

To install **py-MEMdyn** follow these steps:  

1.  Clone the current version of **py-MEMdyn**

        git clone https://username@bitbucket.org/gpcrmodsim/pymemdyn.git

    Make sure to change *username* to the one you have created at
    bitbucket.  

2.  The previous command will create a *pymemdyn* directory. Now you
    have to tell your operating system how to find that folder. You
    achieve this by declaring the location of the directory in a .bashrc
    file or .cshrc file in your home folder. An example of what you will
    have to include in your .bashrc file follows:

        export PYMEMDYN=/home/username/software/pymemdyn
        export PATH=$PYMEMDYN:$PATH

    or if your shell is csh then in your .cshrc file you can add:

        setenv PYMEMDYN /home/username/software/pymemdyn
        set path = ($path $PYMEMDYN)

    Notice that I have cloned *pymemdyn* in the software folder in my
    home folder, you will have to adapt this to wherever it is that you
    downloaded your *pymemdyn* to.

    After including the route to your *pymemdyn* directory in your
    .bashrc file make sure to issue the command:

        source .bashrc

    or open a new terminal.

    To check if you have defined the route to the *pymemdyn* directory
    correctly try to run the main program called pymemdyn in a terminal:

        pymemdyn --help

    You should obtain the following help output:

        usage: pymemdyn [-h] [-b OWN_DIR] [-r REPO_DIR] -p PDB [-l LIGAND]
                      [--alo ALOSTERIC] [--waters WATERS] [--ions IONS] [--cho CHO]
                      [-q QUEUE] [--debug]

        == Setup Molecular Dynamics for Membrane Proteins given a PDB. ==

        optional arguments:
          -h, --help       show this help message and exit
          -b OWN_DIR       Working dir if different from actual dir
          -r REPO_DIR      Path to templates of fixed files. If not provided, take the
                           value from settings.REPO_DIR.
          -p PDB           Name of the pdb to insert into MD (mandatory)
          -l LIGAND        Name of the ligand, without extension. Three files must be
                           present along with the molecule pdb: the ligand, its itp
                           and its force field.
          --alo ALOSTERIC  Name of the alosteric interaction, without extension. Three
                           files must be present along with the molecule pdb: the
                           alosteric, its itp and its force field.
          --waters WATERS  Crystalized water molecules. File name without extension.
          --ions IONS      Crystalized ions file name without extension.
          --cho CHO        Crystalized cholesterol molecules file name without
                           extension.
          -q QUEUE         Queueing system to use (slurm, pbs, pbs_ib and svgd
                           supported)
          --debug  

3.  Updates are very easy thanks to the git versioning system. Once
    **py-MEMdyn** has been downloaded into its own *pymemdyn* folder you
    just have to move to it and pull the newest changes:

        cd /home/username/software/pymemdyn
        git pull   

4.  You can also clone older stable versions of **py-MEMdyn**. For
    example the stable version 1.0 which works well and has been tested
    extensively again gromacs version 4.0.5 can be cloned with:

        git clone https://username@bitbucket.org/gpcrmodsim/pymemdyn \
        --branch stable/1.0 --single-branch pymemdyn-1.0

    Now you will have to change your .bashrc or .cshrc files in your
    home folder accordingly.  

5.  To make sure that your gromacs installation is understood by
    **py-MEMdyn** you will need to specify the path to where Gromacs is
    installed in your system. To do this you will need to edit the
    settings.py file with any text editor (“vi” and “emacs” are common
    options in the unix environment). Make sure that only one line is
    uncommented, looking like: GROMACS\_PATH = /opt/gromacs405/bin
    Provided that in your case gromacs is installed in /opt. The program
    will prepend this line to the binaries names, so calling
    “/opt/gromacs405/bin/grompp” should point to that binary.  


### Modeling Modules 

The following modules define the objects to be modelled.

- **protein.py**.  This module defines the ProteinComplex, Protein, Monomer,
Dimer, Compound, Ligand, CrystalWaters, Ions, Cholesterol, Lipids, 
and Alosteric objects. These  objects are  started with  the required files, 
and can then be passed  to other objects.   
- **membrane.py**. Defines the cellular membrane.  
- **complex.py**.  Defines the full complex, protein + membrane.   
  It can  include any  of the previous objects.

### Auxiliary Modules

- **queue.py**.   Queue  manager.  That  is,  it  receives  objects to  be
  executed.   
- **recipes.py**.   Applies  step by  step instructions  for  carrying a 
  modeling  step.  
- **utils.py**.  Puts the  functions done by the previous objects on demand.
  For example, manipulate files, copy  folders, etc.
- **settings.py** This modules sets up the main environment variables needed
  to run the calculation, for example, the path to the gromacs binaries.

### Execution Modules

- **gromacs.py**. Defines the Gromacs and Wrapper objects.  * Gromacs will
  load the  objects to be modeled,  the modeling recipe, and  run it.  *
  Wrapper is a  proxy for gromacs commands. When a  recipe entry is sent
  to it this returns the command to be run.

### Examples

- **example.py**  An example  showing how  to use  the  previously defined
  libraries.

- **pymemdyn** The main program to call which sends the run to a cluster.


Changelog
--------------------------------------------------------------------------------

### Changes from version 1.0 to 1.1

- Tuesday, July 15, 2014

Gromacs 4.6.X internally makes HOH residues belong to both the Water and SOL groups.
This creates a problem with crystal waters which are not recognized as a separate
entity just as, for example, ligands. One fix is to modify the gromacs 
residuetypes.dat file so that the association is forgotten (erased), or, as we 
have done, make sure that HOH and SOL groups generated in pdb's and topologies 
remain continuous. This has forced us to take the waters 
group (which defines crystal waters)  away from the default concat function in 
the **utils.py** module.

- Wednesday, July 9, 2014

Among many changes to get pyMEMdyn up an running with gromacs 4.6.5 instead of
4.0.5 a new substitution for HIE, HID, and HIP is done. Previously the 
substitution was HIE:HISB, HID:HISA, HIP:HISH, now it's HIE:HISE, HID:HISD,
HIP:HISH