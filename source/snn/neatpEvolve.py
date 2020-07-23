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
class pynnIFCondExpGene(BaseGene):
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

class 



    






