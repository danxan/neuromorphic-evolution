import numpy as np
import random

class Animat:
    def __init__(self, num_nodes):
        self.score = 0
        self.genome = np.random.randint(-15,15, (num_nodes, num_nodes))
        # TODO: fix weights, cant be genome
        #genome = genome/np.linalg.norm(genome)
        #genome = 2.*(genome - np.min(genome))/np.ptp(genome)-1
        print(f"genome: {self.genome}")
        print(f"sum:  {sum(self.genome)}")
        print(f"count zeros:  {np.count_nonzero(self.genome==0)}")

    '''
    def _or_func(self, neur_in):
        # OR
        treshold = 0
        if np.mean(neur_in) > treshold:
            return 1
        elif np.mean(neur_in) < treshold:
            return -1
        else:
            return 0
    '''

    '''
    def run(self, sens_in):
        print(f'sense in: {sens_in}')
        neur_in = sens_in*self.genome
        print(f'neur in: {neur_in}')
        ret = self._or_func(neur_in)
        print(f"animat motor output is: {ret}")
        return ret
    '''

    def update_score(self, points):
        self.score += points
