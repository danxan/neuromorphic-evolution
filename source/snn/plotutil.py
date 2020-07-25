import sys
import os

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.interpolate import interp1d
import pickle
import numpy as np

from datetime import datetime

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

    # For saving data to file
    local_dir = os.path.dirname(__file__)
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y-%b-%d-%H:%M:%S:%f")

    with open(filename, 'rb') as h:
        animatlog = pickle.load(h)

        nps = 5
        f1, f2 = find_factors(nps)
        fig = plt.figure(constrained_layout=True)
        spec = gridspec.GridSpec(ncols=f2, nrows=f1, figure=fig)

        cnt = 0
        for i in range(len(animatlog)):
            if cnt%nps == 0:
                ax = fig.add_subplot(spec[cnt%f1, cnt%f2])
            cnt += 1
            params = animatlog[i]

            alabel = 'Animat ID: '+str(params['id'])

            idxa = np.argsort(params['mean_w'])

            eps = np.linspace(0,0.01,len(params['mean_w']))
            mean_w = np.array([params['mean_w'][i] for i in idxa])
            mean_w = mean_w+eps
            outputs = np.array([params['outputs'][i] for i in idxa])
            outputs = outputs + 3*np.random.rand(len(outputs))

            xnew = np.linspace(0,np.max(params['mean_w']), num=1000, endpoint=True)
            f = interp1d(mean_w, outputs)

            ax.plot(mean_w, outputs, 'o', xnew, f(xnew), '--')

            if cnt%nps == 0:
                ax.legend()

        figname = 'results/paramplot_date['+str(timestamp)+'].svg'
        figname = os.path.join(local_dir, figname)
        fig.savefig(figname)
        plt.show()

if __name__ == '__main__':
    plot_paramsfile(sys.argv[1])

    '''
    # Creating figure for plotting
    fig = plt.figure(constrained_layout=True)
           n1 = i%r1
            n2 = i%r2
            ax = fig.add_subplot(spec[n1, n2])
            ax.title.set_text('tau_m='+str(t))

    pec = gridspec.GridSpec(ncols=r2, nrows=r1, figure=fig)

                            alabel = 'Animat ID: '+str(a.id)
                            idxa = np.argsort(params['mean_w'])

                            eps = np.linspace(0,0.01,len(params['mean_w']))
                            mean_w = np.array([params['mean_w'][i] for i in idxa])
                            mean_w = mean_w+eps
                            outputs = np.array([params['outputs'][i] for i in idxa])
                            outputs = outputs + 3*np.random.rand(len(outputs))
                            xnew = np.linspace(0,np.max(params['mean_w']), num=1000, endpoint=True)
                            f = interp1d(mean_w, outputs)
                            ax.plot(params['mean_w'], params['outputs'], 'o', xnew, f(xnew), '--')
                            ax.legend(['data', 'cs'])

    # End of a tau_m iteration
    figname = 'paramplot_date['+str(timestamp)+'].svg'
    figname = os.path.join(local_dir, figname)
    '''
    #fig.savefig(figname)
