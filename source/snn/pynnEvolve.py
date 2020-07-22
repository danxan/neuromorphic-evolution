import multiprocessing
import sys
import os

import math
import re
from matplotlib import pyplot as plt
import time
from datetime import datetime
import pickle
import numpy as np

import pyNN.nest as pynn

from pynnGame import Game
from pynnAnimat import Animat

import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    "-g", "--generations", 
    help="The number of generations to be run per epoch.", 
    type=int,
    default=100)
parser.add_argument(
    "-p", "--populationsize", 
    help="The number of individuals that each population \
        consist of per generation.", 
    type=int,
    default=10)
parser.add_argument(
    "-i", "--input", 
    help="The number of input nodes per animat. \
        Currently this number has to be two.", 
    type=int,
    default=2)
parser.add_argument(
    "-n", "--network", 
    help="The number of hidden nodes in each animats network.\
        Currently this number has to be 4.", 
    type=int,
    default=4)
parser.add_argument(
    "-o", "--output", 
    help="The number of output nodes per animat. \
        Currently this number has to be two.", 
        type=int,
        default=2)
parser.add_argument(
    "-t", "--trials", 
    help="The number of games to be run per individual per generation. \
        This determines the maximum fitness.", 
    type=int,
    default=128)
args = parser.parse_args()

class Genome(object):
    def __init__(self, num_inp=2, num_hid=4, num_out=2, id=0):
        self.fitness = 0
        self.genes = np.random.randint(0,15, 2*(num_inp*num_hid+num_hid*num_hid+num_hid*num_out))
        self.genes[0] = 15
        self.genes[1] = 15
        self.id = id

class Genepool(object):
    def __init__(self, num_individuals=10, num_inp=2, num_hid=4, num_out=2):
        self.genomes = []
        for i in range(num_individuals):
            self.genomes.append(Genome(num_inp=num_inp, num_hid=num_hid, num_out=num_out, id=i))

def fitness_function(genepool, animats, num_games=128):
    for i in range(len(genepool.genomes)):
        animats[i].setWeights(genepool.genomes[i].genes)
        genepool.genomes[i].fitness = 0

        for j in range(num_games):
            # reset simulator
            genepool.genomes[i].fitness += game.run(animats[i])

    return genepool

if __name__ == '__main__':

    # Creating population
    num_gen = args.generations

    num_individuals = args.populationsize

    # Setting animat size
    num_inp = args.input
    num_hid = args.network
    num_out = args.output

    # Setting max fitness
    num_games = args.trials

    game = Game()

    genepool = Genepool(num_individuals=num_individuals, num_inp=num_inp, num_hid=num_hid, num_out=num_out)

    # Initial Best Solution
    best_solution = genepool.genomes[0]


    # Initializing SNNs once, which will be adjusted based on their genomes
    cellparams = {
        'tau_m' : 0.1,
        'tau_syn_E' : 1,
        'tau_syn_I' : 2
    }

    animats = []
    for i in range(num_individuals):
        animats.append(Animat(pop_size=5, input_n=2, hidden_n=4, output_n=2))
        animats[i].inp.set_params(cellparams)
        animats[i].hid.set_params(cellparams)
        animats[i].out.set_params(cellparams)
        a = animats[i].out

    print(animats[0].hid.populations[0].get('tau_m'))
    # Set up mutation
    r = 12
    increase = 0.9

    local_dir = os.path.dirname(__file__)
    # redirect print
    original = sys.stdout
    log_path = os.path.join(local_dir, 'pynnEvolve.log')
    sys.stdout = open(log_path, 'w')

    scoreMax = []
    scoreMean = []

    # Starting epoch
    start = time.time()
    for i in range(num_gen):
        genepool = fitness_function(genepool=genepool, animats=animats, num_games=num_games)

        scores = [g.fitness for g in genepool.genomes]
        sort = np.argsort(scores)[::-1]
        scoreMean.append(np.mean(scores))
        scoreMax.append(np.max(scores))

        genepool.genomes[0].genes = genepool.genomes[sort[0]].genes # Best net doesn't change
        genepool.genomes[0].id = genepool.genomes[sort[0]].id

        if genepool.genomes[0].fitness > best_solution.fitness:
            best_solution = genepool.genomes[0]

        for j in range(1, num_individuals):
            old_genome = genepool.genomes[sort[j]]
            old_genes = old_genome.genes
            lg = len(old_genes)
            # Mutation based on rank, lower rank, more mutation
            new_genes = old_genes + ((np.random.rand(lg)-0.5)/r*increase**j)
            genepool.genomes[j].genes = new_genes
            genepool.genomes[j].id = old_genome.id

        print("Generation {} finished. \n \
            Best fitness (genepool[0]) was {}. \n \
            Best fitness (scoreMax) was {}. \n \
            Mean fitness was {}. \n\
            ".format(i, genepool.genomes[0].fitness, scoreMax[-1], scoreMean[-1]))



    print("{} generations with {} animats took {}".format(num_gen,num_individuals,time.time()-start))
    print("Plotting mem.pot. and spiketrain of animat with best solution.")
    animats[0].setWeights(best_solution.genes)
    game.run(animats[0])
    animats[0].plot()

    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y-%b-%d-%H:%M:%S:%f")
    gname = 'best-solution_fitness['+str(best_solution.fitness)+']_date['+str(timestamp)+']'
    log_path = os.path.join(local_dir, gname)
    with open(log_path, 'wb') as handle:
        pickle.dump(best_solution, handle, protocol=pickle.HIGHEST_PROTOCOL)

    plt.plot(scoreMean)
    log_path = os.path.join(local_dir, 'scoreMean.png')
    plt.savefig(log_path)
    plt.plot(scoreMax)
    log_path = os.path.join(local_dir, 'scoreMax.png')
    plt.savefig(log_path)

    # redirect print
    sys.stdout = original

