#!/usr/bin/env python3
import multiprocessing
import pickle
import sys
import os
import time
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
    net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
    game = Game(8)
    for i in range(num_games):
        ret = game.run(net)
        # print('game return: %d' %ret)
        genome.fitness += ret
        # print('genome id: %d \ngenome fitness: %d'%(genome_id,genome.fitness))

    # the treshold at which the genome will be saved
    if genome.fitness > (num_games*2*0.9 - 128):

        # Getting the local directory path
        local_dir = os.path.dirname(__file__)

        timestamp = datetime.now()
        timestamp = timestamp.strftime("%Y-%b-%d-%H:%M:%S:%f")

        genomedir = os.path.join(local_dir, "good-genome/gg["+timestamp+']/')
        os.makedirs(genomedir)

        genomepath = os.path.join(local_dir, "good-genome/gg["+timestamp+']/genome')
        # Save the good genome.
        with open(genomepath, 'wb') as f:
            pickle.dump(genome, f)

        configpath = os.path.join(local_dir, "good-genome/gg["+timestamp+']/config')
        # Save the good genome.
        config.save(configpath)

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
    # Restore from checkpoint
    #print("restore pop")
    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-23969")

    # Getting the local directory path
    local_dir = os.path.dirname(__file__)

    # Add a stdout reporter to show progress in the terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    filename = os.path.join(local_dir, 'neat-checkpoint-')
    p.add_reporter(neat.Checkpointer(generation_interval=5000, time_interval_seconds=14400, filename_prefix=filename))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = p.run(pe.evaluate)

    # Save the winner.
    filename = os.path.join(local_dir, 'winner-feedforward')
    with open('winner-feedforward', 'wb') as f:
        pickle.dump(winner, f)

    # Display the winning genome
    print('\nBest genome:\n%f', winner)

    filename = os.path.join(local_dir, "avg_fitness-recurrent.svg")
    visualize.plot_stats(stats, ylog=False, view=True, filename=filename)

    print("writing species")
    filename = os.path.join(local_dir, "species-recurrent.svg")
    visualize.plot_species(stats, view=True, filename=filename)

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
