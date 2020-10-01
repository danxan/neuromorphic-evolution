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
from nestGame import Game

def create_genomes(comm, num_ind):
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

    mean_smax = 0

    return genomes, best_solution, mean_smax

def load_solutions(filename, comm, num_ind):
    ''' loads top five solutions, until num_ind '''
    #assert 5%num_ind == 5 or 5%num_ind == 0, "num ind must be a multiple of 5"
    genomes = []
    if Rank() == 0:
        log = get_data(filename)
        best_solution = log['best_solution']
        genomes = log['top_solutions']
        if len(genomes) >= num_ind:
            genomes = genomes[0:num_ind]
        else:
            for i in range(num_ind):
                genomes.append(copy.deepcopy(genomes[i%num_ind]))

        mean_smax = np.mean(log['scoreMax'])

    else:
        genomes.append(None)
        best_solution = None

        mean_smax = None

    genomes = comm.bcast(genomes, root=0)
    best_solution = comm.bcast(best_solution, root=0)

    mean_smax = comm.bcast(mean_smax, root=0)
    print("MEAN SMAX: {}".format(mean_smax))

    return genomes, best_solution, mean_smax

def setup_game(comm, gamewidth, num_ind, num_trials):
    # Setting random variables, broadcasting
    if Rank() == 0:
        ## Block
        blockstates = np.random.randint(0, high=gamewidth, size=(num_ind, num_trials))
        #print("blockstates: \n{}".format(blockstates))

        directions = np.random.randint(-1, high=2, size=(num_ind, num_trials))
        #print("directions: \n{}".format(directions))

        blocksizes = np.random.randint(1, high=5, size=(num_ind, num_trials))
        blocksizes = blocksizes - ((blocksizes == 4)+0) - ((blocksizes == 2)+0)

        #print("blocksizes: \n {}".format(blocksizes))

        ## Paddle
        paddlestates = np.random.randint(0, high=gamewidth, size=(num_ind, num_trials))
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

    return blockstates, directions, blocksizes, paddlestates

def run_steps(comm, numprocs, gameheight, num_ind, num_trials, no, blockstates, blocksizes, paddlestates, directions, gamewidth, inds):
    # STEPS
    start = 1.0
    runtime = 33.0
    for step in range(gameheight):
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
    return blockstates, paddlestates

def last_step(comm, blockstates, blocksizes, paddlestates, num_ind, num_trials, gamewidth, inds):
    # evaluate gamestates
    b_ends = (blockstates + blocksizes)
    p_left = paddlestates-1
    p_right = paddlestates+1

    # todo: vectorize this?
    for i in range(num_ind):
        for j in range(num_trials):
            crash = False
            score = 0

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

    return inds


def test_top_solutions(comm, numprocs, top_solutions, num_tests, num_ind, num_trials, gameheight, gamewidth):
    no = 2
    scores = np.zeros((num_tests, num_ind))
    # AVERAGING TESTS
    for test in range(num_tests):
        ResetKernel()
        inds = []
        for ind in range(num_ind):
            top_solutions[ind].fitness = 0
            tris = []
            for t in range(num_trials):
                tris.append(Animat(top_solutions[ind]))
            inds.append(tris)

        # TRIALS
        #game = Game(gh=gameheight, gw=gamewidth, n_ind=num_ind, n_trials=num_trials)
        #blockstates, directions, blocksizes, paddlestates = setup_game(comm, gamewidth, num_ind, num_trials)
        # setup game
        # Setting random variables, broadcasting
        if Rank() == 0:
            ## Block
            blockstates = np.random.randint(0, high=gamewidth, size=(num_ind, num_trials))
            #print("blockstates: \n{}".format(blockstates))

            directions = np.random.randint(-1, high=2, size=(num_ind, num_trials))
            #print("directions: \n{}".format(directions))

            blocksizes = np.random.randint(1, high=5, size=(num_ind, num_trials))
            blocksizes = blocksizes - ((blocksizes == 4)+0) - ((blocksizes == 2)+0)

            #print("blocksizes: \n {}".format(blocksizes))

            ## Paddle
            paddlestates = np.random.randint(0, high=gamewidth, size=(num_ind, num_trials))
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

        #blockstates, paddlestates = run_steps(comm, numprocs, gameheight, num_ind, num_trials, no, blockstates, blocksizes, paddlestates, directions, gamewidth, inds)
        # run steps
        # STEPS
        start = 1.0
        runtime = 33.0
        for step in range(gameheight):
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

        #inds = last_step(comm, blocksizes, paddlestates, num_ind, num_trials, gamewidth, inds)
        # last step
        # evaluate gamestates
        b_ends = (blockstates + blocksizes)
        p_left = paddlestates-1
        p_right = paddlestates+1

        # TODO: VECTORIZE THIS?
        for i in range(num_ind):
            for j in range(num_trials):
                crash = False
                score = 0

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
        for i in range(num_ind):
            for j in range(num_trials):
                scores[test][i] = inds[i][j].genome.fitness

    mean_scores = np.mean(scores, axis=0)
    print("Mean scores:\n {}".format(mean_scores))
    argsort_ms = np.argsort(mean_scores)[::-1]
    print("Sorted mean_scores: \n{}".format(argsort_ms))

    return scores, mean_scores, argsort_ms

