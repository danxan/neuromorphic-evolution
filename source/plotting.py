import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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

def plot_param(ax, max_fitness, maxscores, minscores, meanscores, xrate, xlabel, param_dict):
    maxscores = np.array(maxscores)
    maxscores = convert_to_percent(max_fitness, maxscores)
    minscores = np.array(minscores)
    minscores = convert_to_percent(max_fitness, minscores)
    meanscores = np.array(meanscores)
    meanscores = convert_to_percent(max_fitness, meanscores)
    #ci = 1.96 * np.std(maxscores)/np.mean(maxscores)
    ax.set_ylabel('Fitness (%)')
    ax.set_xlabel(xlabel)
    ax.set_ylim(0,100)
    ax.plot(xrate, meanscores, **param_dict)
    ax.fill_between(xrate, minscores, maxscores, color='yellow', alpha=0.09)
    ax.legend()
    return ax


def plot_box1000(ax, max_fitness, scores, names, param_dict):
    '''
    Expects lists with data for eac run to be plotted.
    scores: list of scores for each run
    names: names of each run
    '''
    print(scores)
    for s in scores:
        s = convert_to_percent(max_fitness, s)


    ax.set_ylabel('Fitness (%)')
    ax.set_ylim(0,100)

    print(scores)

    ax.boxplot(scores, notch=True)
    ax.set_xticklabels(names)
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


def findfiles(dir, pattern):
    import os
    import fnmatch
    filenames = []
    for filename in os.listdir(dir):
        word = '*'+pattern+'*'
        if fnmatch.fnmatch(filename, word):
            filename = dir+filename
            filenames.append(filename)

    return filenames

