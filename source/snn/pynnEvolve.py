import pyNN.nest as pynn

from pynnAnimat import Animat
from genome import SgaGenome
from pynnGame import Game

from parallel import ParallelEvaluator

import numpy as np
from numpy.random import randint
from nest import SetKernelStatus

import os
import sys
import pickle
import multiprocessing

import matplotlib.pyplot as plt

from datetime import datetime


import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    "-g", "--generations",
    help="The number of generations to be run per epoch.",
    type=int,
    default=10)
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
    default=10)
args = parser.parse_args()

class Troll(object):
    def __init__(self):
        self.weight = randint(1,100)

    def get(self):
        return self.weight

x = 10

t = Troll()

def f(genome, params, num_games):
    params = params
    game = Game()
    genome.fitness = 0
    for i in range(num_games):
        genome.fitness += game.run(genome, params)
    return genome.fitness

if __name__ == '__main__':
    print(1)
    # Creating population
    num_gen = args.generations

    num_individuals = args.populationsize

    # Setting animat size
    num_inp = args.input
    num_hid = args.network
    num_out = args.output

    # Setting max fitness
    num_games = args.trials

    genomes = []
    for i in range(num_individuals):
        genomes.append(SgaGenome(num_inp=num_inp, num_hid=num_hid, num_out=num_out, id=i))
    print(2)

    # Initial Best Solution
    best_solution = genomes[0]

    cellparams = {
        'tau_m' : 20,
        'tau_syn_E' : 5,
        'tau_syn_I' : 5
    }

    # Set up mutation
    r = 12
    increase = 0.9

    local_dir = os.path.dirname(__file__)
    workers = os.cpu_count()
    pe = ParallelEvaluator(workers, f)
    print(3)
    # redirect print
    original = sys.stdout
    log_path = os.path.join(local_dir, 'pynnEvolve.log')
    sys.stdout = open(log_path, 'w')

    scoreMax = []
    scoreMean = []

    # Creating pool of workers
    workers = multiprocessing.cpu_count()
    pe = ParallelEvaluator(workers, f)
    print(4)

    # Starting epoch
    start = datetime.now()
    for i in range(num_gen):
        print(4)

        pe.evaluate_sga(genomes=genomes, params=cellparams, num_games=num_games)
        print(5)

        scores = [g.fitness for g in genomes]
        sort = np.argsort(scores)[::-1]
        scoreMean.append(np.mean(scores))
        scoreMax.append(np.max(scores))

        genomes[0].genes = genomes[sort[0]].genes # Best net doesn't change
        genomes[0].id = genomes[sort[0]].id

        if  genomes[sort[0]].fitness > best_solution.fitness:
            best_solution = genomes[sort[0]]

        for j in range(1, num_individuals):
            old_genome = genomes[sort[j]]
            old_genes = old_genome.genes
            lg = len(old_genes)
            # Mutation based on rank, lower rank, more mutation
            new_genes = old_genes + ((np.random.rand(lg)-0.5)/r*increase**j)
            genomes[j].genes = new_genes
            genomes[j].id = old_genome.id

        print("Generation {} finished. \n \
            Best fitness (genepool[0]) was {}. \n \
            Best fitness (scoreMax) was {}. \n \
            Mean fitness was {}. \n\
            ".format(i, genomes[sort[0]].fitness, scoreMax[-1], scoreMean[-1]))



    print(6)
    print("{} generations with {} animats took {}".format(num_gen,num_individuals,datetime.now()-start))
    print("Plotting mem.pot. and spiketrain of animat with best solution.")
    game = Game()
    game.run(best_solution, params=cellparams, plot=True)

    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y-%b-%d-%H:%M:%S:%f")
    gname = 'results/best-solution_fitness['+str(best_solution.fitness)+']_date['+str(timestamp)+']'
    log_path = os.path.join(local_dir, gname)
    with open(log_path, 'wb') as handle:
        pickle.dump(best_solution, handle, protocol=pickle.HIGHEST_PROTOCOL)

    plt.plot(scoreMean)
    plt.xlabel("Generations")
    plt.ylabel("Mean fitness")
    figname = "results/scoreMean_date["+str(timestamp)+"].png"
    figname = os.path.join(local_dir, figname)
    plt.savefig(log_path)
    plt.show()

    plt.plot(scoreMax)
    plt.xlabel("Generations")
    plt.ylabel("Max fitness")
    figname = 'results/scoreMax_date['+str(timestamp)+'].png'
    log_path = os.path.join(local_dir, figname)
    plt.savefig(log_path)
    plt.show()

    # redirect print
    sys.stdout = original


    print(datetime.now() - start)