def test_solution_parallel():
    P = 56
    SetKernelStatus({"total_num_virtual_procs": P,'local_num_threads':1})

    comm = MPI.COMM_WORLD
    numprocs = NumProcesses()


    ResetKernel()

    scoreMax = []
    scoreMean = []

    # EVOSTATS
    r = 12 # arbitrary mutation rate that affects every mutation linearly
    increase = 0.9 # increase that is scaled exponentially with the rank
    muadj = 1 # adjustment for weight scale

    num_gen = 1
    num_trials = 128
    gameheight = 16
    num_ind = 1
    gamewidth = 8

    # CREATING GENOMES
    ni = 2 # THIS MUST ALWAYS BE 2
    nh = 4
    no = 2 # THIS MUST ALWAYS BE 2

    ps = 5 # Population Size


    log = get_data()
    best_solution = log['best_solution']
    genomes = []
    genomes.append(best_solution)


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
        for step in range(gameheight):
            spikes = np.zeros((num_ind, num_trials, ni))

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
                score = 0

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

        print("Generation {} finished. \n \
            Best solution had fitness {}. \n \
            Best fitness (scoreMax) was {}. \n \
            Mean fitness was {}. \n\
            ".format(gen, best_solution.fitness, scoreMax[-1], scoreMean[-1]))

def test_solution():
    ResetKernel()
    print("Testing solution: ")
    log = get_data()

    bso = log['best_solution']

    gw = 8
    gh = 16

    pp = 4
    bp = 0


    ni = 2
    nh = 4
    no = 2

    trials = 128
    animats = []
    for i in range(trials):
        animats.append(Animat(bso))

    di = np.random.randint(-1,high=2, size=(trials)) # direction
    p = np.random.randint(0,high=2, size=(trials)) # probability for task

    pp = np.random.randint(0, high=15, size=(trials)) # paddle position

    bp = np.random.randint(0, high=15, size=(trials)) # block position

    bs = np.random.randint(1, high=5, size=(trials))
    bs = bs - ((bs == 4)+0) - ((bs == 2)+0) # block size

    start = 1.0
    runtime = 33.0
    # STEP
    for i in range(gh):
        be = bp + bs
        pl = pp - 1
        pr = pp + 1

        for j in range(trials):
            for bu in range(bp[j], be[j], 1):
                SetStatus(animats[j].sgs[0], {'spike_times': []})
                SetStatus(animats[j].sgs[1], {'spike_times': []})
                if bu == pl[j]:
                    SetStatus(animats[j].sgs[0], {'spike_times': [start]})
                elif bu == pr[j]:
                    SetStatus(animats[j].sgs[1], {'spike_times': [start]})


        Simulate(33.0)
        start = start+runtime

        # Collect number of spikes for each spike detector
        ns = np.zeros((trials, no)) # this has to be strange in order
        #print("rank {}: before loop ns={}".format(Rank(),ns))
        for j in range(trials):
            ns[j][0] = GetStatus(animats[j].sds[0])[0]['n_events']
            ns[j][1] = GetStatus(animats[j].sds[1])[0]['n_events']

            # Clear spike detector
            SetStatus(animats[j].sds[0], {'n_events': 0})
            SetStatus(animats[j].sds[1], {'n_events': 0})

        # MAKE DECISION
        ld = ns[:,0] > ns[:,1]
        rd = ns[:,0] < ns[:,1]
        decisions = (rd + 0) - (ld + 0)

        pp = (pp+decisions)%gw
        # END OF STEP

    be = bp + bs
    pl = pp - 1
    pr = pp + 1

    # last step
    bso.fitness = 0
    for i in range(trials):
        score = 0
        crash = False
        for bu in range(bp[i], be[i]):
            for pu in range(pl[i], pr[i]+1):
                crash = (bu%gw) == (pu%gw)
                if crash:
                    break
            if crash:
                break

        if crash:
            if bs[i] == 1:
                score = 1
        else:
            if bs[i] == 3:
                score = 1

        bso.fitness += score

    print(bso.fitness)

