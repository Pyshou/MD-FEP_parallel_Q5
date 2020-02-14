set defer_builds_mode, 3
load hexagon.pdb, ini-state
cmd.color("grey70","ini-state")
load hexagon.pdb
hide lines, resn pop
show spheres, hexagon and name n4+p8+na*
set sphere_scale, .2
hide lines, hydro and neighbor element c
sel prot, chain a and hexagon
show cartoon, prot
cmd.spectrum("count",selection="(prot)&e. c")
### If you have a ligand (use for any cofactor) ###
sel lig, hexagon and resn lig
show sticks, lig and not (hydro and neighbor element c)
util.cba(154,"lig",_self=cmd)
cmd.disable('lig')
### End of ligand settings #########
load traj_pymol.xtc, hexagon
cmd.intra_fit("(hexagon) and name ca")
center lig
zoom lig

set auto_zoom, 0
