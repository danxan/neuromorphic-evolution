import os
import sys
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.interpolate import CubicSpline, interp1d

import pickle
from datetime import datetime

import pyNN.nest as pynn

from pynnGame import Game
from pynnAnimat import Animat
import nodes
from plotutil import plot_paramsfile, find_factors

import parallel

        
if __name__ == '__main__':
    print(find_factors(12))
    pynn.setup()
    local_dir = os.path.dirname(__file__)

    # The number of points per parameter
    nt = 1 # tau_m
    ntse = 1 # tau_syn_E
    ntsi = 1 # tau_syn_I

    tau_m = np.random.uniform(low=20, high=20, size=(nt,))
    tau_syn_E = np.random.uniform(low=5, high=5, size=(ntse,))
    tau_syn_I = np.random.uniform(low=5, high=5, size=(ntsi,))
    
    v_reset = np.linspace(-65, -65, 1)
    e_rev_E = np.linspace(0, 0, 1)
    e_rev_I = np.linspace(-70, -70, 1)

    # Number of random sets of weights to be tested
    nw = 100*60 

    # chain of 3 single nodes
    # input is always spiked.
    # for each iteration, all the weights have the same value
    # weights change between iterations
    # all combination of parametersvalues are tested, within set intervals

    ni = 2 # number of inputs
    nh = 4 # number of hidden
    no = 2 # number of output

    id_cnt = 0
    
    # For saving data to file
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y-%b-%d-%H:%M:%S:%f")
    animatlog = 'animats_date['+str(timestamp)+']'
    animatlog = os.path.join(local_dir, animatlog)

    animatlogs = []


    numpoints = nt*ntse*ntsi*nw

    # Finding the amount of subplots and the gridspec
    r1, r2 = find_factors(nt)

    print("Plotting {} points".format(numpoints))

    plt_cnt = 0

    # Creating figure for plotting 
    fig = plt.figure(constrained_layout=True)
    spec = gridspec.GridSpec(ncols=r2, nrows=r1, figure=fig) 
    for i,t in enumerate(tau_m[:nt]):
        n1 = i%r1
        n2 = i%r2
        ax = fig.add_subplot(spec[n1, n2])
        ax.title.set_text('tau_m='+str(t))
        
        for tse in tau_syn_E[:ntse]:
            for tsi in tau_syn_I[:ntsi]:
                for vr in v_reset[:1]:
                    for ere in e_rev_E[:1]:
                        for eri in e_rev_I[:1]:
                
                            id_cnt += 1
                            # Set each combination of parameters
                            params = {
                                'id'        : id_cnt,
                                'tau_m'     : t,
                                'tau_syn_E' : tse,
                                'tau_syn_I' : tsi,
                                'v_reset'   : vr,
                                'e_rev_E'   : ere,
                                'e_rev_I'   : eri,
                                'weights'   : [],
                                'mean_w'    : [], # mean_w  and outputs are to be plotted against each other
                                'outputs'   : []
                            }
                            
                            for idx in range(nw):
                                pynn.setup()
                                a = Animat(pop_size=5, input_n=ni, hidden_n=nh, output_n=no)
                                a.id = id_cnt

                                a.inp.set_params(params)
                                a.hid.set_params(params)
                                a.out.set_params(params)

                                # For each set of parameters, plot weights against spikes
                                params['weights'].append( np.random.randint(-15, high=15, size=(ni*nh+nh*nh+nh*no)) )
                                params['mean_w'].append( np.mean(params['weights'][-1]) )

                                plt_cnt += 1
                                print("Plotting point {}/{}".format(plt_cnt, numpoints))

                                a.setWeights(params['weights'][-1])

                                # Set spikes in input nodes
                                for n in a.inp.populations:
                                    n.initialize(v=1)

                                pynn.run(33)

                                s = 0
                                # outputs is linearly dependent on number of output neurons...
                                for onode in a.out.populations:
                                    s += len(onode.get_data().segments[0].spiketrains[0].times)
                                params['outputs'].append(s)

                            alabel = 'Animat ID: '+str(a.id)
                            idxa = np.argsort(params['mean_w'])

                            eps = np.linspace(0,0.01,len(params['mean_w']))
                            mean_w = np.array([params['mean_w'][i] for i in idxa])
                            mean_w = mean_w+eps
                            outputs = np.array([params['outputs'][i] for i in idxa])
                            outputs = outputs + 3*np.random.rand(len(outputs))
                            xnew = np.linspace(0,np.max(params['mean_w']), num=1000, endpoint=True)
                            f = interp1d(mean_w, outputs)
                            ax.plot(params['mean_w'], params['outputs'], 'o', xnew, f(xnew), '--')
                            ax.legend(['data', 'cs'])
                            animatlogs.append(params)

    # End of a tau_m iteration
    figname = 'paramplot_date['+str(timestamp)+'].svg'
    figname = os.path.join(local_dir, figname)
    fig.savefig(figname)
    with open(animatlog, 'ab') as handle:
        pickle.dump(animatlogs, handle, protocol=pickle.HIGHEST_PROTOCOL)

    plt.show()

    plot_paramsfile(animatlog)




                                

                                

                            


                            