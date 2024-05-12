import os
import numpy as np
import fluiddyn as fld
from fluidsim.solvers.ns2d.bouss.solver import Simul
import sys

def one_simulation(initlist=[],nh=64,save_name='result3',subdir_name="../academic/projects/fluid/dataset/"):  
    params = Simul.create_default_params()
    params.short_name_type_run = "test"
    params.oper.nx = params.oper.ny = nh
    params.oper.Lx = params.oper.Ly = Lh = 10.0

    delta_x = Lh / nh
    params.nu_8 = 2e-3 * params.forcing.forcing_rate ** (1.0 / 3) * delta_x**8
    params.oper.coef_dealiasing = 0.7

    params.time_stepping.t_end = 10.0
    
    if len(initlist) == 0:
        params.init_fields.type = "dipole"

    #params.forcing.enable = True
    #params.forcing.type = "tcrandom"

    params.output.sub_directory = subdir_name
    
    params.output.periods_plot.phys_fields = 0.1
    params.output.periods_save.phys_fields = 0.2
    params.output.periods_save.spatial_means = 0.05

    params.output.ONLINE_PLOT_OK = True

    sim = Simul(params)
    # The maximum of rot should be 2
    if len(initlist) > 0:
        X = sim.oper.X
        Y = sim.oper.Y
        ux = 0*X
        uy = 0*Y
        b = 0* X
        
        for c in range(len(initlist)):
            (x0,y0,amp,bandwidth) = initlist[c][0], initlist[c][1], initlist[c][2], initlist[c][3]
            R2 = (X - x0) ** 2 + (Y - y0) ** 2            
            ux += amp*np.exp(-R2 / bandwidth**2)

            (x0,y0,amp,bandwidth) = initlist[c][4], initlist[c][5], initlist[c][6], initlist[c][7]
            R2 = (X - x0) ** 2 + (Y - y0) ** 2            
            uy += amp*np.exp(-R2 / bandwidth**2)

            (x0,y0,amp,bandwidth) = initlist[c][8], initlist[c][9], initlist[c][10], initlist[c][11]
            R2 = (X - x0) ** 2 + (Y - y0) ** 2            
            b += amp*np.exp(-R2 / bandwidth**2)
        
        #ux[40:60,:10]+=1
        dux_dy, dux_dx = np.gradient(ux, edge_order=1)
        duy_dy, duy_dx = np.gradient(uy, edge_order=1)
        vorticity = dux_dy - duy_dx
        rot = vorticity / np.max(np.abs(vorticity)) 
        
        
        #rot = np.random.randn(X.shape[0], X.shape[1])
        #rot = rot/np.max(np.abs(rot))
        sim.state.init_from_rotb(rot, b)

    sim.output.path_run = save_name
    #sys.stdout = open(os.devnull, 'w')
    sim.time_stepping.start()
    #sys.stdout = sys.__stdout__

def gen_simulations():
    tot_sim = 5000
    for i in range(tot_sim):
        print('-'*10)
        print(i)
        print('-'*10)
        n_source = np.random.randint(2, 6)
        initlist = []
        #(x0,y0,amp,bandwidth) x 3 for ux,uy and b, amp for b should be negative 
        for j in range(n_source):
            
            u = np.random.rand(12)
            tp = [10*u[0],10*u[1],u[2]-0.5,0.5+u[3]*0.5,
                  10*u[4],10*u[5],u[6]-0.5,0.5+u[7]*0.5,
                  10*u[8],10*u[9],-0.2-u[10],0.8+u[3]*0.4]            
            initlist.append(tp)

        one_simulation(initlist=initlist, nh=64, save_name='dataset/result_01%s_h'%i)
        one_simulation(initlist=initlist, nh=32, save_name='dataset/result_01%s_l'%i)


if __name__ == "__main__":
    gen_simulations()