from pyNN.nest import *

class Animat:
    def __init__(self):

        # to make the neurons spike, each neuron must be a population of neurons
        neurons = []
        for i in range(8):
            n = Population(10, iaf_cond_exp)
            neurons.append(n)

        for i in range(
