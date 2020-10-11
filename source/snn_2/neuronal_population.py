#!/usr/bin/env python
# -*- coding: utf-8; -*-

import os
import numpy as np
import random

from pyhalbe import HICANN
import pyhalbe.Coordinate as C
from pysthal.command_line_util import init_logger
import pysthal

import pyhmf as pynn

import uuid

class Neuronal_population(object):
    def __init__(self, num_pop, pop_size):
        self.neuron_parameters = {
        'cm': 0.2,
        'v_reset': -70.,
        'v_rest': -20.,
        'v_thresh': -15.,
        'e_rev_I': -100.,
        'e_rev_E': 60.,
        'tau_m': 7.,
        'tau_refrac': 4.,
        'tau_syn_E': 5.,
        'tau_syn_I': 5.,
        }

        self.num_pop = num_pop
        self.pop_size = pop_size
        self.populations = []
        self.asm = pynn.Assembly()
        for i in range(int(num_pop)):
            self.pop = pynn.Population(pop_size, pynn.IF_cond_exp, self.neuron_parameters)
            self.populations.append(self.pop)
            self.asm += self.pop
            self.pop.record()

        self.outgoing_projections = {   'exc' : {},
                                        'inh' : {} }


        self.incoming_projections = {   'exc' : {},
                                        'inh' : {} }


class Ring_population(Neuronal_population):
    def __init__(self, num_pop, pop_size):
        Neuronal_population.__init__(self, num_pop, pop_size)
        self.config_ring()

    """
    neuronal_pop is a population consisting of pynn.Populations
    """
    def config_ring(self):
        connector = pynn.AllToAllConnector(weights=1)

        exc_spike_times = [
            100
        ]

        inh_spike_times = [
        ]

        self.ring_stim_exc = []
        self.ring_stim_inh = []

        stimulus_exc = pynn.Population(self.pop_size, pynn.SpikeSourceArray, {
            'spike_times': exc_spike_times})
        self.ring_stim_exc.append(stimulus_exc)

        self.projections = {
                'self.populations[0]' :pynn.Projection(stimulus_exc, self.populations[0], connector, target='excitatory'),
        }
        self.np_projections.append(self.projections)

        for pop_a, pop_b in zip(self.populations, self.populations[1:]):
            self.projections = [
                pynn.Projection(pop_a, pop_b, connector, target='excitatory'),
                pynn.Projection(pop_b, pop_a, connector, target='inhibitory'),
            ]
            self.np_projections.append(self.projections)


        self.projections = [
            pynn.Projection(self.populations[-1], self.populations[0], connector, target='excitatory'),
        ]
        self.np_projections.append(self.projections)


"""
num_pop for sensor_population is half the size of num_pop of ring_pop, rounded up.
"""
class Sensor_population(Neuronal_population):
    def __init__(self, ring_pop, pop_size):
        if type(ring_pop) == type(list()):
            num_pop = np.ceil(len(ring_pop)/2.)
        else:
            print("need to input ring_pop as a list")

        Neuronal_population.__init__(self, num_pop, pop_size)
        self.connect_to_ring(ring_pop)


    """
    ring_pop: list of pynn.Populations
    """
    def connect_to_ring(self, ring_pop):
        connector = pynn.AllToAllConnector(weights=1)

        for i in range(len(ring_pop)):
            if i < len(self.populations):
                self.projections = [
                    pynn.Projection(ring_pop[i], self.populations[i],  connector, target='excitatory'),
                ]
                self.np_projections.append(self.projections)
            else:
                self.projections = [
                    pynn.Projection(ring_pop[i], self.populations[-1 -(i%len(self.populations))],  connector, target='excitatory'),
                ]
                self.np_projections.append(self.projections)

"""
The motor is supposed to stop the ring, and fitness in measured both in terms of how fast the ring is stopped and how many fires was used.
After a set time, the ring is stopped by the program and the animat is assignment minimum fitness.
TODO: Figure out how to check if the animat stopped the block or if the block was stopped by a random cause (it seems this can happen if mapping on HICANNs is unstable).
"""
class Motor_population(Neuronal_population):
    def __init__(self, num_pop = 1, pop_size = 5):
        Neuronal_population.__init__(self, num_pop, pop_size)

    """
    ring_pop: list of pynn.Populations
    """
    def connect_to_ring(self, ring_pop):
        connector = pynn.AllToAllConnector(weights=1)

        marker = np.ceil(len(ring_pop)/2.)

        for pop in self.populations:
            self.projections = [
                    pynn.Projection(pop, ring_pop[marker], connector, target='inhibitory'),
            ]
            self.np_projections.append(self.projections)

    """
    time_of_murder is a float value
    """
    def setup_kill_manually(self, time_of_murder):
        connector = pynn.AllToAllConnector(weights=1)
        exc_spike_times = [
            time_of_murder
        ]

        motor_stim_exc = []

        stimulus_exc = pynn.Population(self.pop_size, pynn.SpikeSourceArray, {
            'spike_times': exc_spike_times})
        motor_stim_exc.append(motor_stimulus_exc)

        for pop in self.populations:
            self.projections = [
                pynn.Projection(stimulus_exc, pop, connector, target='excitatory'),
            ]
            self.np_projections.append(self.projections)

class Network_population(Neuronal_population):
    def __init__(self, num_pop, pop_size):
        Neuronal_population.__init__(self, num_pop, pop_size)

    def config_all_to_all(self):
        connector = pynn.AllToAllConnector(weights=1) #TODO: allow self connections?

        for i, pop in enumerate(self.populations):
            for j, other_pop in enumerate(self.populations):
                self.projections = [
                        pynn.Projection(pop, other_pop, connector, target='excitatory'),
                ]
                self.np_projections.append(projections)

                self.projections = [
                        pynn.Projection(pop, other_pop, connector, target='inhibitory'),
                ]
                self.np_projections.append(projections)
    """
    Each animat has a genome, initialized with random values between 1 and 15.
    After assessing the fitness the most fit individuals will be duplicated
    and the duplicate will be  mutated randomly.

    Assuming a counter, numex, numin, for the number of each of the synapse types, excitatory and inhibitory.

    genome = [[random.randint(1,15) for i in range(numex)], \
    [random.randint(1,15) for i in range(numin)]]


    """



    """
    genome: 3d list of values that determine the strength of synapses
    """
    """
    def reconfig(genome):
        for i in range(genome[0]):
            for j in range(genome[0]):
                val_p = genome[i,j][0]
                val_n = genome[i,j][1]

        change synapse strengths based on genome.
        e.g.:
            a = genome[i,j][0]
            b = genome[i,j][1]
                set excitatory connection between pop[i] and pop[j] to a,
                and set inhibitory connection between pop[i] and pop[j] to b
                vice versa...
        """



