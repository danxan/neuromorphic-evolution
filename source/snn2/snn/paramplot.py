import os
import sys
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.interpolate import CubicSpline, interp1d

import pickle
from datetime import datetime

import pyNN.nest as pynn
from pyNN.random import NumpyRNG, RandomDistribution
from nest import SetKernelStatus
T = os.cpu_count() + 2
SetKernelStatus({'local_num_threads': T})

from pynnGame import Game
from pynnAnimat import Animat
import nodes
from plotutil import plot_paramsfile, find_factors

import multiprocessing

def evaluate(params):
    ni = params['num_inp']
    nh = params['num_hid']
    no = params['num_out']

    outputs = []
    for w in enumerate(params['weights']):

        pynn.setup()
        a = Animat(pop_size=5, input_n=ni, hidden_n=nh, output_n=no)

        a.inp.set_params(params)
        a.hid.set_params(params)
        a.out.set_params(params)

        a.setWeights(w)

        # Set spikes in input nodes
        for n in a.inp.populations:
            n.initialize(v=1)

        pynn.run(33)

        s = 0
        # outputs is linearly dependent on number of output neurons...
        for onode in a.out.populations:
            s += len(onode.get_data(gather=False).segments[0].spiketrains[0].times)
            outputs.append(s)

        pynn.end()

    return outputs




if __name__ == '__main__':

    local_dir = os.path.dirname(__file__)

    # The number of points per parameter
    nt = 5 # tau_m
    ntse = 5 # tau_syn_E
    ntsi = 5 # tau_syn_I

    tau_m = np.random.uniform(low=0.1, high=20, size=(nt,))
    tau_syn_E = np.random.uniform(low=0.1, high=5, size=(ntse,))
    tau_syn_I = np.random.uniform(low=0.1, high=5, size=(ntsi,))

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


    numpoints = nt*ntse*ntsi*nw

    # Parallel
    workers = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(workers)

    # Finding the amount of subplots and the gridspec
    r1, r2 = find_factors(nt)

    print("Plotting {} points".format(numpoints))

    plt_cnt = 0
    id_cnt = 0

    animatlogs = []
    for t in tau_m:
        for tse in tau_syn_E:
            for tsi in tau_syn_I:
                for vr in v_reset:
                    for ere in e_rev_E:
                        for eri in e_rev_I:
                            id_cnt += id_cnt
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
                                    'outputs'   : [],
                                    'num_inp'   : ni,
                                    'num_hid'   : nh,
                                    'num_out'   : no,
                                    'pop_size'  : 5
                                    }
                            for idx in range(nw):
                                w = RandomDistribution('normal', (-5,5)).next(ni*nh+nh*nh+nh*no)
                                params['weights'].append(w)
                                params['mean_w'].append(np.mean(w))

    jobs = []
    for p in animatlogs:
        jobs.append(pool.apply_async(evaluate, (p,)))

    for job in jobs:
        job.wait()
        outputs = job.get()
        p['outputs'] = outputs

    pool.close()
    pool.join()

    # For saving data to file
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y-%b-%d-%H:%M:%S:%f")
    animatlog = 'results/animats_date['+str(timestamp)+']'
    animatlog = os.path.join(local_dir, animatlog)

    with open(animatlog, 'ab') as handle:
        pickle.dump(animatlogs, handle, protocol=pickle.HIGHEST_PROTOCOL)














