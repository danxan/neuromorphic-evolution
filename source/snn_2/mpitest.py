import pyNN.nest as pynn
from pyNN.random import NumpyRNG
from pyNN.utility.plotting import Figure, Panel
from nest import Rank, SetKernelStatus

from mpi4py import MPI


class Animat(object):
    def __init__(self, rank):
        print('beginning of animat')
        self.pi = pynn.Population(1, pynn.SpikeSourceArray(spike_times=[10]))
        self.ph = pynn.Population(1, pynn.IF_cond_exp())
        self.po = pynn.Population(1, pynn.IF_cond_exp())
        self.po.record('spikes')

        connector = pynn.AllToAllConnector()

        p = pynn.Projection(self.pi, self.ph, connector)
        p = pynn.Projection(self.ph, self.po, connector)

        print('end of animat')

if __name__ == '__main__':
    rng = NumpyRNG(seed=21324, parallel_safe=False)
    myrank = pynn.setup()
    print('starting: {}'.format(myrank))
    a = Animat(myrank)


    print('before run')
    pynn.run(100)

    print('after run')


    print('proc {} is gonna print'.format(myrank))
    try:
        x = a.po.get_data(gather=False).segments[-1].spiketrains[0]
        print(x)
    except IndexError:
        print('{} has nothing'.format(myrank))
    print('endig: {}'.format(myrank))
    pynn.end()



