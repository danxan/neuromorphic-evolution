from nest import *
from mpi4py import MPI
import neo
import numpy as np
from nest import raster_plot
import matplotlib.pyplot as plt
SetKernelStatus({"total_num_virtual_procs": 8,'local_num_threads':2})

comm = MPI.COMM_WORLD
numprocs = NumProcesses()

class Genome(object):
    def __init__(self):


class Animat(object):
    def __init__(self, sgs, sds, genome):
        self.ps = 10# population size / neurons per node
        self.ni = 2 # num input nodes
        self.nh = 4 # num hidden nodes
        self.no = 2 # num output nodes

        self.sgs = sgs
        self.sds = sds

        self.hid = []
        for i in range(self.nh):
            self.hid.append(Create('iaf_cond_exp', self.ps))

        self.out = []
        for i in range(self.no):
            self.out.append(Create('iaf_cond_exp', self.ps))

        for i in range(self.ni):
            for j in range(self.nh):
                syn_dict = {'weight': genome['iw'][i][j]}
                Connect(sgs[i], self.hid[j], syn_spec=syn_dict)

        for i in range(self.nh):
            for j in range(self.nh):
                syn_dict = {'weight': genome['hw'][i][j]}
                Connect(self.hid[i], self.hid[j], syn_spec=syn_dict)

            for j in range(self.no):
                syn_dict = {'weight': genome['ow'][i][j]}
                Connect(self.hid[i], self.out[j], syn_spec=syn_dict)

        for i in range(self.no):
            Connect(self.out[i], sds[i])



generations = 1
trials = 10
steps = 10
num_ind = 10

ResetKernel()
SetKernelStatus({"data_prefix": "generation_0_"})


ni = 2 # THIS MUST ALWAYS BE 2
nh = 4
no = 2 # THIS MUST ALWAYS BE 2

sgs = [None]*num_ind
sds = [None]*num_ind
animats = []
'''
iw = [ [1000.0, -4000.0, 2000.0, -1000.0], [-4000.0, -2000, -1000.0, -2000.0 ] ]
hw = [ [1000.0, -4000.0, 2000.0, -1000.0], [2000.0, -3000.0, 1000.0, -4000.0], [1000.0, -4000.0, 2000.0, -1000.0], [2000.0, -3000.0, 1000.0, -4000.0]]
ow = [ [4000.0, 2000.0], [3000.0, 4000.0], [0.0, 0.0], [0.0, 0.0] ]
iw = [ [1.0, -4.0, 2.0, -1.0], [-4.0, -20.0, -1.0, -2.0 ] ]
hw = [ [1.0, -4.0, 2.0, -1.0], [2.0, -3.0, 1.0, -4.0], [1.0, -4.0, 2.0, -1.0], [2.0, -3.0, 1.0, -4.0]]
ow = [ [4000.0, 2000.0, 1000.0],[4000.0, 2000.0, 1000.0], [4000.0, 2000.0, 1000.0], [4000.0, 2000.0, 1000.0]]
'''
iw = [ [1.0, -4.0, 2.0, -1.0], [-4.0, -20.0, -1.0, -2.0 ] ]
hw = [ [1.0, -4.0, 2.0, -1.0], [2.0, -3.0, 1.0, -4.0], [1.0, -4.0, 2.0, -1.0], [2.0, -3.0, 1.0, -4.0]]
ow = [ [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0] ]
genome = { 'iw': iw,
            'hw': hw,
            'ow': ow }

sgs[0] = []
for j in range(ni):
    sgs[0].append(Create("spike_generator"))
sds[0] = []
for j in range(no):
    sds[0].append(Create("spike_detector"))#, params={"to_file": True}))

animats.append(Animat(sgs[0], sds[0], genome))

'''
iw = [ [1.0, -4.0, 2.0, -1.0], [-4.0, -20.0, -1.0, -2.0 ] ]
hw = [ [1.0, -4.0, 2.0, -1.0], [2.0, -3.0, 1.0, -4.0], [1.0, -4.0, 2.0, -1.0], [2.0, -3.0, 1.0, -4.0]]
ow = [ [4.0, 2], [3.0, 4.0], [0.0, 0.0], [0.0, 0.0] ]
'''

iw = [ [1000.0, 1000.0, 1000.0, 1000.0], [1000.0, 1000, 1000.0, 1000.0 ] ]
hw = [ [1000.0, 1000.0, 1000.0, 1000.0], [1000.0, 1000.0, 1000.0, 1000.0], [1000.0, 1000.0, 1000.0, 1000.0], [1000.0, 1000.0, 1000.0, 1000.0]]
ow = [ [1000.0, 1000.0],[1000.0, 1000.0], [1000.0, 1000.0], [1000.0, 1000.0]]
genome = { 'iw': iw,
            'hw': hw,
            'ow': ow
            'fitness': 0}


