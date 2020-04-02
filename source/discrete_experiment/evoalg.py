import sys
import os
import numpy as np
import re

import neat
import visualize
from neat import activations
from game import Game

time_const = 0.01

def eval_genomes(genomes, config):
    num_games = 50
    for genime_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        game = Game(8)
        for i in range(num_games):
            genome.fitness += game.run(net)

# Aggregation functions o
#TODO: Check what x can be...
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

#TODO: Tror ikke at denne fungerer... Checkout out aggregation..
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

    #print(f'init pop')
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    # Restore from checkpoint
    #print(f"restore pop")
    #p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-59")

    # Add a stdout reporter to show progress in the terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    num_gen = 500
    winner = p.run(eval_genomes, num_gen)


    # Display the winning genome
    print(f'\nBest genome:\n{winner}')

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    game = Game(8)
    winner_net = neat.nn.recurrent.RecurrentNetwork.create(winner, config)
    print(f'WINNER FITNESS {winner.fitness}')
    winner.fitness = 0
    i = 0
    num_games = 50
    while i < num_games:
        ret = game.run(winner_net)
        print(f'Game returned {ret}')
        winner.fitness += ret
        i+=1
    print(f'\nOver {num_games} games, a winner scored {winner.fitness}.\n')


    print(f'input nodes {winner_net.input_nodes}')
    print(f'output nodes {winner_net.output_nodes}')
    #Using regex to find the names ofv
    p = re.compile('(AND|OR|XOR)')
    node_names = {-1:'IA', -2:'IB', 0:'OA', 1:'OB'}
    '''
    for node, activation, aggregation, bias, response, links in winner_net.node_evals:
        print(f'NODE NUMBER IS {node}')
        if node not in node_names.keys():
            node_names[node] = p.search(str(activation)).group(0)
        else:
            node_names[node] = str(node_names[node]) + '\n' + str(p.search(str(activation)).group(0))
    '''


    visualize.draw_net(config, winner, True, node_names=node_names, show_disabled=False, prune_unused=True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4')
    p.run(eval_genomes, 10)
if __name__ == '__main__':
    # Detemine path to configuration file. This path manipulation is

    # here so that the script will run sucessfully regardless of the
    # current working directory.

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-ff')

    # redirect print
    original = sys.stdout
    log_path = os.path.join(local_dir, 'ffnn.log')
    sys.stdout = open('ffnn.log', 'w')

    # run program
    run(config_path)

    # redirect print
    sys.stdout = original
