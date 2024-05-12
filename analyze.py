from fluidsim import load_state_phys_file
from netCDF4 import Dataset
import os
import numpy as np
import matplotlib.pyplot as plt

def directory2data(directory):
    ux = []
    uy = []
    rot = []
    b = []
    time = []
    for filename in os.listdir(directory):
        if filename.endswith('.nc'):
            # Construct the full file path
            file_path = os.path.join(directory, filename)
            sim = load_state_phys_file(file_path,hide_stdout=True)
            time.append(float(filename[-11:-3]))
            ux.append(sim.state.get_var('ux'))
            uy.append(sim.state.get_var('uy'))
            rot.append(sim.state.get_var('rot'))
            b.append(sim.state.get_var('b'))
    return ux,uy,rot,b,time

def main():
    #PATH = "../../../Sim_data/examples/NS2D_test_64x64_S10x10_2024-03-12_14-58-50"
    PATH = "dataset/result_01160_h"
    ux,uy,rot,b,time = directory2data(PATH)
    print(ux[0].shape)
    print(uy[0].shape)
    print(rot[0].shape)
    print(time)
    t_arr = np.array(time)
    sorted_indices = np.argsort(t_arr)
    print(sorted_indices)
    

    # Sort the t array
    ux = np.stack(ux)[sorted_indices]
    uy = np.stack(uy)[sorted_indices]
    rot = np.stack(rot)[sorted_indices]
    b = np.stack(b)[sorted_indices]
    N = len(rot)
    fig, axes = plt.subplots(4, N, figsize=(N*4.1, 4 * 4))
    global_min = []
    global_max = []
    for i in range(3):
        global_min.append(min([np.min(d) for d in [rot,ux,uy][i]]))
        global_max.append(max([np.max(d) for d in [rot,ux,uy][i]]))
    for i in range(N):
        dux_dy, dux_dx = np.gradient(ux[i], edge_order=1)
        duy_dy, duy_dx = np.gradient(uy[i], edge_order=1)
        vorticity = dux_dy - duy_dx
        print(vorticity.shape, rot[i].shape)
        n1,n2 = np.linalg.norm(rot[i]),np.linalg.norm(vorticity)
        

        print(np.linalg.norm(rot[i]),np.linalg.norm(vorticity+rot[i]/n1*n2))

        axes[0,i].imshow(-rot[i])
        axes[0,i].axis('off')
        axes[1,i].imshow(ux[i])
        axes[1,i].axis('off')
        axes[2,i].imshow(uy[i])
        axes[2,i].axis('off')
        axes[3,i].imshow(b[i])
        axes[3,i].axis('off')

    plt.savefig('example.png',bbox_inches='tight')
    



def main3():
    PATH = "../../../Sim_data/examples/NS2D_test_64x64_S10x10_2024-03-12_14-58-50/state_phys_t0000.000.nc"
    sim = load_state_phys_file(PATH)
    print('-'*10)
    #times = sim.time_stepping
    #times = sim.output.phys_fields.get_list_times()
    #print(vars(times).items())
    #return
    
    print(sim.state.get_var('ux').shape)
    #print(vars(sim.output.phys_fields.movies.phys_fields.output).items())

def main2():
    directory = r"../../../Sim_data/examples/NS2D_test_64x64_S10x10_2024-03-12_14-58-50/"

    velocity_fields = []

    # Loop over all nc files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.nc'):
            # Construct the full file path
            file_path = os.path.join(directory, filename)
            
            try:
                # Read the netCDF file
                nc_data = Dataset(file_path)

                # Extract the velocity field data
                u = np.array(nc_data.variables['u'][:]) # Assuming 'u' is the name of the variable
                v = np.array(nc_data.variables['v'][:]) # Assuming 'v' is the name of the variable
                velocity_field = (u, v)

                velocity_fields.append(velocity_field)
                
                nc_data.close()
            except Exception as e:
                print("Failed to read {}: {}".format(file_path, e))

    # Now you have a list of velocity fields arrays
if __name__ == "__main__":
    main()
