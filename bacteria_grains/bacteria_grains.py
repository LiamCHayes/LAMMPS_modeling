import numpy as np
import pandas as pd
from lammpsWithPython.lammps_object import Simulation

sim = Simulation("run", 3, 0.5, 0.5, 0.2, y_bound="p", x_bound="p", z_bound="f")
timestep = 5 * 10 ** -7 

# Grains
grain_diameter = 0.1
number_of_grains = 100
grains1 = np.column_stack(((np.random.rand(number_of_grains, 2) - 0.5),np.zeros(number_of_grains)))
grains2 = np.column_stack(((np.random.rand(number_of_grains, 2) - 0.5),np.zeros(number_of_grains)))

grains_type1 = sim.add_grains(grains1, grain_diameter, 0.01)
grains_type2 = sim.add_grains(grains2, grain_diameter, 0.01)

# Potential
E_grains = 10**6
sim.turn_on_granular_potential(grains_type1, grains_type1, E_grains)
sim.turn_on_granular_potential(grains_type2, grains_type2, E_grains)

# Move things
sim.perturb(grains_type1, xdir=0.001, ydir=0.001)
sim.perturb(grains_type2, xdir=-0.001, ydir=-0.001)

# Output
sim.custom("dump DUMPFILE all xyz 100 dump.xyz")
sim.design_dump_files(0.05)
sim.run_simulation(1, timestep)
