import os

import numpy as np
import matplotlib.pyplot as plt
from quantities import nA

import pyNN.nest as pynn
from nest import Rank
from nest import SetKernelStatus

from threading import Thread

from nodes import *

class Animat(object):
    def __init__(self, input_n=2, hidden_n=4, output_n=2, pop_size=1):
        print('Creating animat')
        self.total_runtime = 0

        self.pop_size = pop_size

        self.num_inp = input_n
        self.num_hid = hidden_n
        self.num_out = output_n

        self.inp = Input_nodes(num_pop=input_n, pop_size=pop_size)
        #print(self.inp.populations)
        self.hid = Hidden_nodes(num_pop=hidden_n, pop_size=pop_size)
        #print(self.hid.populations)
        self.out = Output_nodes(num_pop=output_n, pop_size=pop_size)
        #print(self.out.populations)

        connector = pynn.AllToAllConnector()

        self.input_connections = { 'exc' : [],
                                   'inh' : [] }

        self.hidden_connections = { 'exc' : [],
                                    'inh' : [] }

        self.output_connections = { 'exc' : [],
                                    'inh' : [] }

        for i in self.inp.populations:
            for h in self.hid.populations:
                self.input_connections['exc'].append(pynn.Projection(i, h, connector, receptor_type='excitatory'))
                self.input_connections['inh'].append(pynn.Projection(i, h, connector, receptor_type='inhibitory'))

        for h in self.hid.populations:
            for h in self.hid.populations:
                self.hidden_connections['exc'].append(pynn.Projection(h, h, connector, receptor_type='excitatory'))
                self.hidden_connections['inh'].append(pynn.Projection(h, h, connector, receptor_type='inhibitory'))

        for h in self.hid.populations:
            for o in self.out.populations:
                self.output_connections['exc'].append(pynn.Projection(h, o, connector, receptor_type='excitatory'))
                self.output_connections['inh'].append(pynn.Projection(h, o, connector, receptor_type='inhibitory'))

    def setWeights(self, genome):
        if len(genome) < (self.num_inp*self.num_hid+self.num_hid*self.num_hid+self.num_hid*self.num_out):
            print("There's not enough genes in the genome to set all the weights. The remainder of the synapses will remain unchanged.")
        for i, g in enumerate(genome):
            if i < self.num_inp:
                self.input_connections['exc'][i%self.num_inp].set(weight=0)
                self.input_connections['inh'][i%self.num_inp].set(weight=0)
                if g > 0:
                    self.input_connections['exc'][i%self.num_inp].set(weight=g)
                elif g < 0:
                    self.input_connections['inh'][i%self.num_inp].set(weight=-g)

            if i < self.num_inp+self.num_hid:
                self.hidden_connections['exc'][i%self.num_hid].set(weight=0)
                self.hidden_connections['inh'][i%self.num_hid].set(weight=0)
                if g > 0:
                    self.hidden_connections['exc'][i%self.num_hid].set(weight=g)
                elif g < 0:
                    self.hidden_connections['inh'][i%self.num_hid].set(weight=-g)

            if i < self.num_inp+self.num_hid+self.num_out:
                self.output_connections['exc'][i%self.num_out].set(weight=0)
                self.output_connections['inh'][i%self.num_out].set(weight=0)
                if g > 0:
                    self.output_connections['exc'][i%self.num_out].set(weight=g)
                elif g < 0:
                    self.output_connections['inh'][i%self.num_out].set(weight=-g)

    def plot_spiketrains(self, segment):
        for spiketrain in segment.spiketrains:
            y = np.ones_like(spiketrain) * spiketrain.annotations['source_id']
            plt.plot(spiketrain, y, '.')
            plt.ylabel(segment.name)
            plt.setp(plt.gca().get_xticklabels(), visible=False)

    def plot_signal(self, signal, index, colour='b'):
        label = "Neuron %d" % signal.annotations['source_ids'][index]
        plt.plot(signal.times, signal[:, index], colour, label=label)
        plt.ylabel("%s (%s)" % (signal.name, signal.units._dimensionality.string))
        plt.setp(plt.gca().get_xticklabels(), visible=False)
        plt.legend()

    def plot(self):
        from pyNN.utility.plotting import Figure, Panel
        # PLOT OUTPUT
        o1 = self.out.populations[0].get_data(gather=False).segments[-1]

        vm1 = o1.filter(name='v')[0]

        o2 = self.out.populations[1].get_data(gather=False).segments[-1]

        vm2 = o2.filter(name='v')[0]

        Figure(
            Panel(vm1, ylabel='Membrane potential (mV)', xticks=True, xlabel="Time (ms)", yticks=True),
            Panel(o1.spiketrains, xlabel='Output 1', xticks=True),
            Panel(vm2, ylabel='Membrane potential (mV)', xticks=True, xlabel="Time (ms)", yticks=True),
            Panel(o2.spiketrains, xlabel='Output 2', xticks=True)
        ).save('simulation_results_outputnodes.png')

        plt.show()


    def run(self, stimuli=[0,0], start=0, runtime=30, plot=False):
        # TODO: This code only works for animats with 2 input nodes
        for i, node in enumerate(self.inp.populations):
            if stimuli[i] == 1:
                start = start+1
                #print("START")
                #print(start)
                node.set(spike_times=[start])
                #node.initialize(v=1)

        stop = start+runtime
        pynn.run_until(stop)

        if plot:
            from pyNN.utility.plotting import Figure, Panel
            # PLOT OUTPUT
            o1 = self.out.populations[0].get_data(gather=False).segments[-1]

            vm1 = o1.filter(name='v')[0]

            o2 = self.out.populations[1].get_data(gather=False).segments[-1]

            vm2 = o2.filter(name='v')[0]

            Figure(
                Panel(vm1, ylabel='Membrane potential (mV)', xticks=True, xlabel="Time (ms)", yticks=True),
                Panel(o1.spiketrains, xlabel='Output 1', xticks=True),
                Panel(vm2, ylabel='Membrane potential (mV)', xticks=True, xlabel="Time (ms)", yticks=True),
                Panel(o2.spiketrains, xlabel='Output 2', xticks=True)
            ).save('simulation_results_outputnodes.png')

            plt.show()

        return float(pynn.get_current_time())

if __name__ == '__main__':
    import random
    pynn.setup()
    animat = Animat(pop_size=5, input_n=2, output_n=2, hidden_n=4)
    #genome = [random.randint(0,15) for i in range(2*(2*4+4*4+4*2))]
    genome = np.random.randint(-15,15, (2*4+4*4+4*2))
    for i, g in enumerate(genome):
        if np.random.random() > 0.3:
            genome[i] = 0
    genome[0] = 15
    genome[1] = 15

    genome = np.array([  2, -11, -11,   1,  14,  11,   0,   0,   0,  -7,  10,   7,   4,
        -7,   2,   5,   8,  -9,  13,  -5, -11,   3,   7,  -4,   5,   0,
        -6,  -2,  -4,  14,  -9, -15])
    genome[0] = 15
    genome[1] = 15
    print(genome)
    animat.setWeights(genome)
    animat.run(stimuli=[1,1])