def test_solution2():
    P = 56
    SetKernelStatus({"total_num_virtual_procs": P,'local_num_threads':1})

    comm = MPI.COMM_WORLD
    numprocs = NumProcesses()

    ResetKernel()

    scoreMax = []
    scoreMean = []

    # EVOSTATS
    r = 12 # arbitrary mutation rate that affects every mutation linearly
    increase = 0.9 # increase that is scaled exponentially with the rank
    muadj = 10000 # adjustment for weight scale

    num_gen = 500
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
    best_solution = None
    for i in range(num_ind):
        if Rank() == 0:
            log = get_data()
            best_solution = log['best_solution']
            best_solution.fitness = 0
            genomes.append(best_solution)

        else:
            genomes.append(None)

    genomes = comm.bcast(genomes, root=0)
    best_solution = comm.bcast(best_solution, root=0)


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
            spikes = np.zeros((num_ind, num_trials, ni))

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
                score = 0

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



        results = { 'scoreMax' : scoreMax,
                    'scoreMean': scoreMean,
                    'best_solution': best_solution}


        timestamp = datetime.now()
        timer = timestamp-starttime
        timestamp = timestamp.strftime("%Y-%b-%d-%H:%M:%S:%f")
        print("Time this took: {}".format(timer))
        print(6)

        results = { 'scoreMax' : scoreMax,
                    'scoreMean': scoreMean,
                    'best_solution': best_solution}

        if Rank() == 0:
            filename = "results/run_np["+str(P)+"g["+str(gen)+"]_t["+str(num_trials)+"]_i["+str(num_ind)+"]_bf["+str(best_solution.fitness)+"]_time["+str(timestamp)+"]"
            with open(filename, 'wb') as f:
                pickle.dump(results, f, protocol=pickle.HIGHEST_PROTOCOL)
        # END OF GENERATION

    # END OF GENERATIONS




        # np.logical_or(np.any((bl+p)%10<1), np.any(np.abs(bl-p)<2))


    #Cleanup()

