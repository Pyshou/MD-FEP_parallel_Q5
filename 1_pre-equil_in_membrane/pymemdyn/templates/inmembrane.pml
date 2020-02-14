#!/usr/bin/python
load hexagon.pdb, initial
load hexagon.pdb, hexagon
load_traj traj_pymol.xtc, hexagon
select waters, resn SOL
select popc, resn POP and hexagon
select gpcr, chain A and hexagon
select initialgpcr, (chain A or resn POP) and initial
select ligand, resn LIG
#select tm1, resi     6-34 and chain A
#select tm2, resi    41-68 and chain A
#select tm3, resi   75-108 and chain A
#select tm4, resi  119-142 and chain A
#select tm5, resi  179-210 and chain A
#select tm6, resi  223-259 and chain A
#select tm7, resi  270-293 and chain A
#select h8, resi   295-310 and chain A

hide everything
intra_fit gpcr

color gray,  initialgpcr
color black, elem c and popc
cmd.spectrum("count",selection="(gpcr)&*/ca")

set cartoon_transparency, 0.5
#set cartoon_trace_atoms, 1, (*CA)

show ribbon, initialgpcr
show lines, popc
show cartoon, gpcr
show sticks, ligand

turn x, -90

deselect

# Improve image ray tracing quality
#set ray_trace_mode, 3
#set antialias, 10

# Make images for movie
#viewport 800,600
#set ray_trace_frames=20
#set cache_frame=0
#mpng mov

# To show a slider in the lower part of the screen uncomment the following lines.
#set movie_panel=1
#movie.add_state_loop(1,0,start=1)
#set movie_panel_row_height, 30
