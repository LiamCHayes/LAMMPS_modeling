import numpy as np
import pandas as pd
from lammpsWithPython.lammps_object import Simulation

# Init simulation
sim = Simulation("run", 3, 0.1, 0.03, 0.1)

# Beam parameters
beam_length = 0.05
beam_stiffness = 10 ** 5
beam_thickness = 0.003

# Simulation parameters
timestep = 0.0000001
density = 0.01
viscosity = 0.000001

# Add beam
beam_type, bond_type, angle_type = sim.add_beam(50, np.array([0, 0, -beam_length/2]),np.array([0, 0, beam_length/2]), beam_thickness, beam_stiffness, density)

# Run simulation
sim.add_viscosity(viscosity)
sim.design_dump_files(0.05)
sim.run_simulation(1)
