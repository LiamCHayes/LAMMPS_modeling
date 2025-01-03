# Simulate Bacteria in LAMMPS

Here are the useful scripts that I've been able to make. I have some code to initialize a simulation from data and a small example of how to add a rod to the simulation. 

LAMMPS is pretty particular about how it wants the simulation to be set up. Most of the time it is solved by tweaking some parameter like density, viscosity, or a potential. This just involves a lot of trial and error.

[LAMMPSStructures](https://github.com/dpholmes/LAMMPSStructures/blob/main/Documentation.md) in Python is helpful to develop the simulation, but for debugging I also found it helpful to understand the actual LAMMPS code. For LAMMPS errors that don't involve tweaking parameters, this is the process that I found to work best:
1. Look up the error in some kind of AI
2. Find the problem code in both the Python script and LAMMPS script
3. Find a solution in the LAMMPS script that makes it work
4. Find a mirror solution in the Python script using LAMMPSStructures

When you start using NUFEB, there are a few things that might be helpful. Most of the errors when running their example scrips can be solved by replacing their dump command with the default dump command from LAMMPSStructures. This also makes it possible to see the same type of visualization in OVITO. Also, if you are using a virtual environment for your LAMMPS installation, deactivate that before you use the NUFEB version of LAMMPS to avoid undefined atom types.

### `initialize_from_data`
This folder contains the code to initialize the LAMMPS simulation from the bacteria location data provided by Prof. Dunlop. 

`label_fr13.npy` - Bacteria location data from Prof. Dunlop

`initialize.py` - The code to go from bacteria location data to LAMMPS locations

`initialize_in_lammps.py` - Example code using functions from `initialize.py` to create a LAMMPS simulation

`run` - Output of `initialize_in_lammps.py`

### `simple_rod`
Example script to add a single rod to the simulation. For some reason, when adding rods in a for loop you need to turn on and off a granular potential before and after you add each rod. See `initialize_in_lammps.py` for an example.