def run_generations(comm, numprocs, num_gen, num_ind, num_trials, gameheight, gamewidth, genomes, best_solution, mean_smax):
    genomes = genomes
    best_solution = best_solution
    mean_smax = mean_smax

    scoreMax = []
    scoreMean = []

    # EVOSTATS
    r = 12 # arbitrary mutation rate that affects every mutation linearly
    increase = 1.1 # increase that is scaled exponentially with the rank
    muadj = 1 # adjustment for weight scale

    ni = 2
    nh = 4
    no = 2

    ps = 5 # Population Size

    top_solutions = []

    starttime = datetime.now()
    gen = 0

    for gen in range(num_gen):
        print("GEN {}".format(gen))
        SetKernelStatus({"data_prefix": "generation_"+str(gen)+"_"})
        ResetKernel()

        # Create num_trials in parallel
        inds = []
        for ind in range(num_ind):
            g = genomes[ind]
            g.fitness = 0
            tris = []
            for t in range(num_trials):
                tris.append(Animat(g))
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
        for step in range(gameheight):
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
            ns = np.zeros((num_ind, num_trials, no))
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
                score = 0

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

        if genomes[sort[0]].fitness > best_solution.fitness:
            best_solution = copy.deepcopy(genomes[sort[0]])

        if genomes[sort[0]].fitness > mean_smax:
            top_solutions.append(copy.deepcopy(genomes[sort[0]]))

        genomes[0].iw = genomes[sort[0]].iw # Best net doesn't change
        genomes[0].hw = genomes[sort[0]].hw # Best net doesn't change
        genomes[0].ow = genomes[sort[0]].ow # Best net doesn't change
        genomes[0].id = genomes[sort[0]].id
        genomes[0].fitness = 0

        print("!!!\n Going through individuals to find top solutions \n!!!!")
        if Rank() == 0:
            for j in range(1, num_ind):

                if genomes[sort[j]].fitness > mean_smax:
                    top_solutions.append(copy.deepcopy(genomes[sort[j]]))

                old_genome = genomes[sort[j]]
                old_iw = old_genome.iw
                old_hw = old_genome.hw
                old_ow = old_genome.ow
                liw = np.shape(old_iw)
                lhw = np.shape(old_hw)
                low = np.shape(old_ow)
                # Mutation based on rank, lower rank, more mutation
                new_iw = old_iw + ((np.random.rand(liw[0],liw[1])-0.5)*(muadj/r*increase**j))
                new_hw = old_hw + ((np.random.rand(lhw[0], lhw[1])-0.5)*(muadj/r*increase**j))
                new_ow = old_hw + ((np.random.rand(low[0], lhw[1])-0.5)*(muadj/r*increase**j))
                genomes[j].iw = new_iw
                genomes[j].hw = new_hw
                genomes[j].ow = new_ow
                genomes[j].id = old_genome.id
                genomes[j].fitness = 0
        else:
            genomes = None

        genomes = comm.bcast(genomes, root=0)
        top_solutions = comm.bcast(top_solutions, root=0)

        print("Generation {} finished. \n \
            Best solution had fitness {}. \n \
            Best fitness (scoreMax) was {}. \n \
            Mean fitness was {}. \n\
            ".format(gen, best_solution.fitness, scoreMax[-1], scoreMean[-1]))


        timestamp = datetime.now()
        timer = timestamp-starttime
        timestamp = timestamp.strftime("%Y-%b-%d-%H:%M:%S:%f")
        print("Time this took: {}".format(timer))

        results = { 'scoreMax' : scoreMax,
                    'scoreMean': scoreMean,
                    'best_solution': best_solution,
                    'top_solutions': top_solutions}


        gen += 1
        print("Current number of top solutions: {}".format(len(top_solutions)))
        # END OF GENERATION
    if Rank() == 0:
        filename = "results/run_gens_np["+str(P)+"g["+str(gen)+"]_scoremax[-1]["+str(scoreMax[-1])+"]_scoremin[-1]["+str(scoreMin[-1])+"]_bf["+str(best_solution.fitness)+"]_time["+str(timestamp)+"]"
        with open(filename, 'wb') as f:
            pickle.dump(results, f, protocol=pickle.HIGHEST_PROTOCOL)

    return genomes, best_solution, mean_smax

