import sys
import pickle
import numpy as np
import multiprocessing as mp
from datetime import datetime
import copy

class Genome(object):
    def __init__(self, gid, low=-0.5, high=0.5):
        self.id = gid

        self.fitness = 0

        self.ni = 2
        self.nh = 5
        self.no = 2

        # The threshold is based on how many nodes that could possibly be connected to it, and assuming that weights are around 1.
        self.thresh_h = np.random.randint(self.ni-2, high=self.nh-1, size=(self.nh))
        self.thresh_o = np.random.randint(self.nh-3, high=self.nh-1, size=(self.no))

        self.bias_h = np.random.uniform(low, high=high, size=(self.nh))
        self.bias_o = np.random.uniform(low, high=high, size=(self.no))


        self.iw = np.random.uniform(low, high=high, size=(self.ni,self.nh))
        self.hw = np.random.uniform(low, high=high, size=(self.nh,self.nh))
        self.ow = np.random.uniform(low, high=high, size=(self.nh,self.no))

    def mutate(self, mutation_power):
        self.thresh_h = self.thresh_h + (np.random.rand(self.nh) - 0.5)*mutation_power
        self.thresh_o = self.thresh_o + (np.random.rand(self.no) - 0.5)*mutation_power

        self.bias_h = self.bias_h + (np.random.rand(self.nh) - 0.5)*mutation_power
        self.bias_o = self.bias_o + (np.random.rand(self.no) - 0.5)*mutation_power

        self.iw = self.iw + (np.random.rand(self.no,self.nh) - 0.5)*mutation_power
        self.hw = self.hw + (np.random.rand(self.nh,self.nh) - 0.5)*mutation_power
        self.ow = self.ow + (np.random.rand(self.nh,self.no) - 0.5)*mutation_power



class Animat(object):
    def __init__(self, genome):
        self.genome = genome
        self.thresh_h = genome.thresh_h
        self.thresh_o = genome.thresh_o
        self.bias_h = genome.bias_h
        self.bias_o = genome.bias_o
        self.iw = genome.iw
        self.hw = genome.hw
        self.ow = genome.ow

        self.il = np.zeros(genome.ni) # input layer
        self.hl = np.zeros(genome.nh) # hidden layer
        self.ol = np.zeros(genome.no) # output layer

    def run(self, stimuli):
        """ stimuli is a 2x1 array of integers
        step activation function
        """
        #stimuli = np.reshape(stimuli, (1,2), order='C')
        self.il = np.where(stimuli > 0, 1, 0)
        #self.hl_r = np.where(np.sum(self.hl.dot(self.hw), axis=0) > self.thresh_h, 1, 0) # hidden layer recurrent
        #+np.sum(self.hl.dot(self.hw), axis=0)
        # TODO: FIGURE OUT IF THESE DOT PRODUCTS DO AS I WANT THEM TO
        self.hl = np.where(self.il.dot(self.iw) + self.hl.dot(self.hw) > self.thresh_h, 1, 0)
        self.ol = self.hl.dot(self.ow) # no threshold on output neuron, compare size instead, this is a replacement for sigmoid, in a way...



        self.decision = 0
        if self.ol[0] > self.ol[1]:
            self.decision = -1
        elif self.ol[0] < self.ol[1]:
            self.decision = 1

        return self.decision

