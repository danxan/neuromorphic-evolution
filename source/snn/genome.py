import numpy as np
from pyNN.random import NumpyRNG, RandomDistribution

class SgaGenome(object):
    def __init__(self, pop_size=5, num_inp=2, num_hid=4, num_out=2, id=0):
        self.id = id
        self.num_inp = num_inp
        self.num_hid = num_hid
        self.num_out = num_out
        self.pop_size = pop_size
        self.fitness = 0
        ni = self.num_inp
        nh = self.num_hid
        no = self.num_out
        rng = NumpyRNG(seed=id*ni*nh*no, parallel_safe=True)
        self.genes = RandomDistribution('normal', (-5,5), rng=rng).next(ni*nh+nh*nh+nh*no)
        self.genes[0] = 5
        self.genes[1] = 5
