import os
import pickle
import numpy as np
from mpi4py import MPI
from datetime import datetime


from nest import *

from nestGame import Game
from nestAnimat import Animat
from nestGenome import Genome

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    numprocs = NumProcesses()
    num_ind = 10
    num_ep = 10
    num_top = 10
    num_trials = 128

    top_solutions = []

    genomes = []
    if Rank() == 0:
        #if sys.argv[1] == "load":
        for i in range(num_ind):
            genomes.append(Genome(id=i))

        best_solution = genomes[0]
    else:
        genomes = []
        best_solution = None

    genomes = comm.bcast(genomes, root=0)
    best_solution = comm.bcast(best_solution, root=0)

    start_ep = datetime.now()
    for ep in range(num_ep):
        while len(top_solutions) < num_top:
            starttime = datetime.now()
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

            game = Game()

            game.setup_game(comm)
            game.run_steps(comm, numprocs, 2, inds)
            inds = game.last_step(comm, inds)

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









