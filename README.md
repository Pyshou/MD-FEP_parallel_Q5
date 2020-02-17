# MD-FEP

Relative Binding Free Energy Calculations with the OPLS-AA Force Field. Check each sub-folder depending on what you need to do (from step 1 for a new project)

This is the way I do things and of course there are always alternatives. An advantage we have over the mainstream way of running MD/FEP simulations is that we sample all intermediate states of a given transfromation in parallel, which reduces the potential trapping into low energy regions of intermediate states leading to wrong sampling of the last state (compound) and then likely gives convergence with a much smaller number of replica. This also gives us results fast, allows us to extend production runs for different windows and also to just add extra intermediate states when needed to converge the results

All this might seem detailed but unless you have someone to show you how to do everything, you will need to pay attention to all these details. When you get used to these steps, this will become like a routine and you might likely be able to setup up to a few FEPs per day once your system is set up (and get results the next day if you're lucky with supercomputers).

Some steps could definitely be semi-automated further but one always needs to pay attention to little things that could screw up your simulations if you are not careful!

I would advice running MD/FEP calculations on a set of closely-related known ligands first to see if you can replicate experimental binding free energies with your system and simulation setup first.
