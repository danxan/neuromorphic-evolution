from nest import *
import numpy as np

class Genome(object):
    def __init__(self, id, ps=5, nh=4, low=-1000, high=1000, min_fitness=0):
        self.id = id
        self.fitness = min_fitness
        self.ps = ps
        self.ni = 2
        self.nh = nh
        self.no = 2
        self.iw = np.random.randint(low, high=high, size=(self.ni,self.nh))
        self.iw = self.iw.astype(np.float)
        self.hw = np.random.randint(low, high=high, size=(self.nh,self.nh))
        self.hw = self.hw.astype(np.float)
        self.ow = np.random.randint(low, high=high, size=(self.nh,self.no))
        self.ow = self.ow.astype(np.float)
