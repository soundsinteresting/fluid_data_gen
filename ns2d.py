import os
import numpy as np
import fluiddyn as fld
from fluidsim.solvers.ns2d.bouss.solver import Simul

def sim1():
    if "FLUIDSIM_TESTS_EXAMPLES" in os.environ:
        t_end = 1.0
        nh = 16
    else:
        t_end = 10.0
        nh = 64

    params = Simul.create_default_params()

    params.short_name_type_run = "test"

    params.oper.nx = params.oper.ny = nh
    params.oper.Lx = params.oper.Ly = Lh = 10.0

    delta_x = Lh / nh
    params.nu_8 = 2e-3 * params.forcing.forcing_rate ** (1.0 / 3) * delta_x**8

    params.time_stepping.t_end = 10.0
    

    params.init_fields.type = "dipole"

    params.forcing.enable = True
    params.forcing.type = "tcrandom"

    params.output.sub_directory = "../academic/projects/fluid/examples/"
    
    params.output.periods_plot.phys_fields = 0.1
    params.output.periods_save.phys_fields = 0.2
    params.output.periods_save.spatial_means = 0.05

    params.output.ONLINE_PLOT_OK = True

    sim = Simul(params)
    

    # The maximum of rot should be 2
    
    print(sim.output.path_run)
    sim.output.path_run = 'examples/result5'
    #return
    sim.time_stepping.start()

    

if __name__ == "__main__":
    sim1()