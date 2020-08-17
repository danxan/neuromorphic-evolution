from __future__ import print_function

import multiprocessing
import os
import pickle

from pynnGame import Game

import neat
import visualize

num_games = 5


# Use the pnifonn network phenotype 
def eval_genome(genome, config):

    game = Game()
    genome.fitness = 0
    for runs in range(num_games):
        genome.fitness += game.run(genome, config=config)

    # The genome's fitness is its worst performance across all runs.
    return genome.fitness


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-pnifconn')
config = neat.Config(neat.pnifconn.pnifcoGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

pop = neat.Population(config)
stats = neat.StatisticsReporter()
pop.add_reporter(stats)
pop.add_reporter(neat.StdOutReporter(True))

#pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
winner = pop.run(eval_genomes)