def hundredtothousand(dir, pattern):
    filenames = findfiles(dir, pattern)
    if len(filenames) < 10:
        print("Need at least 10 files of 100invidividuals to create a 1000first file")

    scores = []
    for file in filenames[:10]:
        with open(file, 'rb') as f:
            scores.append(pickle.load(f))

    filename = dir+"1000first_nest"
    with open(filename, 'wb') as f:
        pickle.dump(scores, f, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':

    import pickle
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--open")
    parser.add_argument("--search")
    parser.add_argument("--dir")
    parser.add_argument("--pattern")
    parser.add_argument("--type")
    parser.add_argument("--plot")
    parser.add_argument("--hundreds")
    parser.add_argument("--neatparam")
    parser.add_argument("--confplot")
    args = parser.parse_args()

    with plt.style.context('ggplot'):

        max_fitness = 128

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
            filenames = findfiles(args.dir, args.search)

            score_max, score_mean = load_file(filenames, type=args.type)

            if args.plot == "box":
                fig = plt.figure()
                fig, ax = plt.subplots()
                ret = plot_box100x100(ax, 128, score_max, score_mean, {})

            else:
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

        elif args.hundreds:

            plotdict = {'rnn':  {'dir': 'ann/results/', 'pattern': '1000first'},
                        'nest r-snn': {'dir': 'snn/results/', 'pattern': '1000first'},
                        'nest r-snn t': {'dir': 'snn2/results/', 'pattern': '1000first'},
                        'neat rnn': {'dir': 'discrete_B-fixed-60k/results/', 'pattern': '1000first'},
                        'neat ct-rnn': {'dir': 'neat_ctrnn/results/', 'pattern': '1000first'},
                        'neat iznn': {'dir': 'neat_iznn/results/', 'pattern': '1000first'},
                        'neat iznn t': {'dir': 'neat_iznn2/results/', 'pattern': '1000first'}
                        }

            names = []
            scores = []

            plt.ion()
            fig = plt.figure()
            fig, ax = plt.subplots()
            for key in plotdict.keys():
                if key == 'nest r-snn':
                    hundredtothousand(dir, '100first')
                elif key == 'nest r-snn t':
                    hundredtothousand(dir, '100first')
                names.append(key)
                dir     = plotdict[key]['dir']
                pattern = plotdict[key]['pattern']

                filenames = findfiles(dir, pattern)
                if filenames:
                    with open(filenames[0], 'rb') as f:
                        s = pickle.load(f)
                        scores.append(s)
                else:
                    names.remove(key)


            ax = plot_box1000(ax, max_fitness, scores, names, {})
            plt.savefig("initial_thousand.eps", format='eps')
            plt.show(True)
            input()

        elif args.neatparam:
            plotdict = {'population-size':  {'dir': 'plot-params/popsize/results/', 'pattern': '100gen', 'smax':[], 'smin':[], 'smean':[], 'rate':[]},
                    'elitism-rate': {'dir': 'plot-params/elitism/results/', 'pattern': '100gen', 'smax':[], 'smin':[], 'smean':[], 'rate':[]},
                    'stagnation-rate': {'dir': 'plot-params/stagnation/results/', 'pattern': '100gen', 'smax':[], 'smin':[], 'smean':[], 'rate':[]},
                    'survival-rate': {'dir': 'plot-params/survival/results/', 'pattern': '100gen', 'smax':[], 'smin':[], 'smean':[],'rate':[]}
                        }


            for key in plotdict.keys():
                plt.ion()
                fig = plt.figure()
                fig, ax = plt.subplots()
                dir = plotdict[key]['dir']
                pattern = plotdict[key]['pattern']

                filenames = findfiles(dir, pattern)
                if filenames:
                    for fname in filenames:
                        with open(fname, 'rb') as f:
                            s = pickle.load(f)
                            smax = s['scoreMax']
                            plotdict[key]['smax'].append(np.max(smax))
                            plotdict[key]['smin'].append(np.min(smax))
                            plotdict[key]['smean'].append(np.mean(smax))


                            if key=='population-size':
                                r = s['popsize']
                            elif key=='stagnation-rate':
                                r = s['stagnation']
                            elif key=='survival-rate':
                                r = s['survival']
                            elif key=='elitism-rate':
                                r = s['elitism_rate']

                            plotdict[key]['rate'].append(r)

                rate = np.sort(plotdict[key]['rate'])
                ratesort = np.argsort(rate)[::-1]
                smax = plotdict[key]['smax']
                smax = [smax[ratesort[i]] for i in range(len(ratesort))]
                smin = plotdict[key]['smin']
                smin = [smin[ratesort[i]] for i in range(len(ratesort))]
                smean = plotdict[key]['smean']
                smean = [smean[ratesort[i]] for i in range(len(ratesort))]
                rate = np.sort(rate)
                print(rate)
                ax = plot_param(ax, 128, smax, smin, smean, rate, key, {})
                fig.savefig(key+'.pdf', format='pdf')
                fig.show()
                input()

        # end elif
        elif args.confplot:
            import pandas as pd

            plt.ion()
            fig = plt.figure()
            fig, ax = plt.subplots()

            filenames = findfiles(args.dir, args.pattern)

            scoremax = []
            scoremean = []

            fcnt = 0
            for fname in filenames:
                with open(fname, 'rb') as f:
                    s = pickle.load(f)
                    smax = s['scoreMax']
                    smean = s['scoreMean']
                    print(len(smax))
                    print(len(smean))

                    scoremax.append(smax)
                    scoremean.append(smean)

                    fcnt += 1

            smax_dict = {'max': [], 'mean':[], 'min':[]}
            smean_dict = {'max':[], 'mean':[], 'min':[]}


            for i in range(len(scoremax[0])):
                tmpmax = []
                tmpmean = []
                for j in range(fcnt):
                    #print(len(scoremax[j]))
                    #print(len(scoremax[j]))
                    tmpmax.append(scoremax[j][i])
                    tmpmean.append(scoremean[j][i])

                smax_dict['max'].append(np.max(tmpmax))
                smax_dict['mean'].append(np.mean(tmpmax))
                smax_dict['min'].append(np.min(tmpmax))

                smean_dict['max'].append(np.max(tmpmean))
                smean_dict['mean'].append(np.mean(tmpmean))
                smean_dict['min'].append(np.min(tmpmean))

            maxscores = np.array(smax_dict['max'])
            print(maxscores)
            maxscores = convert_to_percent(max_fitness, maxscores)
            minscores = np.array(smax_dict['min'])
            print(minscores)
            minscores = convert_to_percent(max_fitness, minscores)
            meanscores = np.array(smax_dict['mean'])
            print(meanscores)
            meanscores = convert_to_percent(max_fitness, meanscores)
            #ci = 1.96 * np.std(maxscores)/np.mean(maxscores)
            ax.set_ylabel('Fitness (%)')
            ax.set_xlabel('Generations')
            ax.set_ylim(0,100)
            ax.plot(list(range(len(maxscores))), meanscores, label='Max')
            ax.fill_between(list(range(len(maxscores))), minscores, maxscores, color='yellow', alpha=0.1)

            maxscores = np.array(smean_dict['max'])
            maxscores = convert_to_percent(max_fitness, maxscores)
            minscores = np.array(smean_dict['min'])
            minscores = convert_to_percent(max_fitness, minscores)
            meanscores = np.array(smean_dict['mean'])
            meanscores = convert_to_percent(max_fitness, meanscores)
            #ci = 1.96 * np.std(maxscores)/np.mean(maxscores)
            ax.plot(list(range(len(maxscores))), meanscores, label='Mean')
            ax.fill_between(list(range(len(maxscores))), minscores, maxscores, color='cyan', alpha=0.1)

            ax.legend()

            fig.show()
            input()






















