class Game(object):
    def __init__(self, gameheight, gamewidth, num_ind, num_trials, nets):
        self.gameheight, self.gamewidth, self.num_ind, self.num_trials, self.nets = gameheight, gamewidth, num_ind, num_trials, nets

        self.blockstates = np.random.randint(0, high=self.gamewidth, size=(self.num_ind, self.num_trials))
        #print("blockstates: \n{}".format(blockstates))

        self.directions = np.random.randint(-1, high=2, size=(self.num_ind, self.num_trials))
        #print("directions: \n{}".format(directions))

        self.blocksizes = np.random.randint(1, high=5, size=(num_ind, num_trials))
        self.blocksizes = self.blocksizes - ((self.blocksizes == 4)+0) - ((self.blocksizes == 2)+0)

        #print("blocksizes: \n {}".format(blocksizes))

        ## Paddle
        self.paddlestates = np.random.randint(0, high=self.gamewidth, size=(self.num_ind, self.num_trials))
        #print("paddlestates: \n{}".format(paddlestates))

    def steps(self):
        self.decisions = np.zeros((self.num_ind, self.num_trials))

        for step in range(self.gameheight):
            self.blockstates = (self.blockstates + self.directions)%self.gamewidth

            self.b_e = self.blockstates + self.blocksizes
            self.p_l = self.paddlestates-1
            self.p_r = self.paddlestates+1

            self.stimuli = np.zeros((self.num_ind, self.num_trials, 2))

            for i in range(self.num_ind):
                for j in range(self.num_trials):
                    for b in range(self.blockstates[i][j], self.b_e[i][j], 1):

                        if (b%self.gamewidth) == (self.p_l[i][j]%self.gamewidth):
                            self.stimuli[i,j,0] = 1

                        if (b%self.gamewidth) == (self.p_r[i][j]%self.gamewidth):
                            self.stimuli[i,j,1] = 1

                    self.decisions[i][j] = self.nets[i][j].run(self.stimuli[i,j])

            self.paddlestates = (self.paddlestates + self.decisions)%self.gamewidth

    def last_step(self):
        self.b_e = (self.blockstates + self.blocksizes).astype(int)
        self.p_l = (self.paddlestates-1).astype(int)
        self.p_r = (self.paddlestates+1).astype(int)

        for i in range(self.num_ind):
            for j in range(self.num_trials):
                score = 0
                crash = False
                for b in range(self.blockstates[i][j], self.b_e[i][j], 1):
                    for p in range(self.p_l[i][j], self.p_r[i][j]+1, 1):
                        crash = (b%self.gamewidth) == (p%self.gamewidth)
                        if crash:
                            break
                    if crash:
                        break

                if crash:
                    if self.blocksizes[i][j] == 1:
                        score = 1
                else:
                    if self.blocksizes[i][j] == 3:
                        score = 1

                self.nets[i][j].genome.fitness += score

        return self.nets


