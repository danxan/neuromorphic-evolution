#!/usr/bin/env python3

# Discrete B fixed 60k

import multiprocessing
import sys
import os
import pickle

from datetime import datetime
#os.environ["PATH"] += os.pathsep +  "/home/daniesis/neuromorphic2/nmenv/lib/python3.5/site-packages/graphviz"
import numpy as np
import re

import neat
import visualize
from neat import activations
from game import Game

import screen

time_const = 0.01

def eval_genome(genome, config):
    num_games = 128
    genome.fitness = 0
    net = neat.ctrnn.CTRNN.create(genome, config, time_const)
    game = Game(8, time_const)
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

    #print(f'init pop')
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    for genome_id, genome in list(p.population.items()):
        connect_full_direct(genome, config.genome_config)

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
    p.add_reporter(neat.Checkpointer(generation_interval=60000, time_interval_seconds=43200, filename_prefix=filename))

    score_max = []
    score_mean = []
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = p.run(pe.evaluate, n=1000, score_max=score_max, score_mean=score_mean )

    timestamp = datetime.now()
    filename = "neat_ctrnn_results/scoremax[-1]=["+str(score_max[-1])+"]_scoremean[-1]=["+str(score_mean[-1])+"]_time=["+str(timestamp)+"]"
    log = { 'scoreMax': score_max,
            'scoreMean': score_mean }
    with open(filename, 'wb') as f:
        pickle.dump(log, f, protocol=pickle.HIGHEST_PROTOCOL)

    # Display the winning genome
    print('\nBest genome:\n%f', winner)

    local_dir = os.path.dirname(__file__)

    filename = os.path.join(local_dir, "avg_fitness-ctrnn.svg")
    visualize.plot_stats(stats, ylog=False, view=True, filename=filename)

    filename = os.path.join(local_dir, "species-ctrnn.svg")
    visualize.plot_species(stats, view=True, filename=filename)

if __name__ == '__main__':
    # Detemine path to configuration file. This path manipulation is

    # here so that the script will run sucessfully regardless of the
    # current working directory.

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-ctrnn')

    # redirect print
    original = sys.stdout
    log_path = os.path.join(local_dir, 'ctrnn.log')
    sys.stdout = open(log_path, 'w')

    # run program
    run(config_path)


    # redirect print
    sys.stdout = original
