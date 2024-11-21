import numpy as np
import pandas as pd
from lammpsWithPython.lammps_object import Simulation
import sys

if __name__ == "__main__":

    # To use this file, enter the filename that you want the sim in in the command line python call, like "python confined_d_cone.py [filename]"
    simname = str(sys.argv[1])

    # Init simulation
    sim = Simulation("run", 3, 0.1, 0.03, 0.1)

    # Beam parameters
    beam_stiffness = 10 ** 5
    beam_thickness = 0.003

    # Simulation parameters
    timestep = 0.0000001
    density = 0.01
    viscosity = 0.000001

    # Add beam
    x_position = np.linspace(-0.4, 0.4, 3)
    for x in x_position:
        beam_type, bond_type, angle_type = sim.add_beam(5, np.array([x, 0, 0]),np.array([x, 0, 0]), beam_thickness, beam_stiffness, density)


    # Run simulation
    sim.add_viscosity(viscosity)
    sim.design_dump_files(0.05)
    sim.run_simulation(1)
