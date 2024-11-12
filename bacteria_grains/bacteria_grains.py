import numpy as np
import pandas as pd
from lammpsWithPython.lammps_object import Simulation

# dump DUMPFILE all xyz 100 dump.xyz

sim = Simulation("run", 3, 0.5, 0.5, 0.2)

# Grains
grain_diameter = 0.01
number_of_grains = 40
grains = np.column_stack(((np.random.rand(number_of_grains, 2) - 0.5),np.zeros(number_of_grains)))

grains_type = sim.add_grains(grains, grain_diameter, 0.01)

# Potential
E_grains = 10**6
sim.turn_on_granular_potential(grains_type, grains_type, E_grains)

# Output
sim.design_dump_files(0.05)
sim.run_simulation(1)
