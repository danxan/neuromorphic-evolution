from nest import *
import numpy as np

class Genome(object):
    def __init__(self, ps, nh, id):
        self.id = id
        self.fitness = 0
        self.ps = ps
        self.ni = 2
        self.nh = nh
        self.no = 2
        self.iw = np.random.randint(1000, high=10000, size=(self.ni,self.nh))
        self.iw = self.iw.astype(np.float)
        self.hw = np.random.randint(1000, high=10000, size=(self.nh,self.nh))
        self.hw = self.hw.astype(np.float)
        self.ow = np.random.randint(1000, high=10000, size=(self.nh,self.no))
        self.ow = self.ow.astype(np.float)
