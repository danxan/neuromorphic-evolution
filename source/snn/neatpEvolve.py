import os
import sys
import numpy as np
import matplotlib.pyplot as plt

import neat.attributes import FloatAttribute
from neat.genes import BaseGene, DefaultConnectionGene
from neat.genome import DefaultGenomeConfig, DefaultGenome
from neat.graphs import required_for_output

import pyNN.nest as pynn

# a, b, c, d, are the most important parameters of the pyNN.nest.IF_cond_exp model
# a: tau_m
# b: tau_syn_E
# c: tau_syn_I
# d: v_reset 
class pynnIFNodeGene(BaseGene):
    ''' Tailored for the
    pyNN.nest.IF_cond_exp gene and determines genomic distances.
    '''

    _gene_attributes = [FloatAttribute('bias'),
                        FloatAttribute('a'),
                        FloatAttribute('b'),
                        FloatAttribute('c'),
                        FloatAttribute('d')]

    def distance(self, other, config):
        s = abs(self.a - other.a) + abs(self.b - other.b) \
            + abs(self.c - other.c) + abs(self.d - other.d)
        return s * config.compatibilit_weight_coefficient

# TODO: Finish implementing if cond exp the same way as IZ but using nest
# TODO: Friday: Get a docker-image set-up to run simulations on freebio.
# TODO: Weekend: Run simulations on neat-nest, sga-nest. Also do comparison plots on neat and sga.
# TODO: Next week: Do an IIT analysis. 
# TODO: Next week: Move

class pynnIFGenome(DefaultGenome):
    @classmethod
    def parse_config(cls, param_dict):
        param_dict['node_gene_type'] = pynnIFNodeGene
        param_dict['connection_gene_type'] = DefaultConnectionGene
        return DefaultGenomeConfig(param_dict)

class pynnIFNeuron(object):
    """
    # TODO: Implement an initiation of NEST neurons here...
    def __init__(self, bias, a, b, c, d, inputs):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.bias = bias
        self.inputs = inputs

        self.v = self.c

        self.u = self.b * self.v

        self.fired = 0.0
        self.current = self.bias

    def advance(self, dt_msec):
        try:

    def reset(self):
    """

class pynnIFNN(object):
    # TODO initialization of the NEST simulator
    def __init__(self, neurons, inputs, outputs):
        self.neurons = neurons
        self.inputs = inputs
        self.outputs = outputs
        self.input_values = {}

    def set_inputs(self, inputs):

    def reset(self):

    def get_time_step_msec(self):

    def advance(self, dt_msec):

    @staticmethod
    def create(genome, config):
        """ receives a genome and returns its phenotype (a neural network). """

        


        


        


        

    


        


    






