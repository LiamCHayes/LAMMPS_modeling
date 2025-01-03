"""
Use the initializing functions to initialize bacteria in LAMMPS
"""

import numpy as np
import sys

from lammpsWithPython.lammps_object import Simulation
from initialize import get_coords, transform_coords

# To use this file, enter in the terminal "python initialize_in_lammps.py [filename]"
simname = str(sys.argv[1])

# Get data and size of the bacteria tray
data = np.load('./label_fr13.npy')
print(data.shape[1])
print(data.shape[1]/100)
x_size = (data.shape[1] + 10)/100 # add a pad to ensure everything is in bounds
y_size = (data.shape[0] + 10)/100

# Init simulation
sim = Simulation(simname, 3, x_size, y_size, 0.1, x_bound = "p", y_bound = "p", z_bound = "p" )

E_walls = 10 ** 4
sim.add_walls(youngs_modulus = E_walls)

# Beam parameters
beam_length = 0.007
beam_stiffness = 10 ** 5
beam_thickness = 0.003

# Simulation parameters
timestep = 1e-7
density = 0.5
viscosity = 2 * 10 ** -9

# Get bacteria coords
end_points = True
bacteria_lines = get_coords(data, end_points)

# Add beam
sim.turn_on_granular_potential(youngs_modulus = E_walls)
for bacteria_start, bacteria_end in bacteria_lines:
    # Rescale
    bacteria_start = bacteria_start/100
    bacteria_end = bacteria_end/100

    # Transform coordinates
    bacteria_start, bacteria_end = transform_coords(bacteria_start, bacteria_end, x_size, y_size)

    # Place bacteria 
    beam_type, bond_type, angle_type = sim.add_beam(30, bacteria_start, bacteria_end, beam_thickness, beam_stiffness, density)
    sim.turn_on_granular_potential(type1 = beam_type, type2 = beam_type, youngs_modulus = 0)

# Run simulation
sim.add_viscosity(viscosity)
sim.design_dump_files(0.001)
sim.run_simulation(1)