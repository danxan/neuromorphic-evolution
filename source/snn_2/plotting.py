import matplotlib as mpl
import matplotlib.pyplot as plt
#from ann.ann_sga import *
from nestAnimat import *
from nestGame import *
from nestGenome import Genome


def plot_fitness(ax, max_fitness, maxscores, meanscores, param_dict):
    maxscores = np.array(maxscores)
    maxscores = maxscores*100/max_fitness
    meanscores = np.array(meanscores)
    meanscores = meanscores*100/max_fitness
    ax.set_ylabel('Fitness (%)')
    ax.set_xlabel('Generations')
    ax.set_ylim(0,100)
    ax.plot(maxscores, label='Max Fitness', **param_dict)
    ax.plot(meanscores, label='Mean Fitness', **param_dict)
    ax.legend()
    return ax

if __name__ == '__main__':

    import pickle
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--open")
    parser.add_argument("--search")
    parser.add_argument("--dir")
    parser.add_argument("--type")
    args = parser.parse_args()


    if args.open:
        with open(args.fname, 'rb') as f:
            fig = plt.figure()
            fig, ax = plt.subplots()
            up = pickle.Unpickler(f)
            if args.type == "sga":
                sga = up.load()
                plot_fitness(ax, 128,  res['score_max_gen'], res['score_mean_gen'], {})
            else:
                res = up.load()


        plt.show()
    elif args.search:
        import os
        import fnmatch
        filenames = []
        for filename in os.listdir(args.dir):
            word = args.search
            word = '*'+args.search+'*'
            if fnmatch.fnmatch(filename, word):
                filename = args.dir+filename
                filenames.append(filename)
        for i, filename in enumerate(filenames[:100]):
            plt.ion()
            fig = plt.figure()
            fig, ax = plt.subplots()
            with open(filename, 'rb') as f:
                up = pickle.Unpickler(f)
                if args.type == "sga":
                    sga = up.load()
                    ret = plot_fitness(ax, 128,  sga.score_max_gen, sga.score_mean_gen, {})
                else:
                    res = up.load()
                    ret = plot_fitness(ax, 128,  res['scoreMax'], res['scoreMean'], {})
        plt.show(True)
        input()





