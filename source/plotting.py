import matplotlib as mpl
import matplotlib.pyplot as plt
from ann_sga import *

def load_maxmin(filenames, type="none"):
    ''' loads scoremax and scoremean from files and into two lists '''
    score_max = []
    score_mean = []
    for i, filename in enumerate(filenames[:10]):
        with open(filename, 'rb') as f:
            if type == "sga":
                sga = pickle.load(f)
                score_max.append(sga.score_max_gen)
                score_mean.append(sga.score_mean_gen)
            else:
                ret = up.load()
                score_max.append(ret['score_max_gen'])
                score_mean.append(ret['score_mean_gen'])

    return score_max, score_mean

def convert_to_percent(max_fitness, value):
    ''' Expects numpyarray, list or int/float, returns numpy array or float '''
    value = np.array(value)
    print(type(value))
    return value*100/max_fitness

def plot_fitness(ax, max_fitness, maxscores, meanscores, param_dict):
    maxscores = np.array(maxscores)
    maxscores = convert_to_percent(max_fitness, maxscores)
    meanscores = np.array(meanscores)
    meanscores = convert_to_percent(max_fitness, meanscores)
    ax.set_ylabel('Fitness (%)')
    ax.set_xlabel('Generations')
    ax.set_ylim(0,100)
    ax.plot(maxscores, label='Max Fitness', **param_dict)
    ax.plot(meanscores, label='Mean Fitness', **param_dict)
    ax.legend()
    return ax


def plot_box1000(ax, scores, names, param_dict):
    '''
    Expects lists with data for eac run to be plotted.
    scores: list of scores for each run
    names: names of each run
    '''
    for s in scores:
        s = convert_to_percent(max_fitness, s)


    ax.set_ylabel('Fitness (%)')
    ax.set_ylim(0,100)

    ax.boxplot(scores,  notch=True)
    ax.xticks(names)
    return ax

def plot_box100x100(ax, max_fitness, maxscores, meanscores, param_dict):
    for s in maxscores:
        s = convert_to_percent(max_fitness, s)
    for s in meanscores:
        s = convert_to_percent(max_fitness, s)

    ax.set_ylabel('Fitness (%)')
    ax.set_ylim(0,100)

    '''
    c = 'blue'
    plotparams = { 'notch':True, 'patch_artist':True,
            'boxprops':dict(facecolor=c, color=c),
            'capprops':dict(color=c),
            'whiskerprops':dict(color=c),
            'flierprops':dict(color=c, markeredgecolor=c),
            'medianprops':dict(color=c)
            }
    ax.boxplot(maxscores, pc = "red"
    '''
    c = 'blue'
    c2 = 'cyan'
    bp1 = ax.boxplot(maxscores, notch=True, patch_artist=True,
                boxprops=dict(facecolor=c, color=c2),
                capprops=dict(color=c),
                whiskerprops=dict(color=c),
                flierprops=dict(color=c, markeredgecolor=c),
                medianprops=dict(color=c),
                )
    c = 'orange'
    c2 = 'yellow'
    bp2 = ax.boxplot(meanscores, notch=True, patch_artist=True,
                boxprops=dict(facecolor=c, color=c2),
                capprops=dict(color=c),
                whiskerprops=dict(color=c),
                flierprops=dict(color=c, markeredgecolor=c),
                medianprops=dict(color=c),
                )
    '''
    c = 'orange'
    c2 = '
    ax.boxplot(meanscores,  plotparams)
    '''
    ax.legend([bp1['boxes'][0], bp2['boxes'][0]], ['Max', 'Mean'], loc='upper right')
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
    parser.add_argument("--plot")
    parser.add_argument("--thousand")
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

        score_max, score_mean = load_file(filenames, type=args.type)

        if args.plot == "box":
            print("hey")
            fig = plt.figure()
            fig, ax = plt.subplots()
            ret = plot_box100x100(ax, 128, score_max, score_mean, {})

        else:
            print(filenames)
            for i, filename in enumerate(filenames):
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
                        ret = plot_fitness(ax, 128,  res['score_max_gen'], res['score_mean_gen'], {})
        plt.show(True)
        input()

    elif args.thousand:
        import os
        import fnmatch







