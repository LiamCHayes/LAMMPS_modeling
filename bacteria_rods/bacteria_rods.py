import numpy as np
import pandas as pd
from lammpsWithPython.lammps_object import Simulation

sim = Simulation("run", 3, 0.5, 0.5, 0.2, y_bound="p", x_bound="p", z_bound="f")
timestep = 5 * 10 ** -7

# Rods
beam_length = 0.05
beam_stiffness = 10 ** 5
beam_thickness = 0.03
density = 0.01

beam_type, bond_type, angle_type = sim.add_beam(6, np.array([0, 0, -beam_length/2]),np.array([0, 0, beam_length/2]), beam_thickness, beam_stiffness, density)

# Potential
E_grains = 10**6
sim.turn_on_granular_potential(beam_type, beam_type, E_grains)

# Move things
sim.perturb(beam_type, xdir=0.001, ydir=0.001)

# Output
sim.custom("dump DUMPFILE all xyz 100 dump.xyz")
sim.design_dump_files(0.05)
sim.run_simulation(1, timestep)