def run_epoch(comm, numprocs, num_top, num_ind, num_tests, num_trials, gameheight, gamewidth, genomes, best_solution, mean_smax):

    genomes = genomes
    best_solution = best_solution
    mean_smax = mean_smax

    scoreMax = []
    scoreMean = []

    # EVOSTATS
    r = 12 # arbitrary mutation rate that affects every mutation linearly
    increase = 1.1 # increase that is scaled exponentially with the rank
    muadj = 1 # adjustment for weight scale

    ni = 2
    nh = 4
    no = 2

    ps = 5 # Population Size

    top_solutions = []

    starttime = datetime.now()
    gen = 0
    #for gen in range(num_gen):
    while len(top_solutions) < num_top:
        print("GEN {}".format(gen))
        SetKernelStatus({"data_prefix": "generation_"+str(gen)+"_"})
        ResetKernel()

        # Create num_trials in parallel
        inds = []
        for ind in range(num_ind):
            g = genomes[ind]
            g.fitness = 0
            tris = []
            for t in range(num_trials):
                tris.append(Animat(g))
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
        for step in range(gameheight):
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
            ns = np.zeros((num_ind, num_trials, no))
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
                score = 0

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

        if genomes[sort[0]].fitness > best_solution.fitness:
            best_solution = copy.deepcopy(genomes[sort[0]])

        if genomes[sort[0]].fitness > mean_smax:
            top_solutions.append(copy.deepcopy(genomes[sort[0]]))

        genomes[0].iw = genomes[sort[0]].iw # Best net doesn't change
        genomes[0].hw = genomes[sort[0]].hw # Best net doesn't change
        genomes[0].ow = genomes[sort[0]].ow # Best net doesn't change
        genomes[0].id = genomes[sort[0]].id
        genomes[0].fitness = 0

        print("!!!\n Going through individuals to find top solutions \n!!!!")
        if Rank() == 0:
            for j in range(1, num_ind):

                if genomes[sort[j]].fitness > mean_smax:
                    top_solutions.append(copy.deepcopy(genomes[sort[j]]))

                old_genome = genomes[sort[j]]
                old_iw = old_genome.iw
                old_hw = old_genome.hw
                old_ow = old_genome.ow
                liw = np.shape(old_iw)
                lhw = np.shape(old_hw)
                low = np.shape(old_ow)
                # Mutation based on rank, lower rank, more mutation
                new_iw = old_iw + ((np.random.rand(liw[0],liw[1])-0.5)*(muadj/r*increase**j))
                new_hw = old_hw + ((np.random.rand(lhw[0], lhw[1])-0.5)*(muadj/r*increase**j))
                new_ow = old_hw + ((np.random.rand(low[0], lhw[1])-0.5)*(muadj/r*increase**j))
                genomes[j].iw = new_iw
                genomes[j].hw = new_hw
                genomes[j].ow = new_ow
                genomes[j].id = old_genome.id
                genomes[j].fitness = 0
        else:
            genomes = None

        genomes = comm.bcast(genomes, root=0)
        top_solutions = comm.bcast(top_solutions, root=0)

        print("Generation {} finished. \n \
            Best solution had fitness {}. \n \
            Best fitness (scoreMax) was {}. \n \
            Mean fitness was {}. \n\
            ".format(gen, best_solution.fitness, scoreMax[-1], scoreMean[-1]))


        timestamp = datetime.now()
        timer = timestamp-starttime
        timestamp = timestamp.strftime("%Y-%b-%d-%H:%M:%S:%f")
        print("Time this took: {}".format(timer))

        results = { 'scoreMax' : scoreMax,
                    'scoreMean': scoreMean,
                    'best_solution': best_solution,
                    'top_solutions': top_solutions}

        if Rank() == 0:
            filename = "results/run_epoch_np["+str(P)+"g["+str(gen)+"]_t["+str(num_trials)+"]_i["+str(num_ind)+"]_bf["+str(best_solution.fitness)+"]_time["+str(timestamp)+"]"
            with open(filename, 'wb') as f:
                pickle.dump(results, f, protocol=pickle.HIGHEST_PROTOCOL)

        gen += 1
        print("Current number of top solutions: {}".format(len(top_solutions)))
        # END OF GENERATION


    # END OF GENERATIONS
    # evaluate epoch
    print("RANK {}: WHILE LOOP IS FINISHED".format(Rank()))
    print("Current number of top solutions: {}".format(len(top_solutions)))

    #scores, mean_scores, argsort_ms = test_top_solutions(comm, numprocs, top_solutions, num_tests, num_top, num_trials, gameheight, gamewidth)
    # test top solutions

    no = 2
    scores = np.zeros((num_tests, num_ind))
    # AVERAGING TESTS
    for i in range(num_tests):
        ResetKernel()
        inds = []
        for ind in range(num_ind):
            top_solutions[ind].fitness = 0
            tris = []
            for t in range(num_trials):
                tris.append(Animat(top_solutions[ind]))
            inds.append(tris)

        # TRIALS
        #game = Game(gh=gameheight, gw=gamewidth, n_ind=num_ind, n_trials=num_trials)
        #blockstates, directions, blocksizes, paddlestates = setup_game(comm, gamewidth, num_ind, num_trials)
        # setup game
        # Setting random variables, broadcasting
        if Rank() == 0:
            ## Block
            blockstates = np.random.randint(0, high=gamewidth, size=(num_ind, num_trials))
            #print("blockstates: \n{}".format(blockstates))

            directions = np.random.randint(-1, high=2, size=(num_ind, num_trials))
            #print("directions: \n{}".format(directions))

            blocksizes = np.random.randint(1, high=5, size=(num_ind, num_trials))
            blocksizes = blocksizes - ((blocksizes == 4)+0) - ((blocksizes == 2)+0)

            #print("blocksizes: \n {}".format(blocksizes))

            ## Paddle
            paddlestates = np.random.randint(0, high=gamewidth, size=(num_ind, num_trials))
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

        #blockstates, paddlestates = run_steps(comm, numprocs, gameheight, num_ind, num_trials, no, blockstates, blocksizes, paddlestates, directions, gamewidth, inds)
        # run steps
        # STEPS
        start = 1.0
        runtime = 33.0
        for step in range(gameheight):
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

        #inds = last_step(comm, blocksizes, paddlestates, num_ind, num_trials, gamewidth, inds)
        # last step
        # evaluate gamestates
        b_ends = (blockstates + blocksizes)
        p_left = paddlestates-1
        p_right = paddlestates+1

        # todo: vectorize this?
        for i in range(num_ind):
            for j in range(num_trials):
                crash = False
                score = 0

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

        for j in range(num_ind):
            scores[i][j] = top_solutions[j].fitness

    mean_scores = np.mean(scores, axis=0)
    print("Mean scores:\n {}".format(mean_scores))
    argsort_ms = np.argsort(mean_scores)[::-1]
    print("Sorted mean_scores: \n{}".format(argsort_ms))

    eef = 2 # epoch elitism fraction
    nelit = int(num_top/eef) # number of top solutions to take over (elitism number)
    sort_ms = argsort_ms[0:nelit]
    genomes = []
    for i in range(nelit):
        genomes.append(top_solutions[sort_ms[i]])

    if Rank() == 0:
        for i in range(nelit, num_ind):
            genomes.append(Genome(id=i, ps=ps, nh=nh))
    else:
        nothing = "nothing"

    genomes = comm.bcast(genomes, root=0)

    mean_smax = np.mean(scoreMax)

    return genomes, best_solution, mean_smax


