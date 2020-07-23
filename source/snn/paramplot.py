import os
import sys
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import pickle
from datetime import datetime

import pyNN.nest as pynn

from pynnGame import Game
from pynnAnimat import Animat
import nodes

def find_factors(number):
    root = np.sqrt(number)
    if int(root) != root:
        r1 = int(root)
        r2 = int(root)+1
    else:
        r1 = int(root)
        r2 = int(root)
    return r1, r2


    

    


if __name__ == '__main__':
    print(find_factors(12))
    pynn.setup()
    local_dir = os.path.dirname(__file__)

    # 100 values between 0 and 1 and 40 elements between 1 and 20
    tau_m = list(np.linspace(0.1,1,3))+list(np.linspace(2,20, 3)) 
    tau_syn_E = list(np.linspace(0.01,1, 2))+list(np.linspace(2,5, 2))
    tau_syn_I = list(np.linspace(0.01,1, 2))+list(np.linspace(2,5, 2))
    
    v_reset = np.linspace(-65, -65, 1)
    e_rev_E = np.linspace(0, 0, 1)
    e_rev_I = np.linspace(0, 0, 1)

    # The number of points per parameter
    nt = 6 # tau_m
    ntse = 4 # tau_syn_E
    ntsi = 4 # tau_syn_I

    # chain of 3 single nodes
    # input is always spiked.
    # for each iteration, all the weights have the same value
    # weights change between iterations
    # all combination of parametersvalues are tested, within set intervals
    a = Animat(pop_size=5, input_n=1, hidden_n=1, output_n=1)
    genome = np.array([  15, 15, 11,   15,  14,  11,   0,   0,   0,  7,  10,   7,   4,
        7,   2,   5,   8,  9,  13,  5, 11,   3,   7,  4,   5,   0,
        6,  2,  4,  14,  9, 15])
    print(genome)
    a.setWeights(genome)

    id_cnt = 0
    

    # For saving data to file
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y-%b-%d-%H:%M:%S:%f")
    animatlog = 'animats_date['+str(timestamp)+']'
    animatlog = os.path.join(local_dir, animatlog)

    animatlogs = []


    numpoints = nt*ntse*ntsi*30

    # Finding the amount of subplots and the gridspec
    r1, r2 = find_factors(nt)

    print("Plotting {} points".format(numpoints))

    plt_cnt = 0

    # Creating figure for plotting 
    fig = plt.figure(constrained_layout=True)
    spec = gridspec.GridSpec(ncols=r2, nrows=r1, figure=fig) 
    for i, t in enumerate(tau_m[:nt]):
        n1 = i%r1
        n2 = i%r2
        ax = fig.add_subplot(spec[n1, n2])
        ax.title.set_text('tau_m='+str(t))
        
        for tse in tau_syn_E[:ntse]:
            for tsi in tau_syn_I[:ntsi]:
                for vr in v_reset[:1]:
                    for ere in e_rev_E[:1]:
                        for eri in e_rev_I[:1]:
                
                            # For each set of parameters, plot weights against spikes
                            outputs = []
                            weights = list(range(-15,15))

                            pynn.setup()
                            a = Animat(pop_size=5, input_n=1, hidden_n=1, output_n=1)
                            a.id = id_cnt
                            id_cnt += 1
                            
                            # Set each combination of parameters
                            cellparams = {
                                'tau_m'     : t,
                                'tau_syn_E' : tse,
                                'tau_syn_I' : tsi,
                                'v_reset'   : vr,
                                'e_rev_E'   : ere,
                                'e_rev_I'   : eri,
                                'id'        : id_cnt
                            }

                            a.inp.set_params(cellparams)
                            a.hid.set_params(cellparams)
                            a.out.set_params(cellparams)

                            #Setting all weights to have the same value
                            for i in weights:
                                plt_cnt += 1
                                print("Plotting point {}/{}".format(plt_cnt, numpoints))

                                w = [i]*(a.num_inp+a.num_hid+a.num_out)
                                a.setWeights(w)

                                
                                # Set spikes in input nodes
                                for n in a.inp.populations:
                                    n.initialize(v=1)

                                pynn.run(50)

                                # outputs is linearly dependent on number of output neurons...
                                for o in a.out.populations:
                                    s = len(o.get_data().segments[0].spiketrains[0].times)
                                    outputs.append(s)

                            alabel = 'Animat ID: '+str(a.id)
                            ax.plot(outputs, weights, label=alabel)
                            ax.legend()
                            animatlogs.append(cellparams)

    # End of a tau_m iteration
    figname = 'paramplot_date['+str(timestamp)+'].svg'
    figname = os.path.join(local_dir, figname)
    fig.savefig(figname)
    with open(animatlog, 'ab') as handle:
        pickle.dump(animatlogs, handle, protocol=pickle.HIGHEST_PROTOCOL)

    plt.show()




                                

                                

                            


                            