from get_data import *

from nest import *
from mpi4py import MPI
import neo
import numpy as np
from nest import raster_plot
import matplotlib.pyplot as plt
from datetime import datetime
import pickle
import os

import copy


from nestAnimat import Animat
from nestGenome import Genome

class Game(object):
    def __init__(self, gh=16, gw=8, n_ind=10, n_trials=128):
        self.gh = gh # self.gh
        self.gw = gw # self.gw
        self.n_ind = n_ind # number of individuals per population per generation
        self.n_trials = n_trials # number of trials per individual (max fitness)

    def setup_game(self, comm):
        # Setting random variables, broadcasting
        if Rank() == 0:
            ## Block
            self.blockstates = np.random.randint(0, high=self.gw, size=(self.n_ind, self.n_trials))
            #print("self.blockstates: \n{}".format(self.blockstates))

            self.directions = np.random.randint(-1, high=2, size=(self.n_ind, self.n_trials))
            #print("self.directions: \n{}".format(self.directions))

            self.blocksizes = np.random.randint(1, high=5, size=(self.n_ind, self.n_trials))
            self.blocksizes = self.blocksizes - ((self.blocksizes == 4)+0) - ((self.blocksizes == 2)+0)

            #print("self.blocksizes: \n {}".format(self.blocksizes))

            ## Paddle
            self.paddlestates = np.random.randint(0, high=self.gw, size=(self.n_ind, self.n_trials))
            #print("self.paddlestates: \n{}".format(self.paddlestates))

        else:
            self.blockstates = None
            self.directions = None
            self.blocksizes = None
            self.paddlestates = None

        self.blockstates = comm.bcast(self.blockstates, root=0)
        self.directions = comm.bcast(self.directions, root=0)
        self.blocksizes = comm.bcast(self.blocksizes, root=0)
        self.paddlestates = comm.bcast(self.paddlestates, root=0)

        return self.blockstates, self.directions, self.blocksizes, self.paddlestates

    def run_steps(self, comm, numprocs, no, inds):
        # STEPS
        start = 1.0
        runtime = 33.0
        for step in range(self.gh):
            # Update blockstate
            self.blockstates = (self.blockstates + self.directions)%self.gw

            # Evaluate gamestates
            b_ends = (self.blockstates + self.blocksizes)
            p_left = self.paddlestates-1
            p_right = self.paddlestates+1

            # TODO: VECTORIZE THIS?
            for i in range(self.n_ind):
                for j in range(self.n_trials):
                    SetStatus(inds[i][j].sgs[0], {'spike_times': []})
                    SetStatus(inds[i][j].sgs[1], {'spike_times': []})

                    for u in range(self.blockstates[i][j], b_ends[i][j], 1):

                        if (u%self.gw) == p_left[i][j]%self.gw:
                            SetStatus(inds[i][j].sgs[0], {'spike_times': [start]})

                        if (u%self.gw) == p_right[i][j]%self.gw:
                            SetStatus(inds[i][j].sgs[1], {'spike_times': [start]})

            Simulate(runtime)
            start = start+runtime

            # Collect number of spikes for each spike detector
            ns = np.zeros((self.n_ind, self.n_trials, no)) # this has to be strange in order
            #print("rank {}: before loop ns={}".format(Rank(),ns))
            for i in range(self.n_ind):
                for j in range(self.n_trials):
                    ns[i][j][0] = GetStatus(inds[i][j].sds[0])[0]['n_events']
                    ns[i][j][1] = GetStatus(inds[i][j].sds[1])[0]['n_events']

                    # Clear spike detector
                    SetStatus(inds[i][j].sds[0], {'n_events': 0})
                    SetStatus(inds[i][j].sds[1], {'n_events': 0})

            if Rank() == 0:
                for p in range(1, numprocs):
                    req = comm.irecv(source=p)
                    ns += req.wait()
            else:
                comm.send(ns, dest=0)

            ns = comm.bcast(ns, root=0)

            #print("{} has ns value {}".format(Rank(), ns))

            # MAKE DECISION
            ld = ns[:,:,0] > ns[:,:,1]
            rd = ns[:,:,0] < ns[:,:,1]
            decisions = (rd + 0) - (ld + 0)

            self.paddlestates = (self.paddlestates+decisions)%self.gw
            # END OF STEP

        # END OF STEPS
        return self.blockstates, self.paddlestates

    def last_step(self, comm, inds):
        # Evaluate gamestates
        b_ends = (self.blockstates + self.blocksizes)
        p_left = self.paddlestates-1
        p_right = self.paddlestates+1

        # TODO: VECTORIZE THIS?
        for i in range(self.n_ind):
            for j in range(self.n_trials):
                crash = False
                score = -1

                for u in range(self.blockstates[i][j], b_ends[i][j], 1):
                    for p in range(p_left[i][j], p_right[i][j]+1, 1):
                        crash = (u%self.gw) == (p%self.gw)
                        if crash: break
                    if crash: break

                if crash:
                    if self.blocksizes[i][j] == 1:
                        score = 1
                else:
                    if self.blocksizes[i][j] == 3:
                        score = 1

                inds[i][j].genome.fitness += score

        return inds
