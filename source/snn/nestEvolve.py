from nest import *
from mpi4py import MPI
import neo
import numpy as np
from nest import raster_plot
import matplotlib.pyplot as plt
from datetime import datetime
import pickle
import os


from nestAnimat import Animat
from nestGenome import Genome

P = 56
SetKernelStatus({"total_num_virtual_procs": P,'local_num_threads':1})

comm = MPI.COMM_WORLD
numprocs = NumProcesses()

if __name__ == '__main__':

    ResetKernel()

    scoreMax = []
    scoreMean = []

    # EVOSTATS
    r = 12 # arbitrary mutation rate that affects every mutation linearly
    increase = 0.9 # increase that is scaled exponentially with the rank
    muadj = 10000 # adjustment for weight scale

    num_gen = 3000
    num_trials = 128
    steps = 16
    num_ind = 10
    gamewidth = 8

    # CREATING GENOMES
    ni = 2 # THIS MUST ALWAYS BE 2
    nh = 4
    no = 2 # THIS MUST ALWAYS BE 2

    ps = 5 # Population Size


    #Prepare()
    genomes = []
    for i in range(num_ind):
        if Rank() == 0:
            genomes.append(Genome(id=i, ps=ps, nh=nh))
        else:
            genomes.append(None)

    genomes = comm.bcast(genomes, root=0)

    best_solution = genomes[0]


    starttime = datetime.now()
    for gen in range(num_gen):
        SetKernelStatus({"data_prefix": "generation_"+str(gen)+"_"})
        ResetKernel()

        # Create num_trials in parallel
        inds = []
        for ind in range(num_ind):
            tris = []
            for t in range(num_trials):
                tris.append(Animat(genomes[ind]))
            inds.append(tris)

        # Setting random variables, broadcasting
        if Rank() == 0:
            ## Block
            blockstates = np.random.randint(0, high=16, size=(num_ind, num_trials))
            #print("blockstates: \n{}".format(blockstates))

            directions = np.random.randint(-1, high=2, size=(num_ind, num_trials))
            #print("directions: \n{}".format(directions))

            blocksizes = np.random.randint(1, high=5, size=(num_ind, num_trials))
            blocksizes = blocksizes - ((blocksizes == 4)+0) - ((blocksizes == 2)+0)

            #print("blocksizes: \n {}".format(blocksizes))

            ## Paddle
            paddlestates = np.random.randint(0, high=16, size=(num_ind, num_trials))
            #print("paddlestates: \n{}".format(paddlestates))

        else:
            blockstates = None
            directions = None
            blocksizes = None
            paddlestates = None

        blockstates = comm.bcast(blockstates, root=0)
        directions = comm.bcast(directions, root=0)
        blocksizes = comm.bcast(blocksizes, root=0)
        paddlestates = comm.bcast(paddlestates, root=0)

        # STEP
        start = 1.0
        runtime = 33.0
        for step in range(steps):
            # Update blockstate
            blockstates = (blockstates + directions)%gamewidth

            # Evaluate gamestates
            b_ends = (blockstates + blocksizes)
            p_left = paddlestates-1
            p_right = paddlestates+1

            # TODO: VECTORIZE THIS?
            for i in range(num_ind):
                for j in range(num_trials):
                    SetStatus(inds[i][j].sgs[0], {'spike_times': []})
                    SetStatus(inds[i][j].sgs[1], {'spike_times': []})

                    for u in range(blockstates[i][j], b_ends[i][j], 1):

                        if (u%gamewidth) == p_left[i][j]%gamewidth:
                            SetStatus(inds[i][j].sgs[0], {'spike_times': [start]})

                        if (u%gamewidth) == p_right[i][j]%gamewidth:
                            SetStatus(inds[i][j].sgs[1], {'spike_times': [start]})

            Simulate(runtime)
            start = start+runtime

            # Collect number of spikes for each spike detector
            ns = np.zeros((num_ind, num_trials, no)) # this has to be strange in order
            #print("rank {}: before loop ns={}".format(Rank(),ns))
            for i in range(num_ind):
                for j in range(num_trials):
                    ns[i][j][0] = GetStatus(inds[i][j].sds[0])[0]['n_events']
                    ns[i][j][1] = GetStatus(inds[i][j].sds[1])[0]['n_events']

                    # Clear spike detector
                    SetStatus(inds[i][j].sds[0], {'n_events': 0})
                    SetStatus(inds[i][j].sds[1], {'n_events': 0})

            if Rank() == 0:
                for p in range(1,numprocs):
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

            paddlestates = (paddlestates+decisions)%gamewidth
            # END OF STEP

        # END OF STEPS
        # Evaluate gamestates
        b_ends = (blockstates + blocksizes)
        p_left = paddlestates-1
        p_right = paddlestates+1

        # TODO: VECTORIZE THIS?
        for i in range(num_ind):
            for j in range(num_trials):
                crash = False
                score = -1

                for u in range(blockstates[i][j], b_ends[i][j], 1):
                    for p in range(p_left[i][j], p_right[i][j]+1, 1):
                        crash = (u%gamewidth) == (p%gamewidth)
                        if crash: break
                    if crash: break

                if crash:
                    if blocksizes[i][j] == 1:
                        score = 1
                else:
                    if blocksizes[i][j] == 3:
                        score = 1

                inds[i][j].genome.fitness += score

        # END OF TRIALS

        scores = [g.fitness for g in genomes]
        sort = np.argsort(scores)[::-1]
        scoreMean.append(np.mean(scores))
        scoreMax.append(np.max(scores))

        if  genomes[sort[0]].fitness > best_solution.fitness:
            best_solution = genomes[sort[0]]

        genomes[0].iw = genomes[sort[0]].iw # Best net doesn't change
        genomes[0].hw = genomes[sort[0]].hw # Best net doesn't change
        genomes[0].ow = genomes[sort[0]].ow # Best net doesn't change
        genomes[0].id = genomes[sort[0]].id
        genomes[0].fitness = 0


        for j in range(1, num_ind):
            if Rank() == 0:
                old_genome = genomes[sort[j]]
                old_iw = old_genome.iw
                old_hw = old_genome.hw
                old_ow = old_genome.ow
                liw = np.shape(old_iw)
                lhw = np.shape(old_hw)
                low = np.shape(old_ow)
                # Mutation based on rank, lower rank, more mutation
                new_iw = old_iw + ((np.random.rand(liw[0],liw[1])-0.5)*muadj/(r*increase**j))
                new_hw = old_hw + ((np.random.rand(lhw[0], lhw[1])-0.5)*muadj/(r*increase**j))
                new_ow = old_hw + ((np.random.rand(low[0], lhw[1])-0.5)*muadj/(r*increase**j))
                genomes[j].iw = new_iw
                genomes[j].hw = new_hw
                genomes[j].ow = new_ow
                genomes[j].id = old_genome.id
                genomes[j].fitness = 0
            else:
                genomes = None

            genomes = comm.bcast(genomes, root=0)


        print("Generation {} finished. \n \
            Best solution had fitness {}. \n \
            Best fitness (scoreMax) was {}. \n \
            Mean fitness was {}. \n\
            ".format(gen, best_solution.fitness, scoreMax[-1], scoreMean[-1]))


        timestamp = datetime.now()
        timer = timestamp-starttime
        timestamp = timestamp.strftime("%Y-%b-%d-%H:%M:%S:%f")
        print("Time this took: {}".format(timer))
        print(6)

        results = { 'scoreMax' : scoreMax,
                    'scoreMean': scoreMean,
                    'best_solution': best_solution}

        if Rank() == 0:
            filename = "results/run_np["+str(P)+"g["+str(num_gen)+"]_t["+str(num_trials)+"]_i["+str(num_ind)+"]_bf["+str(best_solution.fitness)+"]_time["+str(timestamp)+"]"
            with open(filename, 'wb') as f:
                pickle.dump(results, f, protocol=pickle.HIGHEST_PROTOCOL)

        # END OF GENERATION

    # END OF GENERATIONS




        # np.logical_or(np.any((bl+p)%10<1), np.any(np.abs(bl-p)<2))


    #Cleanup()