for i in range(1,num_ind):
    sgs[i] = []
    for j in range(ni):
        sgs[i].append(Create("spike_generator"))

    sds[i] = []
    for j in range(no):
        sds[i].append(Create("spike_detector"))#, params={"to_file": True}))

    animats.append(Animat(sgs[i], sds[i], genome))


Prepare()

for trial in range(trials):
    start = 1.0
    runtime = 33.0

    # Initialize games
    gamewidth = 16

    # Setting random variables, broadcasting
    if Rank() == 0:
        ## Block
        blockstates = np.random.randint(0, high=15, size=num_ind)

        decision = np.random.randint(-1,1)

        p = np.random.randint(0,1)
        if p == 1:
            blocksize = 1
        else:
            blocksize = 3

        ## Paddle
        paddlestates = np.random.randint(0, high=15, size=num_ind)

    else:
        blockstates = None
        decision = None
        blocksize = None
        paddlestates = None

    blockstates = comm.bcast(blockstates, root=0)
    decision = comm.bcast(decision, root=0)
    blocksize = comm.bcast(blocksize, root=0)
    paddlestates = comm.bcast(paddlestates, root=0)

    print("Rank {}: decision = {}".format(Rank(),decision))

    for i in blockstates:
        i = (i+decision)%gamewidth


    for step in range(steps):
        spikes = [[0]*ni]*num_ind

        # Evaluate gamestates
        for i in range(num_ind):
            bs = blockstates[i] # Start of block
            be = start + blocksize # end of block
            pl = paddlestates[i]-1 # left paddle unit
            pr = paddlestates[i]+1 # right paddle unit

            # TODO: MAKE THIS LOGIC SMARTER
            s = np.zeros(ni) # TODO: THIS REQUIRES A SET NUMBER OF INPUT: 2
            if pl >= bs and pl <= be:
                s[0] = 1
            elif pr >= bs and pr <= be:
                s[1] = 1

            spikes[i] = s

        for i in range(num_ind):
            for j in range(ni):
                if spikes[i][j] == 1:
                    SetStatus(sgs[i][j], {'spike_times': [start]})

        Run(runtime)
        start = start+runtime+1.0

        ns = np.zeros((num_ind, no))
        #print("rank {}: before loop ns={}".format(Rank(),ns))
        for i in range(num_ind):
            spikes = [0]*no
            for k in range(no):
                s = 0
                s = len(GetStatus(sds[i][k], 'events')[0]['times'])
                #print("hey! i={}, k={}, s={}".format(i,k,s))
                spikes[k] = float(s)

                SetStatus(sds[i][k], {'n_events': 0})
            ns[i] = spikes


        if Rank() == 0:
            for p in range(1,numprocs):
                req = comm.irecv(source=p)
                ns += req.wait()
        else:
            comm.send(ns, dest=0)

        if Rank() == 0:
            for p in range(1,numprocs):
                comm.send(ns, dest=p)
        else:
            req = comm.irecv(source=0)
            ns = req.wait()

        #print("{} has ns value {}".format(Rank(), ns))

        # MAKE DECISION
        for i, s in enumerate(ns):
            decision = 0
            if s[0] < s[1]:
                decision = 1
            elif s[0] > s[1]:
                decision = -1

            paddlestates[i] = (paddlestates[i]+decision)%gamewidth

        print("Rank {} has blockstates {}".format(Rank(),blockstates))
        print("Rank {} has paddlestates {}".format(Rank(),paddlestates))



Cleanup()

'''
    ResetKernel()
    SetKernelStatus({"data_prefix": "generation_1_"})

sgs = []
sds = []
animats = []
w = [ [100.0, 40.0, 200.0, 10.0], [20.0, 30.0, 100.0, 40.0], [10.0, 40.0, 20.0, 100.0], [20.0, 30.0, 100.0, 40.0]]
for i in range(10):
    sgs.append(Create("spike_generator", params={"spike_times": [1.0]}))
    sds.append(Create("spike_detector", params={"to_file": True}))
    animats.append(Animat(sgs[i], sds[i], genome))

Simulate(100.0)

spikes = [1,0,1,0,1,1,1,0,1,0]

for i in range(10):
    if spikes[i] == 1:
        SetStatus(sgs[i], {'spike_times': [101.0]})
    elif spikes[i] == 0:
        print("do not set stimulus")


Simulate(100.0)

for sg in sgs:
    print(GetStatus(sg))

'''

