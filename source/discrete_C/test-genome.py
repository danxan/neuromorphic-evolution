"""
Test the performance of the best genome produced by evolve-feedforward.py.
"""

from __future__ import print_function

import os
import pickle

import argparse

#from movie import make_movie

import neat
import visualize

from game import Game
import screen

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("g", help="the filename of the genome")
    parser.add_argument("c", help="the filename of the config")
    args = parser.parse_args()

    # load the winner
    with open(args.g, 'rb') as f:
        genome = pickle.load(f)

    print('Loaded genome:')
    print(genome)

    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, args.c)



    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    print("Loaded config:")
    print(config)

    net = neat.nn.recurrent.RecurrentNetwork.create(c, config)
    game = Game(8)
    fitness_list = []
    trials = 10
    for i in range(trials):
        num_games = 128
        fitness = 0
        for i in range(num_games):
            ret = game.run(net)
            fitness += ret
        fitness_list.append(fitness)

    print(" ")
    print("Final conditions over {} trials of {} games:".format(trials, num_games))
    print("Max fitness: {}".format(max(fitness_list)))
    print("Mean fitness: {}".format(mean(fitness_list)))
    print("Min fitness: {}".format(sum(fitness_list)/len(fitness_list)))
    print(" ")
    print("Making movie...")
    #make_movie(net, discrete_actuator_force, 15.0, "feedforward-movie.mp4")
    print(" ")
    print("Vizualising network")
    node_names = {-1: 'inA', -2: 'inB', 0: 'outA', 1: 'outB'}
    visualize.draw_net(config, genome, True, node_names=node_names)

    visualize.draw_net(config, genome, view=True, node_names=node_names,
                       filename="net.gv")
    visualize.draw_net(config, genome, view=True, node_names=node_names,
                       filename="net-enabled.gv", show_disabled=False)
    visualize.draw_net(config, genome, view=True, node_names=node_names,
                       filename="net-enabled-pruned.gv", show_disabled=False, prune_unused=True)
