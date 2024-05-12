import os
import numpy as np
import matplotlib.pyplot as plt

from analyze import directory2data

def comb_through_time(time,rot,b):
    t_arr = np.array(time)
    sorted_indices = np.argsort(t_arr)    
    rot = np.stack(rot)[sorted_indices]
    b = np.stack(b)[sorted_indices]
    return t_arr, rot, b

def find(t,tlist):
    N = len(tlist)
    for i in range(N):
        if tlist[i] >= t:
            return i-1
        
def lin_interpolate(tid,t,tlist,b):
    return ((t-tlist[tid])*b[tid+1]+(tlist[tid+1]-t)*b[tid])/(tlist[tid+1]-tlist[tid])

def main():
    PATH = 'dataset/'
    
    rotlist_h = []
    blist_h = []
    rotlist_l = []
    blist_l = []
    for filename in os.listdir(PATH):
        if filename.endswith('_h'):
            # low resolution simulation
            ux,uy,rot,b,time = directory2data(PATH+filename)
            time, rot, b = comb_through_time(time,rot,b)
            rotlist_h.append(rot[0])

            
            blist_h.append(np.stack((b[0],b[-1])))

            # low resolution simulation
            ux,uy,rot,b,time = directory2data(PATH+filename[:-1]+'l')
            time, rot, b = comb_through_time(time,rot,b)

            t5id = find(5,time)
            middlerot = lin_interpolate(t5id,5,time,rot)
            rotlist_l.append(middlerot)
            middleb = lin_interpolate(t5id,5,time,b)

            finalb = b[-1]
            blist_l.append(np.stack((b[0],middleb,finalb)))
    name = ['rotlist_h', 'rotlist_l', 'blist_h', 'blist_l']
    dtlist = [rotlist_h,rotlist_l,blist_h,blist_l]
    for i in range(len(dtlist)):
        with open('%s.npy'%name[i], 'wb') as f:
            np.save(f, np.stack(dtlist[i]))

def test_length():
    with open('rotlist_l.npy', 'rb') as f:
        rotlist_l = np.load(f)
        print(rotlist_l.shape)
    with open('rotlist_h.npy', 'rb') as f:
        rotlist_l = np.load(f)
        print(rotlist_l.shape)
    with open('blist_l.npy', 'rb') as f:
        rotlist_l = np.load(f)
        print(rotlist_l.shape)
    with open('blist_h.npy', 'rb') as f:
        rotlist_l = np.load(f)
        print(rotlist_l.shape)
    N = 10
    fig, axes = plt.subplots(1,N, figsize=(N*4., 1* 4))
    print('-'*10)
    for i in range(N):
        print(rotlist_l[i,-1].shape)
        axes[i].imshow(rotlist_l[i,-1])
        axes[i].axis('off')
    plt.savefig('example_series.png',bbox_inches='tight')

if __name__ == "__main__":
    #main()
    test_length()
