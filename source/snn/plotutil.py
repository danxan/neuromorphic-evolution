import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pickle
import numpy as np

def find_factors(number):
    root = np.sqrt(number)
    if int(root) != root:
        r1 = int(root)
        r2 = int(root)+1
    else:
        r1 = int(root)
        r2 = int(root)
    return r1, r2

def plot_paramsfile(filename):

    with open(filename, 'rb') as h:
        animatlog = pickle.load(h)

        nps = 5
        f1, f2 = find_factors(nps)
        fig = plt.figure(constrained_layout=True)
        spec = gridspec.GridSpec(ncols=f2, nrows=f1, figure=fig) 

        cnt = 0
        ax = fig.add_subplot(spec[cnt%f1, cnt%f2])
        for i in range(len(animatlog)):
            if cnt%nps == 0:
                ax = fig.add_subplot(spec[cnt%f1, cnt%f2])
            cnt += 1
            params = animatlog[i]
            alabel = 'Animat ID: '+str(params['id'])
            ax.plot(params['mean_w'], params['outputs'], label=alabel)
            ax.legend()

        plt.show()

if __name__ == '__main__':
    plot_paramsfile(sys.argv[1])