def run_sga_epoch(comm, numprocs):
    ResetKernel()

    gameheight = 16
    gamewidth = 8
    num_trials = 128
    num_ep = 1000
    num_top = 10
    num_ind = 10
    num_tests = 10
    if sys.argv[1] == "load":
        filename = sys.argv[2]
        genomes, best_solution, mean_smax = load_solutions(filename, comm, num_ind)
    else:
        genomes, best_solution, mean_smax = create_genomes(comm, num_ind)

    scoreMean = []
    scoreMax = []

    start_ep = datetime.now()
    for ep in range(num_ep):
        genomes, best_solution, mean_smax = run_epoch(comm, numprocs, num_top, num_ind, num_tests, num_trials, gameheight, gamewidth, genomes, best_solution, mean_smax)
        scores = [g.fitness for g in genomes]
        sort = np.argsort(scores)[::-1]
        scoreMean.append(np.mean(scores))
        scoreMax.append(np.max(scores))
        print("Epoch {} finished. \n \
            Best solution had fitness {}. \n \
            Best fitness (scoreMax) was {}. \n \
            Mean fitness was {}. \n\
            ".format(ep, best_solution.fitness, scoreMax[-1], scoreMean[-1]))

        results = { 'scoreMax' : scoreMax,
                    'scoreMean': scoreMean,
                    'best_solution': best_solution,
                    'top_solutions': genomes}

        timestamp_e = datetime.now()
        timer = timestamp_e-start_ep
        timestamp_e = timestamp_e.strftime("%Y-%b-%d-%H:%M:%S:%f")
        print("Time this took: {}".format(timer))

        if Rank() == 0:
            filename = "results/run_np["+str(P)+"epoch["+str(ep)+"]_bf["+str(best_solution.fitness)+"]_time["+str(timestamp_e)+"]"
            with open(filename, 'wb') as f:
                pickle.dump(results, f, protocol=pickle.HIGHEST_PROTOCOL)
        # END OF EPOCH

if __name__ == '__main__':
    P = 56
    SetKernelStatus({"total_num_virtual_procs": P,'local_num_threads':1})

    num_tests = 20
    num_ind = 10
    num_trials = 128
    gameheight = 36
    gamewidth = 16
    num_gen = 100

    comm = MPI.COMM_WORLD
    numprocs = NumProcesses()



    genomes, best_solution, mean_smax = create_genomes(comm, num_ind)
    mean_smax = 80

    for i in range(100):
        run_generations(comm, numprocs, num_gen, num_ind, num_trials, gameheight, gamewidth, genomes, best_solution, mean_smax)

    '''
    filename = sys.argv[1]
    genomes, best_solution, mean_smax = load_solutions(filename, comm, num_ind)
    print("best solution fitness: {}".format(best_solution.fitness))

    for g in genomes:
        print(g.fitness)

    scores, mean_scores, argsort_ms = test_top_solutions(comm, numprocs, [best_solution], num_tests, num_ind, num_trials, gameheight, gamewidth)

    print("scores: {} \nmean_scores: {} \nargsort_ms: {}".format(scores, mean_scores, argsort_ms))
    '''



