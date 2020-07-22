import numpy as np
import matplotlib.pyplot as plt

import pyNN.nest as pynn

from pynnGame import Game
from pynnAnimat import Animat
import nodes

if __name__ == '__main__':

    # 100 values between 0 and 1 and 40 elements between 1 and 20
    tau_m = list(np.linspace(0,1,100))+list(np.linspace(1,20, 40)) 
    tau_syn_E = list(np.linspace(0,1, 100))+list(np.linspace(1,5, 40))
    tau_syn_I = list(np.linspace(0,1, 100))+list(np.linspace(1,5, 40))
    
    v_reset = np.linspace(-90, -60, 3)
    e_rev_E = np.linspace(-90, 0, 6)
    e_rev_I = np.linspace(-90, 0, 6)

    # chain of 3 single nodes
    a = Animat(pop_size=5, input_n=1, hidden_n=1, output_n=1)
    genome = np.array([15,15,0,8,6,0,0,14,0,0,0,12,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,8,13,0,0,13,9,0,0,0,0,0,0,3,0,0,5,6,4,7,0,0,13,0,0,0,0,0,0,13,6,13,0,0,0,0,8,5,0])
    print(genome)
    a.setWeights(genome)

    

    

    