class Sga(object):
    def __init__(self, num_ind, num_trials, gameheight, gamewidth):
        self.num_ind, self.num_trials, self.gameheight, self.gamewidth = num_ind, num_trials, gameheight, gamewidth

        self.gencnt = 0
        self.epcnt = 0

        self.score_max_gen = []
        self.score_mean_gen = []

        self.score_max_ep = []
        self.score_mean_ep = []

        self.top_elitism = 4
        self.top_solutions = []
        self.genomes = []
        self.best_solution = None

        # mutation
        m_scalar = 12
        m_scalar_h = 212
        m_exp_incr = 0.9

        self.m_power = [(1/(m_scalar*m_exp_incr**i)) for i in range(1,self.num_ind)]
        #self.m_power_h = [(1/m_scalar*m_exp_incr**i) for i in range(1,self.num_ind)]

        #if sys.argv[1] == "load":
        #    filename = sys.argv[2]
        #    self.load_solutions(filename)
        #else:
        self.create_solutions(self.num_ind)

    def create_solutions(self, num_ind):
        print("create solutions")
        for i in range(num_ind):
            self.genomes.append(Genome(gid=i))
        self.best_solution = self.genomes[0]
        self.mean_smax = 0

        return self.genomes

    def create_networks(self, genomes, num_ind):
        print("create networks")
        self.nets = []
        for i in range(num_ind):
            self.nets.append([])
            for trial in range(self.num_trials):
                self.nets[i].append(Animat(genomes[i]))

        return self.nets

    def run_generation(self, mean_smax):

        starttime = datetime.now()
        print("run generation {}".format(self.gencnt))

        for i in range(self.num_ind):
            self.genomes[i].fitness = 0

        self.nets = self.create_networks(self.genomes, self.num_ind)
        game = Game(self.gameheight, self.gamewidth, self.num_ind, self.num_trials, self.nets)
        game.steps()
        self.nets = game.last_step()

        for g in self.genomes:
            if g.fitness > self.best_solution.fitness:
                self.best_solution = copy.deepcopy(g)

            if g.fitness > mean_smax:
                self.top_solutions.append(copy.deepcopy(g))

        scores = [g.fitness for g in self.genomes]
        argsort_ms = np.argsort(scores)[::-1]

        self.score_max_gen.append(scores[argsort_ms[0]])
        self.score_mean_gen.append(np.mean(scores))

        for i in range(self.num_ind-1): # best net doesn't change
            self.genomes[argsort_ms[i+1]].mutate(self.m_power[i])

        print("Generation {} finished. \n \
            Best solution had fitness {}. \n \
            Best fitness (scoreMax) was {}. \n \
            Mean fitness was {}. \n\
            ".format(self.gencnt, self.best_solution.fitness, self.score_max_gen[-1], self.score_mean_gen[-1]))

        timestamp = datetime.now()
        timer = timestamp-starttime
        timestamp = timestamp.strftime("%Y-%b-%d-%H:%M:%S:%f")
        filename = "results/1000first_rnn_t["+str(timestamp)+"]"
        with open(filename, 'wb') as f:
            pickle.dump(scores, f, protocol=pickle.HIGHEST_PROTOCOL)

        print("Time this took: {}".format(timer))


        self.gencnt += 1
        print("Current number of top solutions: {} | mean_smax is {}".format(len(self.top_solutions), mean_smax))


        return self.genomes, self.best_solution, self.top_solutions


    def test_top_solutions(self, top_solutions):
        print("test top solutions")

        scores = np.zeros(self.num_top)
        for test in range(self.num_tests):
            for i in range(self.num_top):
                self.top_solutions[i].fitness = 0
            self.nets = self.create_networks(self.top_solutions, self.num_top)
            game = Game(self.gameheight, self.gamewidth, self.num_top, self.num_trials, self.nets)
            game.steps()
            self.nets = game.last_step()

            for i in range(self.num_top):
                scores[i] += self.top_solutions[i].fitness

        mean_scores = scores/self.num_tests
        mean_smax = np.max(mean_scores)

        return scores, mean_scores, mean_smax


    def run_epoch(self, mean_smax):
        start_ep = datetime.now()
        print("run epoch {}".format(self.epcnt))
        self.top_solutions = []

        self.gencnt = 0
        while len(self.top_solutions) < self.num_top:
            self.genomes, self.best_solution, self.top_solutions = self.run_generation(mean_smax)

        scores, self.mean_scores, self.mean_smax = self.test_top_solutions(self.top_solutions)

        argsort_ms = np.argsort(mean_scores)[::-1]
        self.elites = []
        while len(self.elites) < self.top_elitism:
            for i in range(self.num_top):
                self.elites.append(copy.deepcopy(self.top_solutions[argsort_ms[i%self.top_elitism]]))

        self.genomes = self.create_solutions(self.num_ind-self.top_elitism)
        self.genomes.extend(self.elites)



        self.score_max_ep.append(np.max(mean_scores))
        self.score_mean_ep.append(np.mean(mean_scores))

        print("TOP SOLUTIONS:\n{}".format(self.top_solutions))

        print("Epoch {} finished. \n \
            Best solution had fitness {}. \n \
            Max avg fitness (of top solution) was {}. \n \
            Mean fitness was {}. \n\
            ".format(self.epcnt, self.best_solution.fitness, self.score_max_ep[-1], self.score_mean_ep[-1]))


        timestamp_e = datetime.now()
        timer = timestamp_e-start_ep
        timestamp_e = timestamp_e.strftime("%Y-%b-%d-%H:%M:%S:%f")
        print("Time this took: {}".format(timer))

        return self.genomes, self.best_solution, self.mean_smax


    def run_sga_epochs(self, num_top, num_tests):

        self.num_top = num_top
        self.num_tests = num_tests
        self.top_solutions = []

        print("run sga epochs")
        for epoch in range(self.num_epochs):
            self.genomes, self.best_solution, self.mean_smax = self.run_epoch(self.mean_smax)
            filename = "results/ann_sga_epoch["+str(self.epcnt)+"]_bf["+str(self.best_solution.fitness)+"]_scoremax_gen[-1]["+str(self.score_max_gen[-1])+"]_scoremax_ep[-1]["+str(self.score_max_ep[-1])+"]"
            with open(filename, 'wb') as f:
                pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)


    def run_sga_gen(self, num_gen, mean_smax, num_tests):
        self.num_tests = num_tests

        self.top_solutions = []

        self.num_gen = num_gen
        for gen in range(num_gen):
            self.run_generation(mean_smax)

            if gen%100 == 0:
                ts = datetime.now()
                filename = "results/ann_sga_gen["+str(self.gencnt)+"of"+str(self.num_gen)+"]_bf["+str(self.best_solution.fitness)+"]_scoremax_gen[-1]["+str(self.score_max_gen[-1])+"]_t["+str(ts)+"]"
                with open(filename, 'wb') as f:
                    pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

        self.num_top = len(self.top_solutions)
        filename = "results/ann_sga_gen["+str(self.gencnt)+"of"+str(self.num_gen)+"]_bf["+str(self.best_solution.fitness)+"]_scoremax_gen[-1]["+str(self.score_max_gen[-1])+"]"
        with open(filename, 'wb') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    sga = Sga(num_ind=1000, num_trials=128, gameheight=32, gamewidth=16)
    sga.run_sga_gen(1, 100, 10)





