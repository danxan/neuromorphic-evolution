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

    num_gen = 10
    trials = 128
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
            genomes.append(Genome(ps, nh, id=i))
        else:
            genomes.append(None)

    genomes = comm.bcast(genomes, root=0)

    best_solution = genomes[0]


    starttime = datetime.now()
    for gen in range(num_gen):
        SetKernelStatus({"data_prefix": "generation_"+str(gen)+"_"})

        # TRIAL
        for trial in range(trials):
            start = 1.0
            runtime = 33.0

            ResetKernel()

            sgs = [None]*num_ind
            sds = [None]*num_ind
            animats = []

            for i in range(0,num_ind):
                sgs[i] = []
                for j in range(ni):
                    sgs[i].append(Create("spike_generator"))

                sds[i] = []
                for j in range(no):
                    sds[i].append(Create("spike_detector"))#, params={"to_file": True}))

                animats.append(Animat(sgs[i], sds[i], genomes[i]))

            # Setting random variables, broadcasting
            if Rank() == 0:
                ## Block
                blockstates = np.random.randint(0, high=15, size=num_ind)

                direction = np.random.randint(-1,1)

                p = np.random.randint(0,1)
                if p == 1:
                    blocksize = 1
                else:
                    blocksize = 3

                ## Paddle
                paddlestates = np.random.randint(0, high=15, size=num_ind)

            else:
                blockstates = None
                direction = None
                blocksize = None
                paddlestates = None

            blockstates = comm.bcast(blockstates, root=0)
            direction = comm.bcast(direction, root=0)
            blocksize = comm.bcast(blocksize, root=0)
            paddlestates = comm.bcast(paddlestates, root=0)


            for i in blockstates:
                i = (i+direction)%gamewidth

            # STEP
            for step in range(steps):
                spikes = [[0]*ni]*num_ind

                # Evaluate gamestates
                for i in range(num_ind):
                    bs = blockstates[i] # Start of block
                    be = (bs + blocksize)%gamewidth # end of block
                    pl = (paddlestates[i]-1) # left paddle sensor
                    pr = (paddlestates[i]+1) # right paddle sensor


                    s = [0,0] # TODO: This code only works for two input neurons

                    for u in range(bs, be, 1):
                        if (u%gamewidth) == pl%gamewidth:
                            s[0] = 1
                        if (u%gamewidth) == pr%gamewidth:
                            s[1] = 1

                    spikes[i] = s

                    for j in range(ni):
                        if spikes[i][j] == 1:
                            SetStatus(sgs[i][j], {'spike_times': [start]})
                        else:
                            SetStatus(sgs[i][j], {'spike_times': []})


                Simulate(runtime)
                start = start+runtime

                # Collect number of spikes for each spike detector
                ns = np.zeros((num_ind, no))
                #print("rank {}: before loop ns={}".format(Rank(),ns))
                for i in range(num_ind):
                    spikes = [0]*no
                    s1 = len(GetStatus(sds[i][0], 'events')[0]['times'])
                    s2 = len(GetStatus(sds[i][1], 'events')[0]['times'])

                    spikes[0] = float(s1)
                    spikes[1] = float(s2)

                    # Clear spike detector
                    SetStatus(sds[i][0], {'n_events': 0})
                    SetStatus(sds[i][1], {'n_events': 0})
                    ns[i] = spikes

                if Rank() == 0:
                    for p in range(1,numprocs):
                        req = comm.irecv(source=p)
                        ns += req.wait()
                else:
                    comm.send(ns, dest=0)

                ns = comm.bcast(ns, root=0)

                #print("{} has ns value {}".format(Rank(), ns))

                # MAKE DECISION
                for i, s in enumerate(ns):
                    decision = 0
                    if s[0] < s[1]:
                        decision = 1
                    elif s[0] > s[1]:
                        decision = -1

                    paddlestates[i] = (paddlestates[i]+decision)%gamewidth
                # END OF STEP

            # END OF STEPS
            for i in range(num_ind):
                bs = blockstates[i] # Start of block
                be = bs + blocksize # end of block
                crash = False
                pl = paddlestates[i]-1 # left paddle unit
                pr = paddlestates[i]+1 # right paddle unit

                score = -1
                for j in range(bs, be, 1):
                    for k in range(pl, pr+1, 1):
                        crash = (j%gamewidth) == (k%gamewidth)
                        if crash: break
                    if crash: break

                if crash:
                    if blocksize == 1:
                        score = 1
                else:
                    if blocksize == 3:
                        score = 1

                genomes[i].fitness += score
                # END OF TRIAL

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
        genomes[0].fitness = -128


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
                genomes[j].fitness = -128
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
            filename = "results/run_np["+str(P)+"g["+str(num_gen)+"]_t["+str(trials)+"]_i["+str(num_ind)+"]_bf["+str(best_solution.fitness)+"]_time["+str(timestamp)+"]"
            with open(filename, 'wb') as f:
                pickle.dump(results, f, protocol=pickle.HIGHEST_PROTOCOL)

        # END OF GENERATION

    # END OF GENERATIONS




        # np.logical_or(np.any((bl+p)%10<1), np.any(np.abs(bl-p)<2))


    #Cleanup()

