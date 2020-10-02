#!/usr/bin/env python3

# plot params stagnation
import multiprocessing
import sys
import os
import pickle

from datetime import datetime
#os.environ["PATH"] += os.pathsep +  "/home/daniesis/neuromorphic2/nmenv/lib/python3.5/site-packages/graphviz"
import numpy as np
import math
import re
from matplotlib import pyplot as plt

import neat
from neat.math_util import mean
import visualize
from neat import activations
from game import Game

import screen

time_const = 0.01

def eval_genome(genome, config):
    num_games = 128
    genome.fitness = 0
    net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
    game = Game(8)
    for i in range(num_games):
        ret = game.run(net)
        # print('game return: %d' %ret)
        genome.fitness += ret
        # print('genome id: %d \ngenome fitness: %d'%(genome_id,genome.fitness))

    # the treshold at which the genome will be saved

    return genome.fitness

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


# New activation functions
def OR_gate(x):
    try:
        if any(x) == 1:
            return np.max(x)
        else:
            return 0
    except TypeError as te:
        if x > 0.5:
            return x
        else:
            return 0

def AND_gate(x):
    try:
        if all(x) > 0.5:
            return np.mean(x)
        else:
            return 0
    except TypeError as te:
        if x > 0.5:
            return 1
        else:
            return 0

def XOR_gate(x):
    try:
        if len(x[x > 0]) == 1:
            return np.max(x)
        else:
            return 0
    except TypeError as te:
        if x > 0.5:
            return x
        else:
            return 0

def or_aggregation(x):
    if any(x) == 1:
        return 1
    else:
        return 0

def and_aggregation(x):
    if all(x) == 1:
        return 1
    else:
        return 0

def xor_aggregation(x):
    if x.count(1) == 1:
        return 1
    else:
        return 0

def copy_aggregation(x):
    if mean(x) > 0:
        return 1
    elif mean(x) < 0:
        return -1
    else:
        return 0

def not_aggregation(x):
    if mean(x) > 0:
        return -1
    elif mean(x) < 0:
        return 1
    else:
        return 0


def compute_all2all_connections(genome, config, direct):
    """
    Compute connections for a fully-connected feed-forward genome--each
    input connected to all hidden nodes
    (and output nodes if ``direct`` is set or there are no hidden nodes),
    each hidden node connected to all output nodes.
    Hidden nodes are connected to all hidden nodes.
    """
    hidden = [i for i in genome.nodes if i not in config.output_keys]
    output = [i for i in genome.nodes if i in config.output_keys]
    connections = []
    if hidden:
        for input_id in config.input_keys:
            for h in hidden:
                connections.append((input_id, h))
        for h in hidden:
            for h_id in hidden:
                connections.append((h, h_id))
            for output_id in output:
                connections.append((h, output_id))
    if direct or (not hidden):
        for input_id in config.input_keys:
            for output_id in output:
                connections.append((input_id, output_id))

    return connections

def connect_full_direct(genome, config):
    """ Create a fully-connected genome, including direct input-output connections. """
    for input_id, output_id in genome.compute_full_connections(config, True):
        connection = genome.create_connection(config, input_id, output_id)
        genome.connections[connection.key] = connection

def run(config_file):
    # Load configuration
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
            neat.DefaultSpeciesSet, neat.DefaultStagnation,
            config_file)


    config.genome_config.add_activation('OR_gate', OR_gate)
    config.genome_config.add_activation('AND_gate', AND_gate)
    config.genome_config.add_activation('XOR_gate', XOR_gate)
    config.genome_config.add_aggregation('or_aggregation', or_aggregation)
    config.genome_config.add_aggregation('and_aggregation', and_aggregation)
    config.genome_config.add_aggregation('xor_aggregation', xor_aggregation)
    config.genome_config.add_aggregation('copy_aggregation', xor_aggregation)
    config.genome_config.add_aggregation('not_aggregation', xor_aggregation)

    best = []
    max_fit_epochs = []
    mean_fit_epochs = []

    num_gen = 1000
    stagnation_rate = [0.01*i+0.01*i*i for i in range(1,10)]
    stagnation = []
    for sr in stagnation_rate:
        #print(f'init pop')
        # Create the population, which is the top-level object for a NEAT run.
        p = neat.Population(config)

        stagnation.append(sr*num_gen)
        print("STAGNATION: {}".format(stagnation[-1]))
        p.config.stagnation_config.max_stagnation = stagnation[-1]

        # creating a all2all connection
        for genome_id, genome in list(p.population.items()):
            connect_full_direct(genome, config.genome_config)

        # for plotting
        # Restore from checkpoint
        #print("restore pop")
        #p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-33419")

        # Getting the local directory path
        local_dir = os.path.dirname(__file__)

        # Add a stdout reporter to show progress in the terminal
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        filename = os.path.join(local_dir, 'neat-checkpoint-')
        checkpointer = neat.Checkpointer(generation_interval=60000, time_interval_seconds=100000, filename_prefix=filename)
        p.add_reporter(checkpointer)

        score_max = []
        score_mean = []
        pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
        winner = p.run(pe.evaluate, n=num_gen, score_max=score_max, score_mean=score_mean)

        timestamp = datetime.now().strftime("%Y-%b-%d-%H:%M:%S:%f")
        filename = "results/100gen_stagnation["+str(sr)+"]_scoremax[-1]=["+str(score_max[-1])+"]_scoremean[-1]=["+str(score_mean[-1])+"]_time=["+str(timestamp)+"]"
        log = { 'scoreMax': score_max,
                'scoreMean': score_mean,
                'stagnation': sr }
        with open(filename, 'wb') as f:
            pickle.dump(log, f, protocol=pickle.HIGHEST_PROTOCOL)

        max_fit_gens = stats.get_fitness_stat(max)
        max_fit_epochs.append(max(max_fit_gens))

        mean_fit_epochs.append(mean(stats.get_fitness_stat(mean)))

        best.append( stats.best_genome() )

    # Display the winning genome
    #print('\nBest genomes:\n%f', best)

    local_dir = os.path.dirname(__file__)

    filename = os.path.join(local_dir, "max-fitness-stagnation.svg")
    plt.plot(stagnation, max_fit_epochs, label='Max fitness')
    plt.plot(stagnation, mean_fit_epochs, label='Mean fitness')
    plt.xlabel('No. of generations without improvement that a genome is kept alive.')
    plt.ylabel('Fitness: No. of successfull trials out of a total of 128 games')
    plt.legend()
    plt.savefig(filename)
    #plt.show()

if __name__ == '__main__':
    # Detemine path to configuration file. This path manipulation is

    # here so that the script will run sucessfully regardless of the
    # current working directory.

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-ff')

    # redirect print
    original = sys.stdout
    log_path = os.path.join(local_dir, 'recurrentnn.log')
    sys.stdout = open(log_path, 'w')

    # run program
    run(config_path)


    # redirect print
    sys.stdout = original
