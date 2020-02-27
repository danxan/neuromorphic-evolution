import sys
import os
import neat
from neat import activations
from animat import Animat
from game import Game

def eval_genomes(genomes, config):
    num_games = 100
    for genime_id, genome in genomes:
        genome.fitness = 0
        '''
        node_evals = {1: (0.01, activations.sigmoid_activation, sum, 0, 1.0, [(-1, 1.0)]),
                      2: (0.01, activations.sigmoid_activation, sum, 0, 1.0, [(-1, 1.0)]),
                      3: (0.01, activations.sigmoid_activation, sum, 0, 1.0, [(-1, 1.0)]),
                      4: (0.01, activations.sigmoid_activation, sum, 0, 1.0, [(-1, 1.0)]),
                      5: (0.01, activations.sigmoid_activation, sum, 0, 1.0, [(-1, 1.0)]),
                      6: (0.01, activations.sigmoid_activation, sum, 0, 1.0, [(-1, 1.0)]),
                      7: (0.01, activations.sigmoid_activation, sum, 0, 1.0, [(-1, 1.0)]),
                      8: (0.01, activations.sigmoid_activation, sum, 0, 1.0, [(-1, 1.0)])}
        '''
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        game = Game()
        for i in range(num_games):
            genome.fitness = game.run(net)

def run(config_file):
    num_games = 100
    # Load configuration
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
            neat.DefaultSpeciesSet, neat.DefaultStagnation,
            config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    num_gen = 300
    # Run each genome through 100 games.
    winner = p.run(eval_genomes, num_gen)

    # Display the winning genome
    print(f'\nBest genome:\n{winner}')

    # Show output of the most fit genome against training data.
    print('\nOutput:')
    winner_net = neat.nn.recurrent.RecurrentNetwork.create(winner, config)
    game = Game()
    for i in range(num_games):
        winner.fitness = game.run(winner)
    print(f'\nOver {num_games} games, a winner scored {winner.fitness}.\n')

if __name__ == '__main__':
    # Detemine path to configuration file. This path manipulation is
    # here so that the script will run sucessfully regardless of the
    # current working directory.

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-discrete')

    # redirect print
    original = sys.stdout
    log_path = os.path.join(local_dir, 'log-discrete')
    sys.stdout = open('log_path', 'w')

    # run program
    run(config_path)

    # redirect print
    sys.stdout = original
