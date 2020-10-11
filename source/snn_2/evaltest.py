import pyNN.nest as pynn
from nest import Rank, SetKernelStatus
import neat

import numpy as np

from multiprocessing import Pool

from nest import SetKernelStatus
from pynnAnimat import Animat
from pynnGame import Game
from genome import SgaGenome


class Eval(object):
    def __init__(self):
        self.mock = 1
        #pynn.setup()

    def eval_genome(self, genome, animat):
        pynn.reset()
        #pynn.setup()
        genome.fitness = 0
        #animat = Animat(input_n=2, hidden_n=4, output_n=2, pop_size=5)
        animat.setWeights(genome.genes)
        xor_in = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (1.0, 1.0)]
        xor_out = [(0.0,), (1.0,), (1.0,), (0.0,)]
        genome.fitness = 0.0
        prev_stop = 0
        total_time = 0
        for xi, xo in zip(xor_in, xor_out):
            prev_stop = total_time
            total_time = animat.run(stimuli=xi, start=prev_stop)
            s1 = 0
            s2 = 0
            o1 = animat.out.populations[0]
            o2 = animat.out.populations[1]
            spikes1 = o1.get_data(gather=False).segments[-1].spiketrains[0]
            spikes2 = o2.get_data(gather=False).segments[-1].spiketrains[0]
            for t1 in spikes1:
                t1 = float(t1)
                if t1 > prev_stop:
                    s1 += 1
            for t2 in spikes2:
                t2 = float(t2)
                if t2 > prev_stop:
                    s2 += 1
            output = 0
            if s1 > s2 or s2 > s1:
                output = 1.0

            #print("output {} and xo {} and output==xo {}".format(output, xo, output==xo[0]))
            if output == xo[0]:
                genome.fitness += 1

        pynn.end()

        return genome
